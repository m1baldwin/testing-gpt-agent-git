// Optional browser check. Start server.py before running this script.
const assert = require('node:assert/strict');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    for (const reducedMotion of ['no-preference', 'reduce']) {
      const page = await browser.newPage({ reducedMotion });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto('http://127.0.0.1:8000/');
      const button = page.getByRole('button', { name: 'Play hello world' });
      assert.equal(await page.getByRole('heading').textContent(), 'hello world');
      const greeting = page.getByRole('heading');
      const originalColor = await greeting.evaluate(el => getComputedStyle(el).color);
      for (let replay = 0; replay < 2; replay++) {
        // Pause the real animation at its midpoint to inspect it without timing races.
        await page.evaluate(() => {
          document.querySelector('#play').click();
          const animation = document.querySelector('h1').getAnimations()[0];
          animation.pause();
          animation.currentTime = animation.effect.getTiming().duration / 2;
        });
        assert.equal(await button.isDisabled(), true);
        assert.equal(await page.getByRole('status').textContent(), 'Saying hello...');
        const visual = await page.locator('h1').evaluate(el => ({
          transform: getComputedStyle(el).transform,
          opacity: Number(getComputedStyle(el).opacity),
          color: getComputedStyle(el).color
        }));
        assert.equal(visual.color, 'rgb(24, 128, 56)');
        if (reducedMotion === 'reduce') {
          assert.equal(visual.transform, 'none');
          assert.ok(visual.opacity > 0.5 && visual.opacity < 1);
        } else {
          assert.notEqual(visual.transform, 'none');
        }
        await page.locator('h1').evaluate(el => el.getAnimations()[0].play());
        await page.waitForFunction(() => !document.querySelector('#play').disabled);
        assert.match(await page.getByRole('status').textContent(), /Hello again!/);
        assert.equal(await greeting.evaluate(el => getComputedStyle(el).color), originalColor);
      }
      assert.deepEqual(errors, []);
      await page.close();
      console.log(`PASS: click, motion, completion and replay (${reducedMotion})`);
    }
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
