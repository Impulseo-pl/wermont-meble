"""Pomiar jak w Lighthouse mobile: Moto G-ish viewport, Slow 4G (150 ms RTT, 1.6 Mb/s), CPU x4.
Uzycie: perf.py URL [URL...] ; kazdy URL mierzony 3x na zimnym cache, mediana."""
import sys, json, statistics
from playwright.sync_api import sync_playwright

JS = """() => new Promise(res => {
  let lcp = 0, cls = 0;
  new PerformanceObserver(l => { for (const e of l.getEntries()) lcp = e.startTime; }).observe({type:'largest-contentful-paint', buffered:true});
  new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value; }).observe({type:'layout-shift', buffered:true});
  setTimeout(() => {
    const n = performance.getEntriesByType('navigation')[0];
    const r = performance.getEntriesByType('resource');
    const fcp = (performance.getEntriesByName('first-contentful-paint')[0]||{}).startTime;
    res({ttfb: n.responseStart, fcp, lcp, cls, load: n.loadEventEnd,
         req: r.length + 1, kb: Math.round((r.reduce((a,x)=>a+(x.transferSize||0),0) + n.transferSize)/1024),
         js: r.filter(x=>x.initiatorType==='script').length,
         thirdParty: [...new Set(r.map(x=>new URL(x.name).host).filter(h=>h!==location.host))]});
  }, 3000);
})"""

def run(url):
    out = []
    with sync_playwright() as p:
        for _ in range(3):
            b = p.chromium.launch()
            ctx = b.new_context(viewport={'width': 412, 'height': 823}, device_scale_factor=1.75, is_mobile=True,
                                user_agent='Mozilla/5.0 (Linux; Android 11; moto g power) AppleWebKit/537.36 Chrome/128 Mobile Safari/537.36')
            pg = ctx.new_page()
            c = ctx.new_cdp_session(pg)
            c.send('Network.enable')
            c.send('Network.emulateNetworkConditions', {'offline': False, 'latency': 150, 'downloadThroughput': 1.6e6/8*0.9, 'uploadThroughput': 750e3/8*0.9})
            c.send('Emulation.setCPUThrottlingRate', {'rate': 4})
            pg.goto(url, wait_until='load', timeout=180000)
            out.append(pg.evaluate(JS))
            b.close()
    med = {k: round(statistics.median(o[k] for o in out)) if k != 'cls' else round(statistics.median(o[k] for o in out), 3)
           for k in ['ttfb', 'fcp', 'lcp', 'cls', 'load', 'req', 'kb', 'js']}
    med['thirdParty'] = out[-1]['thirdParty']
    return med

if __name__ == '__main__':
    res = {u: run(u) for u in sys.argv[1:]}
    print(json.dumps(res, ensure_ascii=False, indent=1))
