/**
 * Extract the upstream Linear A corpus into JSON.
 *
 * The upstream file is a JavaScript `Map` literal, not JSON, so it must be
 * evaluated rather than parsed. It is run inside a `vm` sandbox so that nothing
 * it contains can touch this process.
 *
 * `translatedWords` is dropped here: those are Linear B-derived semantic
 * glosses, which are interpretation rather than data. See docs/PROCEDURE.md.
 *
 * @file
 * @see docs/PROCEDURE.md
 */

/* eslint-env node */

const fs = require('fs');
const vm = require('vm');

const src = fs.readFileSync('raw_repo/LinearAInscriptions.js', 'utf-8');

/**
 * The sandbox the upstream file is evaluated in. It defines a global named
 * `inscriptions`, which is why that property is not declared in this file and
 * cannot be resolved statically.
 *
 * @type {{inscriptions?: Map<string, Object>}}
 */
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(src, sandbox);

/** @type {Map<string, Object>} */
const map = sandbox.inscriptions;
const out = [];
for (const val of map.values()) {
  // Strip translatedWords deliberately - held out for later cross-check only
  const { translatedWords, ...clean } = val;
  out.push(clean);
}
fs.writeFileSync('data/inscriptions_clean.json', JSON.stringify(out, null, 1));
console.log('Extracted', out.length, 'entries.');
console.log('Fields in first entry:', Object.keys(out[0]));
