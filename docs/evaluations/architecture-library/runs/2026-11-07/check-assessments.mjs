import fs from 'node:fs';
import path from 'node:path';
import {JSDOM} from 'jsdom';
const dom=new JSDOM('<!doctype html><html><body></body></html>');globalThis.window=dom.window;globalThis.document=dom.window.document;
const {default:mermaid}=await import('./node_modules/mermaid/dist/mermaid.esm.mjs');mermaid.initialize({startOnLoad:false,securityLevel:'strict'});
const root='/Users/jaeyong/skills/docs/evaluations/architecture-library/runs/2026-11-07/assessments';const results=[];
for(const name of fs.readdirSync(root).sort()){
 const file=path.join(root,name,'diagrams.md');let example=0;
 for(const match of fs.readFileSync(file,'utf8').matchAll(/^```mermaid[ \t]*\r?\n([\s\S]*?)^```/gm)){
  example++;
  try{const parsed=await mermaid.parse(match[1]);if(!parsed)throw new Error('Parser returned false');results.push({case:name,diagram:example,result:'syntax-valid',diagramType:parsed.diagramType});}
  catch(error){results.push({case:name,diagram:example,result:'parse-failed',message:String(error.message)});}
 }
 if(!example)results.push({case:name,result:'no-mermaid-blocks; syntax unassessed'});
}
const record={parser:'Mermaid 12.3.0',dom:'JSDOM31.0.0',mode:'Syntax parsing only of frozen outputs; no rendering, semantic or operational acceptance',results};fs.writeFileSync('/private/tmp/architecture-assessment-diagram-results.json',JSON.stringify(record,null,2)+'\n');console.log(JSON.stringify(record,null,2));dom.window.close();if(results.some(r=>r.result==='parse-failed'))process.exitCode=1;
