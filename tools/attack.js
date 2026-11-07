/* Adversarial suite: run it before letting anyone else near the overlay.
   node tools/attack.js
   Attacks chat input, the economy, storage, and load. Every check that
   fires here once fired for real. */
const {chromium}=require('playwright');
const F='file://'+process.cwd()+'/index.html';
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const findings=[];
const bad=(t,d)=>{ findings.push(t+" :: "+d); console.log("  BROKEN  "+t+" :: "+d); };
const ok =(t)=>console.log("  ok      "+t);

(async()=>{
  const b=await chromium.launch();

  /* ---------- 1. XSS via the channel URL parameter ---------- */
  {
    const pg=await b.newPage();
    let alerted=false; pg.on('dialog',async d=>{alerted=true; await d.dismiss();});
    await pg.goto(F+'?channel=%3Cimg%20src%3Dx%20onerror%3D%22window.__pwn%3D1%22%3E',{waitUntil:'load'});
    await pg.waitForTimeout(3000);
    // actually exercise the line that writes the channel into innerHTML
    await pg.evaluate(()=>{ try{ stat("Connected to #"+CFG.channel+" - live."); }catch(e){} });
    await pg.waitForTimeout(600);
    const pwn = await pg.evaluate(()=>window.__pwn===1 ||
      !!document.querySelector('#status img') ||
      /<img/i.test(document.getElementById("status").innerHTML));
    pwn ? bad("XSS via ?channel=","HTML from the URL executes in the status line")
        : ok("XSS via ?channel=");
    await pg.close();
  }

  /* ---------- 2. economy: negative and absurd numbers ---------- */
  {
    const pg=await b.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
    await pg.goto(F+'?channel=test',{waitUntil:'load'}); await pg.waitForTimeout(3000);
    const r = await pg.evaluate(()=>{
      Game.chat("Alice","hi"); Game.chat("Bob","hi");
      const A=Save.get("Alice"), B=Save.get("Bob");
      A.coins=100; B.coins=100;
      const out={};
      Game.chat("Alice","!vgive Bob -5000");      out.giveNeg   ={A:A.coins,B:B.coins};
      A.coins=100; B.coins=100;
      Game.chat("Alice","!vgive Bob 99999999");   out.giveOver  ={A:A.coins,B:B.coins};
      A.coins=100;
      Game.chat("Alice","!vslots -100000");       out.slotsNeg  = A.coins;
      A.coins=100;
      Game.chat("Alice","!vslots 1e308");         out.slotsHuge = A.coins;
      A.coins=100; B.coins=100;
      Game.chat("Alice","!vduel Bob -9999");      out.duelNeg   ={A:A.coins,B:B.coins};
      A.coins=0;
      Game.chat("Alice","!vbuy crown");           out.buyBroke  ={coins:A.coins, owned:[...A.owned]};
      A.coins=1000; A.owned=[];
      Game.chat("Alice","!vbuy crown"); Game.chat("Alice","!vbuy crown");
      out.buyTwice ={coins:A.coins, owned:[...A.owned]};
      return out;
    });
    const neg = r.giveNeg.A > 100 || r.giveNeg.B < 0;
    neg ? bad("!vgive negative","coins created or drained: "+JSON.stringify(r.giveNeg)) : ok("!vgive negative");
    r.giveOver.B > 100000000 ? bad("!vgive overflow",JSON.stringify(r.giveOver)) : ok("!vgive overflow");
    /* A negative wager is clamped to the 5-coin minimum, so coins CAN go up -
       that is a legitimate win, not an exploit. What matters is that the
       clamp holds: the only reachable outcomes at the minimum stake are
       -5, +5 and +25. An earlier version of this check called a normal win
       a bug. */
    ([-5,5,25].includes(r.slotsNeg-100))
      ? ok("!vslots negative bet (clamped to minimum stake)")
      : bad("!vslots negative bet","outcome outside a 5-coin stake: "+(r.slotsNeg-100));
    (!isFinite(r.slotsHuge) || r.slotsHuge > 1e9) ? bad("!vslots huge bet",String(r.slotsHuge)) : ok("!vslots huge bet");
    (r.duelNeg.A>100||r.duelNeg.B>100) ? bad("!vduel negative stake",JSON.stringify(r.duelNeg)) : ok("!vduel negative stake");
    r.buyBroke.owned.length ? bad("!vbuy with 0 coins","got the item anyway") : ok("!vbuy with 0 coins");
    r.buyTwice.coins < 940 ? bad("!vbuy twice","charged twice for one item: "+JSON.stringify(r.buyTwice)) : ok("!vbuy twice");
    if(errs.length) bad("economy errors",errs.join(" | "));
    await pg.close();
  }

  /* ---------- 3. absurd command arguments ---------- */
  {
    const pg=await b.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
    await pg.goto(F+'?channel=test',{waitUntil:'load'}); await pg.waitForTimeout(3000);
    await pg.evaluate(()=>{
      Game.chat("Fuzz","hi");
      const junk=["!roll 99999d99999","!roll -5d-5","!roll 1e9d1e9","!shoot 1e400",
                  "!vslots abc","!vgive","!vgive  ","!vbuy","!vbuy \u0000",
                  "!hug","!attack","!attack Fuzz","!color notacolor",
                  "!color javascript:alert(1)","!avatar notaclass","!roll 0d0",
                  "!vduel Fuzz 10","!8ball","!shoot -999","!mass notathing"];
      for(const j of junk) Game.chat("Fuzz",j);
    });
    await pg.waitForTimeout(2500);
    const st = await pg.evaluate(()=>({err:window.__jvErr||null, ents:V.ents.length,
                                       fps:V.ents.every(e=>isFinite(e.x)&&isFinite(e.y))}));
    if(errs.length) bad("junk args throw",errs.slice(0,2).join(" | ")); else ok("junk args");
    if(st.err) bad("junk args internal error",st.err);
    if(!st.fps) bad("junk args","an entity has a non-finite position");
    await pg.close();
  }

  /* ---------- 4. hostile names ---------- */
  {
    const pg=await b.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
    await pg.goto(F+'?channel=test',{waitUntil:'load'}); await pg.waitForTimeout(3000);
    await pg.evaluate(()=>{
      const names=["<img src=x onerror=alert(1)>", "a".repeat(5000),
                   "‮reversed", "\u0000\u0001\u0002", "😀".repeat(200),
                   "", " ", "\n\n\n", "​".repeat(100), "𝕴𝖓𝖘𝖆𝖓𝖊",
                   "'; DROP TABLE--", "{{7*7}}", "../../etc/passwd"];
      for(const n of names){ try{ Game.chat(n,"hello"); }catch(e){ window.__nameThrew=e.message; } }
    });
    await pg.waitForTimeout(3000);
    const r = await pg.evaluate(()=>({
      threw: window.__nameThrew||null, err: window.__jvErr||null,
      ents: V.ents.length,
      injected: !!document.querySelector('#rows img, #hdr img, #status img')
    }));
    r.threw   ? bad("hostile names throw", r.threw) : ok("hostile names");
    r.injected? bad("hostile names","HTML injected into the page") : ok("hostile names no injection");
    if(r.err) bad("hostile names internal", r.err);
    if(errs.length) bad("hostile names pageerror", errs.slice(0,2).join(" | "));
    await pg.close();
  }

  /* ---------- 5. corrupt and oversized storage ---------- */
  {
    const pg=await b.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
    await pg.goto(F+'?channel=test',{waitUntil:'load'});
    await pg.evaluate(()=>{ localStorage.setItem("jv-save-v1:test","{not json at all"); });
    await pg.reload({waitUntil:'load'}); await pg.waitForTimeout(3000);
    let r = await pg.evaluate(()=>({err:window.__jvErr||null, ents:V.ents.length}));
    r.err ? bad("corrupt save", r.err) : ok("corrupt save survived");
    await pg.evaluate(()=>{ localStorage.setItem("jv-save-v1:test",
        JSON.stringify({x:{name:"x",coins:"notanumber",level:null,owned:"nope",msgs:{}}})); });
    await pg.reload({waitUntil:'load'}); await pg.waitForTimeout(3000);
    await pg.evaluate(()=>{ try{ Game.chat("x","hi"); Game.chat("x","!vbuy crown");
      Game.chat("x","!vshop"); }catch(e){ window.__storeThrew=e.message; } });
    await pg.waitForTimeout(1500);
    r = await pg.evaluate(()=>({err:window.__jvErr||null, threw:window.__storeThrew||null}));
    (r.err||r.threw) ? bad("save with wrong types", r.err||r.threw)
                     : ok("save with wrong types survived");
    if(errs.length) bad("storage pageerror", errs.slice(0,2).join(" | "));
    await pg.close();
  }

  /* ---------- 6. chat flood ---------- */
  {
    const pg=await b.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
    await pg.goto(F+'?channel=test',{waitUntil:'load'}); await pg.waitForTimeout(3000);
    const t0=Date.now();
    await pg.evaluate(()=>{ for(let i=0;i<3000;i++) Game.chat("flood"+(i%300),"msg "+i); });
    const took=Date.now()-t0;
    await sleep(6000);
    const r = await pg.evaluate(()=>({err:window.__jvErr||null, ents:V.ents.length,
      heap: performance.memory? Math.round(performance.memory.usedJSHeapSize/1048576):0}));
    if(r.err) bad("3000 messages", r.err);
    else if(r.ents > 200) bad("3000 messages","entity count ran away: "+r.ents);
    else ok("3000 messages from 300 people  ("+took+"ms, "+r.ents+" entities, "+r.heap+"MB)");
    if(errs.length) bad("flood pageerror", errs.slice(0,2).join(" | "));
    await pg.close();
  }

  /* ---------- 7. everything at once ---------- */
  {
    const pg=await b.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
    await pg.goto(F+'?channel=test',{waitUntil:'load'}); await pg.waitForTimeout(3000);
    await pg.evaluate(()=>{
      for(let i=0;i<40;i++) Game.chat("v"+i,"hi");
      Game.chat("v1","!royale"); for(let i=0;i<40;i++) Game.chat("v"+i,"!join");
      Game.chat("test","!megaboss");
      Game.chat("v2","!basketball"); for(let i=0;i<40;i++) Game.chat("v"+i,"!shoot 5");
      for(let i=0;i<20;i++) Game.redeem("whale","Summon the Boss");
      for(let i=0;i<30;i++) Game.redeem("whale","Spawn a Monster");
      Game.chat("v3","!lounge"); Game.chat("v3","!war"); Game.chat("v3","!lounge");
    });
    await sleep(12000);
    const r = await pg.evaluate(()=>({err:window.__jvErr||null, ents:V.ents.length,
      finite: V.ents.every(e=>isFinite(e.x)&&isFinite(e.y)&&isFinite(e.hp))}));
    if(r.err) bad("everything at once", r.err);
    else if(!r.finite) bad("everything at once","an entity has NaN position or hp");
    else ok("everything at once  ("+r.ents+" entities, all finite)");
    if(errs.length) bad("chaos pageerror", errs.slice(0,2).join(" | "));
    await pg.close();
  }

  console.log("\n================ "+(findings.length? findings.length+" PROBLEMS" : "nothing broke")+" ================");
  findings.forEach(f=>console.log(" - "+f));
  await b.close();
})();
