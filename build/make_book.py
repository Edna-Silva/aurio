import os
D = r"c:\Users\yamme\Downloads\AURIO"
src = open(os.path.join(D, "old.html"), encoding="utf8").read()
head_fonts = src[src.index('<link href'):src.index('<style>')]
art = src[src.index("const O='#111'"):src.index("const main=")]
modal_css = src[src.index(".letterbtn{"):src.index("@media(max-width:720px)")]
modal_html = src[src.index('<div class="modal"'):src.index("<footer>")]
modal_html = modal_html.replace('class="letterbtn" id="openLetter"', 'class="letterbtn" id="openLetter" style="display:none"')

CSS = r"""
:root{--g:#19e36b;--gd:#0b7a3d;--ink:#0d0d0d;--gold:#ffcf3a;--pw:min(45vw,calc((100vh - 150px)*.75),540px)}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;background:radial-gradient(circle at 50% 30%,#0f3a22,#040b07 70%) #06100b;color:#fff;font-family:'Comic Neue','Comic Sans MS',sans-serif;display:flex;flex-direction:column;align-items:center;overflow-x:hidden}
.top{text-align:center;padding:14px 10px 4px}
.top h1{font-family:Bangers,Impact;margin:0;font-size:clamp(26px,4vw,44px);color:var(--gold);letter-spacing:3px;text-shadow:3px 3px 0 #000,0 0 24px var(--g)}
.stage{flex:1;display:flex;align-items:center;justify-content:center;width:100%;padding:10px 0 4px;perspective:2600px}
.book{position:relative;width:calc(var(--pw)*2);height:calc(var(--pw)/.75);transform-style:preserve-3d;transition:transform .9s cubic-bezier(.4,.1,.2,1);filter:drop-shadow(0 30px 40px #000a)}
.leaf{position:absolute;left:50%;top:0;width:50%;height:100%;transform-origin:left center;transform-style:preserve-3d;transition:transform 1.05s cubic-bezier(.45,.05,.2,1)}
.leaf.flipped{transform:rotateY(-180deg)}
.face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;overflow:hidden}
.face.back{transform:rotateY(180deg)}
.page{background:#f7efd6;color:#241a10;padding:calc(var(--pw)/40);display:flex;flex-direction:column;gap:calc(var(--pw)/60);
 background-image:radial-gradient(#0000000d 1px,transparent 1.5px),linear-gradient(90deg,#00000000 70%,#0000001f);background-size:7px 7px,100% 100%}
.face.back.page{background-image:radial-gradient(#0000000d 1px,transparent 1.5px),linear-gradient(270deg,#00000000 70%,#0000001f)}
.right-edge{box-shadow:inset -6px 0 0 #e9dcb4,inset -9px 0 0 #cdbd90}
.left-edge{box-shadow:inset 6px 0 0 #e9dcb4,inset 9px 0 0 #cdbd90}
.hd{display:flex;align-items:center;gap:8px;font-family:Bangers,Impact;letter-spacing:1.5px;color:var(--gd);font-size:calc(var(--pw)/17)}
.hd .n{background:var(--gold);color:#000;border:3px solid #000;padding:0 9px;font-size:calc(var(--pw)/19);transform:rotate(-3deg);box-shadow:2px 2px 0 #000}
.hd .t{flex:1;line-height:1;text-shadow:2px 2px 0 #0001}
.hd button{font-size:calc(var(--pw)/26);padding:2px 10px}
button{font-family:Bangers,Impact;letter-spacing:1px;border:3px solid #000;background:var(--g);color:#000;padding:5px 14px;border-radius:6px;cursor:pointer;box-shadow:3px 3px 0 #000;font-size:18px}
button:active{transform:translate(2px,2px);box-shadow:1px 1px 0 #000}
button:disabled{opacity:.35;cursor:default}button.off{background:#666;color:#ddd}
.rowp{display:flex;gap:calc(var(--pw)/60);flex:1;min-height:0}
.panel{position:relative;flex:1;min-width:0;min-height:0;background:#222;border:4px solid var(--ink);overflow:hidden;box-shadow:3px 3px 0 #0006}
.panel svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.panel::after{content:"";position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(#0003 1.1px,transparent 1.5px);background-size:6px 6px;mix-blend-mode:multiply}
.cap{position:absolute;z-index:3;background:#ffe45c;color:#000;border:2px solid #000;padding:4px 7px;font-weight:700;font-size:calc(var(--pw)/34)!important;line-height:1.22;max-width:84%!important;box-shadow:2px 2px 0 #000}
.cap.tl{top:6px;left:6px}.cap.tr{top:6px;right:6px}.cap.bl{bottom:6px;left:6px}.cap.br{bottom:6px;right:6px}.cap.bc{bottom:6px;left:50%;transform:translateX(-50%);text-align:center}
.cap.dark{background:#04180d;color:#d6ffe6;border-color:var(--g)}.cap.gold{background:var(--gold)}
.bub{position:absolute;z-index:4;background:#fff;color:#000;border:3px solid #000;border-radius:50%/60%;padding:5px 14px;font-family:Bangers,Impact;font-size:calc(var(--pw)/17)!important;box-shadow:2px 2px 0 #000;white-space:nowrap}
.sfx{position:absolute;z-index:4;font-family:Bangers,Impact;font-size:calc(var(--pw)/7)!important;color:var(--gold);-webkit-text-stroke:2px #000;text-shadow:3px 3px 0 #000;transform:rotate(-8deg);letter-spacing:2px}
.sfx[style*="translateX(-50%)"]{font-size:calc(var(--pw)/10)!important}
.sfx[style*="white-space"]{white-space:normal!important;text-align:center;width:90%;left:5%!important;font-size:calc(var(--pw)/13)!important;transform:rotate(-2deg)!important;line-height:.95}
.bub{white-space:normal!important;max-width:75%;text-align:center;font-size:calc(var(--pw)/22)!important;line-height:1}
.page #rep{font-size:calc(var(--pw)/28)!important;width:88%!important;top:16%!important}
.page #rep em{width:36%!important}.page #rep b{width:34%!important}
.say{font-size:calc(var(--pw)/31);line-height:1.28;background:#fff8;border-left:5px solid var(--gd);padding:5px 9px;font-weight:700;font-style:italic}
.pn{text-align:center;font-family:Bangers;font-size:calc(var(--pw)/32);color:#7a6a48;letter-spacing:2px}
.cover{width:100%;height:100%;background:radial-gradient(circle at 50% 38%,#145a33,#06220f 75%);border:calc(var(--pw)/60) solid #3a2410;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:calc(var(--pw)/30);padding:calc(var(--pw)/14);text-align:center;cursor:pointer;box-shadow:inset 0 0 0 calc(var(--pw)/70) var(--gold),inset 0 0 70px #000}
.cover h2{font-family:Bangers,Impact;margin:0;font-size:calc(var(--pw)/7.2);line-height:.95;color:var(--gold);letter-spacing:3px;text-shadow:4px 4px 0 #000,0 0 26px var(--g)}
.cover p{margin:0;font-weight:700;color:#bfffd8;font-size:calc(var(--pw)/26)}
.cover .hint{font-family:Bangers;letter-spacing:2px;color:#fff;animation:bl 1.3s infinite;font-size:calc(var(--pw)/22)}
@keyframes bl{50%{opacity:.25}}
.endcover{background:linear-gradient(120deg,#06220f,#0d3d22);border:calc(var(--pw)/60) solid #3a2410;display:flex;align-items:center;justify-content:center;font-family:Bangers;color:var(--gold);font-size:calc(var(--pw)/9);letter-spacing:3px;text-shadow:3px 3px 0 #000;box-shadow:inset 0 0 0 calc(var(--pw)/70) var(--gold),inset 0 0 70px #000}
.endcover{flex-direction:column;gap:calc(var(--pw)/22);overflow:hidden}
.endwrap{cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:calc(var(--pw)/40);width:100%;position:relative;height:calc(var(--pw)*.62)}
.endring{width:calc(var(--pw)*.46);height:calc(var(--pw)*.46);object-fit:contain;filter:drop-shadow(0 0 22px #19e36b) drop-shadow(0 8px 10px #000);animation:floaty 2.2s ease-in-out infinite;position:absolute;left:50%;top:0;margin-left:calc(var(--pw)*-.23)}
.endwrap:hover .endring{filter:drop-shadow(0 0 34px #6dff95) drop-shadow(0 8px 10px #000)}
.endclick{position:absolute;bottom:0;font-family:Bangers,Impact;font-size:calc(var(--pw)/14);letter-spacing:3px;color:#fff;text-shadow:3px 3px 0 #000,0 0 18px var(--g);animation:bl 1.3s infinite}
@keyframes floaty{50%{transform:translateY(calc(var(--pw)*-.03)) rotate(3deg)}}
@keyframes roll{0%{transform:translateX(0) rotate(0)}100%{transform:translateX(calc(var(--pw)*.62)) rotate(900deg)}}
.endwrap.roll .endring{animation:roll 1.7s cubic-bezier(.5,0,.8,.6) forwards}
.endwrap.roll .endclick{opacity:0;animation:none}
.toc{display:flex;flex-direction:column;gap:calc(var(--pw)/70);margin-top:4px}
.toc button{text-align:left;background:#fff9;font-size:calc(var(--pw)/24);padding:3px 10px;box-shadow:2px 2px 0 #000;color:#111}
.toc button:hover{background:var(--g)}
.intro-t{font-family:Bangers;font-size:calc(var(--pw)/9);color:var(--gd);line-height:1;text-shadow:3px 3px 0 var(--gold)}
.intro-p{font-size:calc(var(--pw)/29);font-weight:700;margin:4px 0}
.ctrl{display:flex;gap:10px;align-items:center;justify-content:center;padding:6px 8px 14px;flex-wrap:wrap}
.ctrl .info{font-family:Bangers;letter-spacing:2px;color:#bfffd8;min-width:110px;text-align:center}
@media(max-width:860px){
 :root{--pw:min(92vw,520px)}
 .stage{perspective:none;display:block}
 .book{width:var(--pw);height:auto;margin:0 auto;transform:none!important;transition:none;filter:none}
 .leaf{position:relative;left:0;width:100%;height:auto;transform:none!important}
 .face{position:relative;inset:auto;transform:none!important;backface-visibility:visible;height:calc(var(--pw)/.75);margin-bottom:14px;border:3px solid #000}
 .ctrl .nav{display:none}
}
"""

JS = r"""
const pageDefs=[{intro:1},{ch:0,r:[[0]],say:1},{ch:1,r:[[0],[1]],say:1},{ch:2,r:[[0],[1]],say:1},{ch:3,r:[[0,1,2]],say:1},{ch:4,r:[[0],[1]]},{ch:4,r:[[2],[3]],cont:1,say:1},{ch:5,r:[[0],[1,2]],say:1},{ch:6,r:[[0],[1]],say:1},{ch:7,r:[[0]]},{ch:8,r:[[0],[1]],say:1},{ch:9,r:[[0]],say:1,letter:1}];
function pageHTML(p,i){
 if(p.intro) return `<div class="intro-t">Para o Aurio</div><p class="intro-p">Uma história de origem, contada com a seriedade de uma grande lenda... e uma pitada de sarcasmo.</p><div class="toc">${CH.map((c,k)=>`<button data-ch="${k}">${k+1}. ${c.t}</button>`).join('')}</div><div class="pn">${i}</div>`;
 const c=CH[p.ch];
 const hd=`<div class="hd"><span class="n">${p.ch+1}</span><span class="t">${c.t}${p.cont?' (cont.)':''}</span></div>`;
 const rows=p.r.map(r=>`<div class="rowp">${r.map(j=>c.html[j]).join('')}</div>`).join('');
 const say=p.say&&c.say?`<div class="say">${c.say}</div>`:'';
 const letter=p.letter?`<button id="openLetter2" style="align-self:center;font-size:calc(var(--pw)/14);padding:6px 24px;background:var(--gold);animation:pulse 1.6s infinite">✉ ABRIR CARTA</button>`:'';
 return hd+rows+say+letter+`<div class="pn">${i}</div>`;
}
const cover=`<div class="cover" id="cover"><svg viewBox="0 0 100 100" style="width:42%"><circle cx="50" cy="50" r="42" fill="#0b2a18" stroke="#ffcf3a" stroke-width="5"/><circle cx="50" cy="50" r="30" fill="#19e36b" stroke="#000" stroke-width="3"/><circle cx="50" cy="50" r="19" fill="#0b2a18" stroke="#ffcf3a" stroke-width="3"/><circle cx="50" cy="50" r="9" fill="#eafff1"/></svg><h2>O LIVRO<br>DAS LENDAS</h2><p>A origem do Guardião da Luz Esmeralda<br>21 de dezembro</p><div class="hint">▶ CLIQUE PARA ABRIR</div></div>`;
const N=7,leaves=[];
const pg=(i,side)=>`<div class="face ${side==='back'?'back ':''}page ${i%2?'right-edge':'left-edge'}">${pageHTML(pageDefs[i],i)}</div>`;
for(let k=0;k<N;k++){
 const front=k===0?`<div class="face">${cover}</div>`:pg(2*k-1,'front');
 const back=k===N-1?`<div class="face back endcover"><div>FIM</div><div class="endwrap" id="endwrap"><img class="endring" src="${RING_URI}" alt="Anel"><div class="endclick">CLIQUE AQUI</div></div></div>`:pg(2*k,'back');
 leaves.push(`<div class="leaf">${front}${back}</div>`);
}
const book=document.getElementById('book');book.innerHTML=leaves.join('');
let idx=0;const lv=[...document.querySelectorAll('.leaf')];
const info=document.getElementById('info');
function render(){
 lv.forEach((l,k)=>{l.classList.toggle('flipped',k<idx);l.style.zIndex=k<idx?k+1:N-k});
 book.style.transform=window.innerWidth<=860?'':`translateX(${idx===0?-25:idx===N?25:0}%)`;
 document.getElementById('prev').disabled=idx===0;document.getElementById('next').disabled=idx===N;
 info.textContent=idx===0?'Capa':idx===N?'Fim':'Páginas '+(2*idx-2)+'–'+(2*idx-1);
}
function go(n){idx=Math.max(0,Math.min(N,n));render()}
document.getElementById('prev').onclick=()=>go(idx-1);document.getElementById('next').onclick=()=>go(idx+1);
document.getElementById('cover').onclick=()=>go(1);
const bgm=new Audio('audio/theme.mp3');bgm.loop=true;bgm.volume=.6;
const mb=document.getElementById('music');let userStopped=false;
const sync=()=>{mb.textContent=bgm.paused?'🎵 Música: PARADA — tocar':'🔊 Música a tocar — parar';mb.classList.toggle('off',bgm.paused)};
const tryPlay=()=>{if(userStopped)return;bgm.play().then(sync).catch(()=>{})};
mb.onclick=()=>{if(bgm.paused){userStopped=false;bgm.play().then(sync).catch(()=>{})}else{userStopped=true;bgm.pause()}sync()};
bgm.onplay=sync;bgm.onpause=sync;sync();tryPlay();
const firstGesture=e=>{if(e.target.closest&&e.target.closest('#music'))return;tryPlay();if(!bgm.paused)['pointerdown','keydown','touchstart'].forEach(ev=>removeEventListener(ev,firstGesture,true))};
['pointerdown','keydown','touchstart'].forEach(ev=>addEventListener(ev,firstGesture,true));
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(idx+1);if(e.key==='ArrowLeft')go(idx-1)});
document.querySelectorAll('.toc button').forEach(b=>b.onclick=()=>{const ch=+b.dataset.ch;const pi=pageDefs.findIndex(p=>!p.intro&&!p.cont&&p.ch===ch);go(Math.floor(pi/2)+1)});
render();
const mo=document.getElementById('modal');
const ew=document.getElementById('endwrap');
const openL=()=>mo.classList.add('open'),closeL=()=>{mo.classList.remove('open');if(ew)ew.classList.remove('roll')};
if(ew)ew.onclick=()=>{if(ew.classList.contains('roll'))return;ew.classList.add('roll');setTimeout(openL,1750)};
document.getElementById('openLetter2').onclick=openL;document.getElementById('closeLetter').onclick=closeL;
mo.onclick=e=>{if(e.target===mo)closeL()};document.addEventListener('keydown',e=>{if(e.key==='Escape')closeL()});
if(location.hash.startsWith('#p')){go(+location.hash.slice(2));}
"""

html = ('<!doctype html>\n<html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>O Livro das Lendas — Aurio (livro)</title>\n' + head_fonts + '<style>' + CSS + modal_css + '</style></head><body>\n'
        '<div class="top"><h1>O LIVRO DAS LENDAS</h1></div>\n<div class="stage"><div class="book" id="book"></div></div>\n'
        '<div class="ctrl"><button class="nav" id="prev">◀ Anterior</button><span class="info" id="info"></span><button class="nav" id="next">Seguinte ▶</button><button id="music">🎵 Música</button></div>\n'
        + modal_html + '\n<script>\n' + art + JS + '\n</script></body></html>')
open(os.path.join(D, "index.html"), "w", encoding="utf8").write(html)
print(len(html))
