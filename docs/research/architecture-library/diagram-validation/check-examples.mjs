import fs from 'node:fs';
import path from 'node:path';
import {JSDOM} from 'jsdom';
const dom=new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window=dom.window;
globalThis.document=dom.window.document;
const {default:mermaid}=await import('./node_modules/mermaid/dist/mermaid.esm.mjs');
const root='/Users/jaeyong/skills/skills/system-architecture';
const files=[path.join(root,'references/diagram-contract.md'),...fs.readdirSync(path.join(root,'library/entries')).filter(n=>n.startsWith('diagram-')).map(n=>path.join(root,'library/entries',n))];
mermaid.initialize({startOnLoad:false,securityLevel:'strict'});
const results=[];
for(const file of files){
 const text=fs.readFileSync(file,'utf8');let example=0;
 for(const match of text.matchAll(/```mermaid\r?\n([\s\S]*?)```/g)){
  example++;
  try{const parsed=await mermaid.parse(match[1]);if(!parsed)throw new Error('Parser returned false');results.push({file:path.relative(root,file),example,result:'syntax-valid',diagramType:parsed.diagramType});}
  catch(error){results.push({file:path.relative(root,file),example,result:'parse-failed',message:String(error.message)});}
 }
}
const version=JSON.parse(fs.readFileSync(new URL('./node_modules/mermaid/package.json',import.meta.url),'utf8')).version;
const record={mermaid_version:version,dom_version:JSON.parse(fs.readFileSync(new URL('./node_modules/jsdom/package.json',import.meta.url),'utf8')).version,mode:'parse-only with DOM sanitization support; no rendering or architectural validation',results};
fs.writeFileSync('/private/tmp/architecture-diagram-examples-results.json',JSON.stringify(record,null,2)+'\n');console.log(JSON.stringify(record,null,2));dom.window.close();
if(!results.length||results.some(r=>r.result!=='syntax-valid'))process.exitCode=1;
