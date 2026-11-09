// Local logic checks using a minimal DOM stand-in; no rendering or native events.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(__dirname + '/index.html', 'utf8');
const nodes = new Map();
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.listeners = {}; this.attrs = {}; this.value = ''; }
  set id(value) { this._id = value; nodes.set(value, this); }
  get id() { return this._id; }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children = children; }
  setAttribute(name, value) { this.attrs[name] = value; }
  removeAttribute(name) { delete this.attrs[name]; }
  addEventListener(name, fn) { this.listeners[name] = fn; }
  focus() { focused = this; }
  dispatch(name) { this.listeners[name]?.({preventDefault() {}}); }
}
let focused;
for (const match of html.matchAll(/<([a-z]+)[^>]*\bid="([^"]+)"/g)) { const element = new Element(match[1]); element.id = match[2]; }
nodes.get('item').value = 'Clay'; nodes.get('quantity').value = '1';
const context = vm.createContext({document:{getElementById:id => nodes.get(id),createElement:tag => new Element(tag)}});
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script); vm.runInContext(script, context);
const run = text => vm.runInContext(text, context);
for (const value of ['', '0', '-1', '21', '1.5', 'abc', 'Infinity']) {
  nodes.get('quantity').value = value; nodes.get('request-form').dispatch('submit');
  assert.equal(run('records.length'), 0); assert.equal(nodes.get('quantity').value, value);
  assert.equal(nodes.get('quantity').attrs['aria-invalid'], 'true'); assert.equal(focused, nodes.get('quantity'));
}
for (const value of ['1','20']) assert.equal(run(`validQuantity('${value}')`), true);
nodes.get('quantity').value = '7'; nodes.get('request-form').dispatch('submit');
assert.equal(run('records[0].status'), 'pending');
assert.match(nodes.get('confirmation').children[1].textContent, /No materials are reserved/);
run("setDecision(1, 'declined')");
assert.equal(run('records[0].status'), 'declined');
let revision = nodes.get('request-1').children.at(-1);
nodes.get('revise-1').value = '2.5'; nodes.get('revise-1').dispatch('input'); revision.dispatch('submit');
assert.equal(run('records[0].status'), 'declined'); assert.equal(nodes.get('revise-1').attrs['aria-invalid'], 'true');
// Another request being submitted must preserve the revision draft.
nodes.get('quantity').value = '20'; nodes.get('request-form').dispatch('submit');
assert.equal(nodes.get('revise-1').value, '2.5');
revision = nodes.get('request-1').children.at(-1);
nodes.get('revise-1').value = '3'; nodes.get('revise-1').dispatch('input'); revision.dispatch('submit');
assert.equal(run('records.find(r=>r.id===1).status'), 'pending');
assert.equal(run('records.find(r=>r.id===1).quantity'), 3);
assert.equal(run('records.length'), 2);
run("setDecision(1, 'approved')");
assert.equal(run('records.find(r=>r.id===1).status'), 'approved');
run("setDecision(1, 'declined')");
assert.equal(run('records.find(r=>r.id===1).status'), 'approved');
assert.match(nodes.get('confirmation').children[1].textContent, /No real reservation/);
assert.equal(focused, nodes.get('request-1'));
assert.ok(!/(?:<script[^>]*src=|<link[^>]*href=|fetch\(|XMLHttpRequest)/.test(html));
console.log('PASS: script syntax; invalid quantities preserve input and focus errors; 1/20 bounds; pending confirmation; decline/revise/resubmit; draft preservation; approve guard; local-only source. DOM stand-in only; native events and rendering unobserved.');
