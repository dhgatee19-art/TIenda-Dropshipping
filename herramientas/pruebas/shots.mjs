import { chromium } from '/usr/local/lib/node_modules_global/playwright/index.mjs';
const SP = process.argv[2];
const pages = (process.argv[3] || '/').split(',');
const THEME = '200400142713';
const BASE = 'https://catboing.com';
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY } }).catch(async () =>
  chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } }));
for (const vp of [{ name: 'desk', width: 1440, height: 900 }, { name: 'movil', width: 390, height: 844, mobile: true }]) {
  const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1, isMobile: !!vp.mobile, hasTouch: !!vp.mobile, locale: 'es-ES' });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('JS: ' + e.message));
  page.on('response', r => { if (r.status() >= 400 && !r.url().includes('monorail') && !r.url().includes('analytics')) errors.push(r.status() + ' ' + r.url().slice(0, 140)); });
  const r = await ctx.request.post(BASE + '/password', { form: { form_type: 'storefront_password', utf8: '✓', password: process.env.TIENDA_PASS } });
  console.log('login', r.status(), r.url());
  for (const p of pages) {
    const url = BASE + p + (p.includes('?') ? '&' : '?') + 'preview_theme_id=' + THEME;
    await page.goto(url, { waitUntil: 'load', timeout: 60000 }).catch(e => errors.push('goto ' + e.message));
    await page.waitForTimeout(2500);
    for (const sel of ['button:has-text("Accept")', 'button:has-text("Aceptar")']) { const b = await page.$(sel); if (b) { await b.click().catch(() => {}); break; } }
    await page.addStyleTag({ content: '#PBarNextFrameWrapper, #preview-bar-iframe, iframe#preview-bar-iframe { display: none !important; }' }).catch(() => {});
    // forzar animaciones de entrada visibles y cargar imágenes lazy
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
      window.scrollTo(0, 0);
      document.querySelectorAll('.cb-reveal').forEach(e => e.classList.add('cb-visible'));
    });
    await page.waitForTimeout(1500);
    const tag = p.replace(/[^a-z0-9]+/gi, '_') || 'home';
    await page.screenshot({ path: `${SP}/shots/${vp.name}${tag}.png`, fullPage: true });
    const info = await page.evaluate(() => ({
      title: document.title, lang: document.documentElement.lang,
      liquidErr: (document.body.innerText.match(/Liquid error[^\n]*/g) || []).slice(0, 5),
      overflowX: document.documentElement.scrollWidth > window.innerWidth ? document.documentElement.scrollWidth : 0,
      h: document.body.scrollHeight,
      fontH: getComputedStyle(document.querySelector('.cb-h1, .cb-h2, h1') || document.body).fontFamily,
      themeId: (window.Shopify && Shopify.theme && Shopify.theme.id) || null,
    }));
    console.log(vp.name, p, JSON.stringify(info));
  }
  if (errors.length) console.log('ERRORES', vp.name, JSON.stringify([...new Set(errors)].slice(0, 15), null, 1));
  await ctx.close();
}
await browser.close();
