const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const elements={};
function el(id){return elements[id]||=( {id,textContent:'',innerHTML:'',attrs:{},handlers:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.handlers[k]=f},focus(){},querySelector(){return {focus(){}}}})}
const ctx={document:{getElementById:el}};
vm.createContext(ctx);vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],ctx);
const cards=el('cards');
function clickSave(id){cards.handlers.click({target:{closest(selector){if(selector==='[data-id]')return {dataset:{id:String(id)}};return null}}})}
function filter(id){el(id).handlers.click()}
assert.equal((cards.innerHTML.match(/<article>/g)||[]).length,3);
for(const [title,time] of [['The city after rain',12],['Learning to notice',18],['A garden at midnight',9]]){assert(cards.innerHTML.includes(title));assert(cards.innerHTML.includes(`${time} min read`))}
filter('saved');assert(cards.innerHTML.includes('No saved reads yet.'));assert(cards.innerHTML.includes('Browse all reads'));assert.equal(el('saved').attrs['aria-pressed'],'true');
cards.handlers.click({target:{closest(selector){return selector==='#browse'?{}:null}}});assert.equal((cards.innerHTML.match(/<article>/g)||[]).length,3);
clickSave(1);assert.equal(el('saved-count').textContent,1);assert(cards.innerHTML.includes('Unsave'));assert(el('notice').textContent.includes('added to'));
filter('saved');assert.equal((cards.innerHTML.match(/<article>/g)||[]).length,1);assert(cards.innerHTML.includes('The city after rain'));assert(!cards.innerHTML.includes('Learning to notice'));
clickSave(1);assert.equal(el('saved-count').textContent,0);assert(cards.innerHTML.includes('No saved reads yet.'));assert(el('notice').textContent.includes('removed from'));
filter('all');clickSave(2);clickSave(3);filter('saved');assert.equal((cards.innerHTML.match(/<article>/g)||[]).length,2);assert.equal(el('saved-count').textContent,2);
assert(!/<(?:link|img|iframe)[^>]*(?:src|href)=["']https?:/i.test(html));assert(!/(?:fetch\(|XMLHttpRequest|@import|url\(https?:)/i.test(html));
console.log('PASS: initial 3 titles/times; empty saved state; browse recovery; save; filter; unsave last item; multiple saved items; selected filter state; live notice; no external assets/requests.');
console.log('LIMIT: VM with minimal DOM stubs checks state transitions, not browser rendering/layout.');
