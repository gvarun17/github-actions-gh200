// Run: npm test  (uses Node's built-in test runner, no extra deps)
const { test } = require('node:test');
const assert = require('node:assert');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

function runAction(env) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'greet-'));
  const files = ['GITHUB_OUTPUT', 'GITHUB_STATE', 'GITHUB_STEP_SUMMARY'];
  files.forEach((f) => fs.writeFileSync(path.join(dir, f), ''));
  let code = 0;
  let stdout = '';
  try {
    stdout = execFileSync(process.execPath, [path.join(__dirname, '..', 'dist', 'index.js')], {
      env: { ...process.env, ...env, ...Object.fromEntries(files.map((f) => [f, path.join(dir, f)])) },
      encoding: 'utf8',
    });
  } catch (err) {
    code = err.status;
    stdout = err.stdout;
  }
  const output = fs.readFileSync(path.join(dir, 'GITHUB_OUTPUT'), 'utf8');
  return { code, stdout, output };
}

test('greets and sets outputs', () => {
  const r = runAction({ INPUT_WHO: 'Varun', INPUT_SHOUT: 'false' });
  assert.strictEqual(r.code, 0);
  assert.match(r.stdout, /Hello, Varun/);
  assert.match(r.output, /greeting<<.*\nHello, Varun/s);
  assert.match(r.output, /time<</);
});

test('shout upper-cases', () => {
  const r = runAction({ INPUT_WHO: 'Varun', INPUT_SHOUT: 'true' });
  assert.match(r.stdout, /HELLO, VARUN/);
});

test('rejects unsafe input', () => {
  const r = runAction({ INPUT_WHO: 'x"; rm -rf /', INPUT_SHOUT: 'false' });
  assert.strictEqual(r.code, 1);
  assert.match(r.stdout, /::error::Input 'who' has invalid characters/);
});
