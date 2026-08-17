import puppeteer from 'puppeteer-core';
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
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
  try {
    copyFileSync(dest, artifact);
  } catch {
    // Artifact directory is optional outside the capture environment.
  }
  console.log('Wrote', name);
}

async function waitForConnected(page) {
  await page.waitForFunction(
    () => document.getElementById('connStatus')?.textContent?.includes('Connected'),
    { timeout: 15000 },
  );
}

async function runScenario(page, value) {
  await page.select('#scenario', value);
  await page.click('#runDemo');
  await page.waitForFunction(
    () => {
      const text = document.getElementById('connStatus')?.textContent || '';
      return text.includes('Alert persisted') || text.includes('Scan complete') || text.includes('Geofence');
    },
    { timeout: 15000 },
  );
}

const page = await browser.newPage();
await page.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle0' });
await page.waitForSelector('h1');
await waitForConnected(page);
await new Promise((r) => setTimeout(r, 400));
await save(page, '01-showcase-hero.png');

await page.evaluate(() => {
  document.getElementById('live').scrollIntoView({ behavior: 'instant', block: 'start' });
});
await runScenario(page, 'distress');
await new Promise((r) => setTimeout(r, 400));
await save(page, '02-live-demo-distress.png');

await runScenario(page, 'crisis');
await new Promise((r) => setTimeout(r, 400));
await save(page, '03-live-demo-crisis.png');

await page.goto('http://127.0.0.1:8000/#boundaries', { waitUntil: 'networkidle0' });
await page.evaluate(() => {
  document.getElementById('boundaries').scrollIntoView({ behavior: 'instant', block: 'start' });
});
await new Promise((r) => setTimeout(r, 400));
await save(page, '05-boundaries-placards.png');

await page.setViewport({ width: 375, height: 812, deviceScaleFactor: 2 });
await page.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle0' });
await waitForConnected(page);
await new Promise((r) => setTimeout(r, 300));
await save(page, '06-mobile-375-hero.png');

await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
await page.evaluate(() => {
  document.getElementById('live').scrollIntoView({ behavior: 'instant', block: 'start' });
});
await runScenario(page, 'distress');
await new Promise((r) => setTimeout(r, 400));
await save(page, '07-mobile-390-results.png');

await browser.close();
console.log('All screenshots captured.');
