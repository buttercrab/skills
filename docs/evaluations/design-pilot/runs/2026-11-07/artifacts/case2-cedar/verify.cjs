const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes={};
function node(id){return nodes[id]??=( {value:'',hidden:false,disabled:false,textContent:'',attrs:{},handlers:{},addEventListener(type,cb){this.handlers[type]=cb},setAttribute(k,v){this.attrs[k]=v},focus(){focused=id}})}
let focused='',chosen=null;
const workshops=[{value:'Handbuilding',dataset:{price:'45',schedule:'Saturday · 10:00'}},{value:'Glazing',dataset:{price:'35',schedule:'Sunday · 14:00'}}];
const form=node('#booking-form');
form.querySelector=selector=>selector.endsWith(':checked')?chosen:{focus(){focused='first workshop'}};
form.reset=()=>{chosen=null;node('#seats').value='1'};
node('#seats').value='1';
Object.defineProperty(node('#seats'),'validity',{get(){const n=Number(this.value);return {valid:this.value!==''&&Number.isFinite(n)&&Number.isInteger(n)&&n>=1&&n<=4}}});
const document={querySelector:node};
vm.runInNewContext(script,{document});
const change=()=>form.handlers.change();
assert.equal(node('#book').disabled,true);assert.equal(node('#total').textContent,'$0');
for(const workshop of workshops){chosen=workshop;for(const count of ['1','2','3','4']){node('#seats').value=count;change();assert.equal(node('#book').disabled,false);assert.equal(node('#total').textContent,'$'+Number(workshop.dataset.price)*Number(count));}}
for(const invalid of ['','0','-1','5','1.5','NaN']){node('#seats').value=invalid;node('#seats').handlers.input();assert.equal(node('#book').disabled,true);assert.equal(node('#seats-error').hidden,false);assert.equal(node('#seats').attrs['aria-invalid'],'true');assert.equal(node('#total').textContent,'—');}
chosen=workshops[1];node('#seats').value='3';change();assert.equal(node('#seats-error').hidden,true);
form.handlers.submit({preventDefault(){}});assert.equal(form.hidden,true);assert.equal(node('#confirmation').hidden,false);assert.equal(node('#confirmed-workshop').textContent,'Glazing');assert.equal(node('#confirmed-seats').textContent,3);assert.equal(node('#confirmed-total').textContent,'$105');assert.equal(focused,'#success-heading');
node('#restart').handlers.click();assert.equal(form.hidden,false);assert.equal(node('#confirmation').hidden,true);assert.equal(chosen,null);assert.equal(node('#seats').value,'1');assert.equal(node('#total').textContent,'$0');assert.equal(node('#book').disabled,true);assert.equal(focused,'first workshop');
console.log('PASS: initial state; both workshops × 1–4 seats; six invalid values; correction; confirmation; reset and focus calls.');
console.log('Limitation: DOM harness uses mocked elements and number validity, not a rendered browser.');
assert(!/<(?:link|img|iframe)\b|\bfetch\s*\(|XMLHttpRequest|https?:\/\//i.test(html));
console.log('PASS: standalone source has no external assets or network API references.');
