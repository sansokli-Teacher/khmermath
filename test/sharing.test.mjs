import test from 'node:test';
import assert from 'node:assert/strict';
import { makeEnv } from './d1shim.mjs';
import { ensureColumns, _resetSchemaForTests } from '../src/lib/schema.js';
import { createSessionCookie } from '../src/lib/session.js';
import { accessibleTests, testAccess } from '../src/lib/access.js';
import { listTests } from '../src/api/tests.js';
import { searchTeachers, setShare, removeShare } from '../src/api/admin.js';
import * as links from '../src/api/share-links.js';
async function setup() {
  const env = makeEnv(new URL('../schema.sql', import.meta.url).pathname);
  _resetSchemaForTests(); await ensureColumns(env); env.SESSION_SECRET = 'test-sharing';
  env.raw.exec(`INSERT INTO teachers(id,username,password_hash,role,plan,active) VALUES
    (1,'admin','x','owner','full',1),(2,'alice','x','teacher','full',1),(3,'bob','x','teacher','full',1),(4,'inactive','x','teacher','full',0);
    INSERT INTO tests(id,title,owner_id,is_sample) VALUES(1,'Admin sample',1,1),(2,'Alice private',2,0),(3,'Bob private',3,0);`);
  env.cookies = {};
  for (const username of ['admin','alice','bob']) env.cookies[username] = (await createSessionCookie({role:'teacher',username},env.SESSION_SECRET)).split(';')[0];
  return env;
}
async function call(fn, env, username, body, params = {}, query = '') {
  const req = new Request('https://test.local/api' + query, { method: body ? 'POST' : 'GET', headers: username ? { Cookie: env.cookies[username], 'Content-Type': 'application/json' } : {}, ...(body ? {body:JSON.stringify(body)} : {}) });
  const response = await fn(req,env,params);
  return {status:response.status, data:await response.json()};
}
test('test list and direct access require ownership or explicit sharing even for admins and samples', async()=>{
 const env=await setup();
 for(const [id,username,role] of [[1,'admin','owner'],[2,'alice','teacher'],[3,'bob','teacher']]){
   assert.deepEqual([...(await accessibleTests(env,{id,role})).keys()],[id]);
   const listed=await call(listTests,env,username);
   assert.deepEqual(listed.data.tests.map(t=>t.id),[id]);
 }
 assert.equal(await testAccess(env,{id:1,role:'owner'},2),null);
 assert.equal(await testAccess(env,{id:2,role:'teacher'},1),null);
 await call(setShare,env,'alice',{type:'test',id:2,teacher_id:3,role:'reviewer'});
 assert.equal(await testAccess(env,{id:3,role:'teacher'},2),'reviewer');
 assert.equal((await call(listTests,env,'bob')).data.tests.length,2);
 await call(removeShare,env,'alice',{type:'test',id:2,teacher_id:3});
 assert.equal(await testAccess(env,{id:3,role:'teacher'},2),null);
});
test('teacher search returns no directory or partial/display-name matches',async()=>{
 const env=await setup();
 for(const query of ['', '?q=', '?q=bo', '?q=%25', '?q=inactive']) assert.deepEqual((await call(searchTeachers,env,'alice',null,{},query)).data.teachers,[]);
 assert.equal((await call(searchTeachers,env,'alice',null,{},'?q=BOB')).data.teachers[0].username,'bob');
 assert.equal((await call(searchTeachers,env,null,null,{},'?q=bob')).status,401);
});
test('link requires login and explicit acceptance, grants role once, and is owner-only',async()=>{
 const env=await setup();
 assert.equal((await call(links.create,env,'bob',{test_id:2})).status,404);
 assert.equal((await call(links.create,env,'admin',{test_id:2})).status,404);
 const created=await call(links.create,env,'alice',{test_id:2,role:'reviewer'});
 assert.equal(created.status,200); const params={token:created.data.token};
 assert.equal((await call(links.info,env,null,null,params)).status,401);
 assert.equal((await call(links.info,env,'bob',null,params)).data.title,'Alice private');
 assert.equal(await testAccess(env,{id:3,role:'teacher'},2),null);
 assert.equal((await call(links.accept,env,'bob',{},params)).status,200);
 assert.equal(await testAccess(env,{id:3,role:'teacher'},2),'reviewer');
 assert.equal((await call(links.accept,env,'admin',{},params)).status,404);
 assert.equal((await call(links.accept,env,'bob',{},params)).status,404);
});
test('revoked, expired and owner-deactivated links cannot grant access',async()=>{
 const env=await setup();
 const create=async()=> (await call(links.create,env,'alice',{test_id:2,role:'editor'})).data.token;
 const revoked=await create(); const id=env.raw.prepare('SELECT id FROM test_share_links').get().id;
 assert.equal((await call(links.revoke,env,'bob',{}, {id})).status,404);
 assert.equal((await call(links.revoke,env,'alice',{}, {id})).status,200);
 assert.equal((await call(links.accept,env,'bob',{}, {token:revoked})).status,404);
 const expired=await create(); env.raw.exec("UPDATE test_share_links SET expires_at='2000-01-01'");
 assert.equal((await call(links.accept,env,'bob',{}, {token:expired})).status,404);
 const inactive=await create();env.raw.exec('UPDATE teachers SET active=0 WHERE id=2');
 assert.equal((await call(links.accept,env,'bob',{}, {token:inactive})).status,404);
 assert.equal(await testAccess(env,{id:3,role:'teacher'},2),null);
});
