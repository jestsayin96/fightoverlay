#!/usr/bin/env node
/* Does the overlay actually still work?
 *
 * A syntax check is not enough. On 2026-11-06 a bad edit left `col` and `w`
 * undefined in lineGoal; the file parsed, every sprite still walked about,
 * and a screenshot looked fine - but nobody ever reached an opponent, so
 * nothing died. The frame loop wraps step() in a try/catch on purpose, so
 * a live stream never hard-crashes, which also means a fatal bug reports
 * zero page errors. That build was committed and pushed.
 *
 * The cheapest proof the thing works is that monsters die. Run this before
 * committing anything that touches movement, pairing, goals or rendering.
 *
 *   node tools/verify.js            # 30s, exits non-zero on failure
 *   node tools/verify.js --seconds 60
 */
const path = require('path');
const { chromium } = require('playwright');

const arg = (k, d) => { const i = process.argv.indexOf(k);
                        return i > -1 ? Number(process.argv[i+1]) : d; };
const SECONDS = arg('--seconds', 30);
const FILE = 'file://' + path.resolve(__dirname, '..', 'index.html');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const pageErrors = [];
  page.on('pageerror', e => pageErrors.push(e.message));

  await page.goto(FILE);
  await page.waitForTimeout(2500);

  const booted = await page.evaluate(() => typeof V !== 'undefined' && !!document.querySelector('canvas'));
  if (!booted) { console.error('FAIL  overlay did not boot'); await browser.close(); process.exit(1); }

  await page.evaluate(() => {
    const s = document.getElementById('setup'); if (s) s.style.display = 'none';
    for (let i = 0; i < 12; i++) joinHero('verify' + i);
  });

  const r = await page.evaluate(sec => new Promise(res => {
    let frames = 0, fighting = 0, ents = 0;
    const iv = setInterval(() => {
      frames++;
      const live = V.ents.filter(e => e.alive && !e.isBoss);
      ents += live.length;
      for (const e of live) if (e.state === 'fight' || e.swing > 0) fighting++;
    }, 16);
    let raf = 0; const t0 = performance.now();
    const tick = () => { raf++; if (performance.now() - t0 < sec * 1000) requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
    setTimeout(() => { clearInterval(iv); res({
      slain: V.slain,
      fightingPct: +(100 * fighting / Math.max(1, ents)).toFixed(1),
      fps: +(raf / sec).toFixed(1),
      entities: V.ents.length,
      jvErr: window.__jvErr || null }); }, sec * 1000);
  }), SECONDS);

  // Everything here has actually been wrong at least once.
  const checks = [
    ['no internal error',   !r.jvErr,            r.jvErr || 'none'],
    ['no page errors',      pageErrors.length===0, pageErrors[0] || 'none'],
    ['monsters die',        r.slain > 0,         r.slain + ' slain'],
    ['fighters engage',     r.fightingPct > 15,  r.fightingPct + '%'],
    ['frame rate holds',    r.fps >= 45,         r.fps + ' fps'],
    ['entities populated',  r.entities > 5,      r.entities + ' entities'],
  ];
  let ok = true;
  for (const [name, pass, detail] of checks){
    console.log((pass ? 'ok   ' : 'FAIL ') + name.padEnd(22) + detail);
    if (!pass) ok = false;
  }
  await browser.close();
  console.log(ok ? '\nVERIFY PASSED' : '\nVERIFY FAILED');
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error('verify crashed:', e.message); process.exit(1); });
