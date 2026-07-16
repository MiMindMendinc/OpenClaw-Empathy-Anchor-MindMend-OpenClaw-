import puppeteer from 'puppeteer-core';
import { copyFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const outDir = join(root, 'docs', 'assets');
const artifactDir = '/opt/cursor/artifacts/screenshots';
mkdirSync(outDir, { recursive: true });
mkdirSync(artifactDir, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || '/usr/local/bin/google-chrome',
  headless: 'new',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--window-size=1440,1100'],
  defaultViewport: { width: 1440, height: 960, deviceScaleFactor: 1 },
});

async function save(page, name) {
  const dest = join(outDir, name);
  const artifact = join(artifactDir, name);
  await page.screenshot({ path: dest, fullPage: false });
  copyFileSync(dest, artifact);
  console.log('Wrote', name);
}

const page = await browser.newPage();

// 1) Hero
await page.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle0' });
await page.waitForSelector('.brand-title');
await new Promise((r) => setTimeout(r, 800));
await save(page, '01-showcase-hero.png');

// 2) Live crisis demo
await page.setViewport({ width: 1440, height: 1100, deviceScaleFactor: 1 });
await page.evaluate(() => {
  document.getElementById('live').scrollIntoView({ behavior: 'instant', block: 'start' });
});
await page.select('#scenario', 'crisis');
await page.click('#runDemo');
await page.waitForFunction(
  () => document.getElementById('connStatus')?.textContent?.includes('Alert persisted')
    || document.getElementById('connStatus')?.textContent?.includes('Scan complete'),
  { timeout: 10000 },
);
await new Promise((r) => setTimeout(r, 600));
await save(page, '02-live-demo-crisis.png');

// 3) All /demo scenarios
await page.click('#runAll');
await page.waitForFunction(
  () => document.getElementById('connStatus')?.textContent?.includes('/demo'),
  { timeout: 10000 },
);
await new Promise((r) => setTimeout(r, 600));
await save(page, '03-demo-all-scenarios.png');

// 4) Status JSON — render into a clean page for readability
const status = await (await fetch('http://127.0.0.1:8000/status')).json();
const statusHtml = `<!doctype html><html><head><meta charset="utf-8"><title>/status</title>
<style>
  body{margin:0;background:#07251f;color:#e7f2ec;font:16px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace}
  header{padding:28px 36px 8px;font:700 28px/1.1 Fraunces,Georgia,serif;color:#f0b27a}
  pre{padding:12px 36px 40px;white-space:pre-wrap}
</style></head><body>
<header>GET /status — runtime evidence</header>
<pre>${JSON.stringify(status, null, 2)}</pre>
</body></html>`;
const statusPath = join(outDir, '_status-temp.html');
writeFileSync(statusPath, statusHtml);
await page.setViewport({ width: 1200, height: 900, deviceScaleFactor: 1 });
await page.goto(`file://${statusPath}`, { waitUntil: 'networkidle0' });
await save(page, '04-status-json.png');

// 5) Boundaries placard section
await page.setViewport({ width: 1440, height: 960, deviceScaleFactor: 1 });
await page.goto('http://127.0.0.1:8000/#boundaries', { waitUntil: 'networkidle0' });
await page.evaluate(() => {
  document.getElementById('boundaries').scrollIntoView({ behavior: 'instant', block: 'start' });
  document.querySelectorAll('[data-reveal]').forEach((el) => el.classList.add('visible'));
});
await new Promise((r) => setTimeout(r, 500));
await save(page, '05-boundaries-placards.png');

await browser.close();
console.log('All screenshots captured.');
