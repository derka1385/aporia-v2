import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync,readFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {runStudy,studyPlan} from '../server/study.mjs';

test('bounded studies resume without repeating completed cases and reject changed model identity',async()=>{
  const directory=mkdtempSync(join(tmpdir(),'aporia-study-'));let calls=0,modelDigest='first';
  const provider={models:async()=>[{name:'fixture',digest:modelDigest}],generate:async()=>{calls++;return {data:{hypothesis:'Psychological continuity is a provisional identity criterion.',premises:['Continuity links psychological states.'],assumptions:['Continuity is unique.'],stance:'conditional',confidence:.6},usage:{input:20,output:30}}}};
  const cases=[31,73].map(seed=>({question:'Is psychological continuity sufficient for personal identity?',condition:'baseline',delta:0,seed,model:'fixture',profiles:['explorer'],budget:8}));
  try{
    const first=await runStudy({cases,provider,directory,maxCases:1});assert.equal(first.recordedCases,1);assert.equal(calls,1);
    const second=await runStudy({cases,provider,directory,maxCases:1});assert.equal(second.recordedCases,2);assert.equal(calls,2);
    await runStudy({cases,provider,directory});assert.equal(calls,2);
    assert.ok(JSON.parse(readFileSync(join(directory,'case-001.json'))).protocol.initialStateDigest);
    modelDigest='changed';await assert.rejects(runStudy({cases,provider,directory}),/identity changed/);assert.equal(calls,2);
  }finally{rmSync(directory,{recursive:true});}
});
test('comparison plans pair questions and seeds across conditions with fresh memory',()=>{
  const plan=studyPlan({suite:'compare'});assert.equal(plan.length,8);assert.equal(new Set(plan.map(c=>c.seed)).size,2);assert.ok(plan.every(c=>c.memoryMode==='fresh'&&c.budget===8));
  for(const seed of [31,73])assert.deepEqual(plan.filter(c=>c.seed===seed).map(c=>[c.condition,c.delta]),[['baseline',0],['prompt',1],['architecture',0],['architecture',1]]);
});
