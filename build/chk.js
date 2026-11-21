
const O='#111';let uid=0;
const rng=s=>()=>((s=Math.imul(s^s>>>15,s|1),s^=s+Math.imul(s^s>>>7,s|61),(s^s>>>14)>>>0)/4294967296);
const svg=(inner,vb='0 0 800 500')=>`<svg viewBox="${vb}" preserveAspectRatio="xMidYMid slice">${inner}</svg>`;
const rad=(id,c,o=1)=>`<radialGradient id="${id}"><stop offset="0" stop-color="${c}" stop-opacity="${o}"/><stop offset="1" stop-color="${c}" stop-opacity="0"/></radialGradient>`;
const stars=(n,seed,w=800,h=500)=>{const r=rng(seed);let s='';for(let i=0;i<n;i++)s+=`<circle cx="${r()*w}" cy="${r()*h}" r="${.6+r()*1.8}" fill="#fff" opacity="${.4+r()*.6}"/>`;return s};
const burst=(cx,cy,r1,r2,n,fill,seed=1,stroke=O)=>{const r=rng(seed);let p=[];for(let i=0;i<n*2;i++){const a=i*Math.PI/n,rr=i%2?r1:r2*(.8+r()*.4);p.push((cx+Math.cos(a)*rr).toFixed(1)+','+(cy+Math.sin(a)*rr).toFixed(1))}return `<polygon points="${p.join(' ')}" fill="${fill}" stroke="${stroke}" stroke-width="4" stroke-linejoin="round"/>`};
const rays=(cx,cy,n,len,col,op=.18,seed=2)=>{const r=rng(seed);let s='';for(let i=0;i<n;i++){const a=r()*6.283,w=.03+r()*.05;s+=`<polygon points="${cx},${cy} ${cx+Math.cos(a-w)*len},${cy+Math.sin(a-w)*len} ${cx+Math.cos(a+w)*len},${cy+Math.sin(a+w)*len}" fill="${col}" opacity="${op}"/>`}return s};
const skyline=(seed,base,minH,maxH,fill,lit,win,w=800,wrecked=false)=>{const r=rng(seed);let s='',x=-20;while(x<w){const bw=50+r()*80,bh=minH+r()*(maxH-minH),y=base-bh;s+=`<rect x="${x}" y="${y}" width="${bw}" height="${bh+4}" fill="${fill}" stroke="${O}" stroke-width="3"/>`;if(wrecked&&r()<.4)s+=`<polygon points="${x+bw*.3},${y} ${x+bw*.8},${y} ${x+bw*.55},${y+34}" fill="#2a1c26" stroke="${O}" stroke-width="3"/>`;for(let wx=x+8;wx<x+bw-12;wx+=16)for(let wy=y+10;wy<base-10;wy+=22)if(r()<lit)s+=`<rect x="${wx}" y="${wy}" width="8" height="12" fill="${win}"/>`;if(r()<.35)s+=`<rect x="${x+bw/2-2}" y="${y-30}" width="4" height="30" fill="${O}"/>`;x+=bw+r()*8}return s};
const planet=(cx,cy,r,col='#14506a')=>{const i='pl'+(uid++);return `<defs>${rad(i,'#19e36b',.7)}</defs><circle cx="${cx}" cy="${cy}" r="${r*1.35}" fill="url(#${i})"/><circle cx="${cx}" cy="${cy}" r="${r}" fill="${col}" stroke="${O}" stroke-width="5"/><ellipse cx="${cx-r*.3}" cy="${cy+r*.1}" rx="${r*.45}" ry="${r*.14}" fill="#1f8a63" opacity=".7"/><ellipse cx="${cx+r*.25}" cy="${cy-r*.35}" rx="${r*.3}" ry="${r*.1}" fill="#1f8a63" opacity=".7"/><path d="M${cx+r*.2} ${cy-r} A${r} ${r} 0 1 0 ${cx+r*.2} ${cy+r} A${r*.82} ${r} 0 0 1 ${cx+r*.2} ${cy-r}Z" fill="#000" opacity=".45"/>`};

function hero(x,y,s=1,o={}){const{suit=true,mouth='smirk',shades=false,age='adult',flip=false,head=false,rot=0}=o;
 const body=suit?'#1fae5a':(age==='kid'?'#e08a2c':'#4a5aa0'),sk=age==='kid'?'#8a5a40':'#7a4e36';
 const beard=age==='adult'?`<path d="M-62 -6 Q-66 70 0 86 Q66 70 62 -6 Q50 30 30 38 Q0 30 -30 38 Q-50 30 -62 -6Z" fill="#171210"/>`:'';
 const hair=age==='kid'?`<path d="M-62 -24 Q-70 -96 0 -98 Q70 -96 62 -24 Q40 -64 0 -62 Q-40 -64 -62 -24Z" fill="#171210"/>`+[-44,-15,15,44].map(h=>`<circle cx="${h}" cy="-92" r="18" fill="#171210"/>`).join(''):`<path d="M-64 -20 Q-68 -94 0 -98 Q68 -94 64 -20 Q50 -64 0 -62 Q-50 -64 -64 -20Z" fill="#171210"/>`;
 const eyes=shades?`<rect x="-50" y="-34" width="44" height="26" rx="7" fill="#0b0b10"/><rect x="6" y="-34" width="44" height="26" rx="7" fill="#0b0b10"/><path d="M-6 -24 H6" stroke="#0b0b10" stroke-width="6"/><path d="M-42 -29 L-30 -29 M14 -29 L26 -29" stroke="#7dffb0" stroke-width="3"/>`:
 [-24,24].map((e,i)=>`<ellipse cx="${e}" cy="-20" rx="13" ry="10" fill="#fff"/><circle cx="${e+3}" cy="-19" r="6.5" fill="#150d08" stroke="none"/><circle cx="${e+5}" cy="-21" r="2" fill="#fff" stroke="none"/><path d="M${e-15} ${i?-42:-38} L${e+15} ${i?-48:-37}" stroke="#171210" stroke-width="6"/>`).join('');
 const mouths={smirk:`<path d="M-16 52 Q6 64 26 44" fill="none" stroke="#f3dccf" stroke-width="5"/><path d="M26 44 l7 -8" stroke="#f3dccf" stroke-width="5"/>`,smile:`<path d="M-22 46 Q0 74 22 46Z" fill="#fff"/>`,open:`<ellipse cx="0" cy="52" rx="20" ry="16" fill="#5a1418"/><ellipse cx="0" cy="60" rx="11" ry="6" fill="#d9606e" stroke="none"/>`,flat:`<path d="M-16 52 H16" stroke="#f3dccf" stroke-width="5"/>`};
 const bodySvg=head?'':`<path d="M-175 210 L-152 124 Q-120 88 -50 80 L50 80 Q120 88 152 124 L175 210Z" fill="${body}"/><path d="M-175 210 L-152 124 Q-132 104 -100 94 L-108 210Z" fill="#0b6a35" stroke="none"/><rect x="-26" y="40" width="52" height="46" fill="#5d3a28"/>`+(suit?`<path d="M-44 84 L0 124 L44 84" fill="none" stroke="#0b6a35" stroke-width="10"/><circle cx="0" cy="158" r="24" fill="#f4f1dc"/><circle cx="0" cy="158" r="14" fill="#17d36a"/><circle cx="0" cy="158" r="5" fill="#eafff1" stroke="none"/>`:'');
 return `<g transform="translate(${x},${y}) rotate(${rot}) scale(${flip?-s:s},${s})" stroke="${O}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">${bodySvg}<ellipse cx="-62" cy="-4" rx="11" ry="17" fill="#664230"/><ellipse cx="62" cy="-4" rx="11" ry="17" fill="#664230"/><ellipse cx="0" cy="-10" rx="63" ry="78" fill="${sk}"/>${hair}${beard}${eyes}<path d="M-6 6 L0 -4 L8 6Z" fill="#5d3a28" stroke-width="3"/>${mouths[mouth]}</g>`}
function baby(x,y,s=1){return `<g transform="translate(${x},${y}) scale(${s})" stroke="${O}" stroke-width="4" stroke-linejoin="round"><ellipse cx="0" cy="130" rx="170" ry="110" fill="#f0f0f8"/><path d="M-120 110 Q0 60 120 110" fill="none" stroke="#c9cbe0" stroke-width="5"/><ellipse cx="0" cy="0" rx="100" ry="96" fill="#8a5a40"/><path d="M-60 -70 Q0 -110 60 -70 Q30 -86 0 -84 Q-30 -86 -60 -70Z" fill="#171210"/><path d="M-60 -14 Q-42 -34 -22 -14" fill="none" stroke="#171210" stroke-width="7"/><path d="M22 -14 Q42 -34 60 -14" fill="none" stroke="#171210" stroke-width="7"/><path d="M-50 0 Q-60 40 -46 70 Q-36 40 -40 4Z" fill="#7cc7ff"/><path d="M50 0 Q60 40 46 70 Q36 40 40 4Z" fill="#7cc7ff"/><ellipse cx="-62" cy="34" rx="16" ry="10" fill="#d97d6c" stroke="none"/><ellipse cx="62" cy="34" rx="16" ry="10" fill="#d97d6c" stroke="none"/><ellipse cx="0" cy="46" rx="28" ry="24" fill="#5a1418"/><ellipse cx="0" cy="58" rx="16" ry="9" fill="#d9606e" stroke="none"/></g>`}
const flyer=(x,y,s=1,rot=-12)=>`<g transform="translate(${x},${y}) rotate(${rot}) scale(${s})" stroke="${O}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"><path d="M-40 10 L-230 36 L-226 62 L-30 44Z" fill="#0f7a3f"/><path d="M-40 -8 L-236 -14 L-238 14 L-30 22Z" fill="#1fae5a"/><path d="M-80 -30 Q20 -50 100 -34 L112 34 Q20 54 -80 40Z" fill="#1fae5a"/><path d="M-80 -30 L-80 40 L-50 38 L-50 -26Z" fill="#0b6a35" stroke="none"/><circle cx="20" cy="2" r="20" fill="#f4f1dc"/><circle cx="20" cy="2" r="12" fill="#17d36a"/><path d="M80 -30 L250 -70 L276 -40 L110 6Z" fill="#1fae5a"/><circle cx="284" cy="-58" r="34" fill="#7dffb0"/><circle cx="284" cy="-58" r="20" fill="#eafff1" stroke="none"/><circle cx="284" cy="-58" r="52" fill="none" stroke="#19e36b" stroke-width="7" opacity=".7"/></g><g transform="translate(${x} ${y}) rotate(${rot})">${hero(120*s,-2*s,.5*s,{head:true,rot:80})}</g>`;
const ring3d=(x,y,sc=1,rot=0)=>{const i='rg'+(uid++);return `<defs>
<linearGradient id="${i}b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a3d1c"/><stop offset=".35" stop-color="#2fe36f"/><stop offset=".55" stop-color="#0f8a3c"/><stop offset="1" stop-color="#042a12"/></linearGradient>
<linearGradient id="${i}d" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c5a28"/><stop offset="1" stop-color="#021a0b"/></linearGradient>
<linearGradient id="${i}t" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7dff9f"/><stop offset=".5" stop-color="#14b84e"/><stop offset="1" stop-color="#06501f"/></linearGradient>
<radialGradient id="${i}c" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffffe8"/><stop offset=".35" stop-color="#f4ff9a"/><stop offset=".7" stop-color="#5dff7c"/><stop offset="1" stop-color="#14b84e"/></radialGradient>
<radialGradient id="${i}g"><stop offset="0" stop-color="#19e36b" stop-opacity=".85"/><stop offset="1" stop-color="#19e36b" stop-opacity="0"/></radialGradient>
<filter id="${i}f"><feGaussianBlur stdDeviation="3"/></filter></defs>
<g transform="translate(${x} ${y}) rotate(${rot}) scale(${sc}) translate(-150 -150)">
<circle cx="150" cy="150" r="230" fill="url(#${i}g)"/>
<path d="M22 150 Q18 270 140 292 Q262 270 278 150 L248 150 Q246 236 150 252 Q54 236 52 150Z" fill="url(#${i}d)" stroke="#021208" stroke-width="3"/>
<path fill-rule="evenodd" d="M20 132 Q10 250 150 274 Q290 250 280 132 Q262 60 150 56 Q38 60 20 132Z M72 150 Q74 214 150 226 Q226 214 228 150 Q220 118 150 114 Q80 118 72 150Z" fill="url(#${i}b)" stroke="#021208" stroke-width="3"/>
<path d="M44 168 Q58 234 128 248" fill="none" stroke="#c9ffd9" stroke-width="9" stroke-linecap="round" opacity=".6" filter="url(#${i}f)"/>
<path d="M262 160 Q250 220 206 240" fill="none" stroke="#7dffb0" stroke-width="7" stroke-linecap="round" opacity=".45" filter="url(#${i}f)"/>
<path d="M88 202 Q110 226 160 230" fill="none" stroke="#9dffc0" stroke-width="6" stroke-linecap="round" opacity=".5" filter="url(#${i}f)"/>
<ellipse cx="150" cy="104" rx="122" ry="68" fill="url(#${i}t)" stroke="#021208" stroke-width="3"/>
<ellipse cx="150" cy="104" rx="112" ry="60" fill="none" stroke="#c9ffd9" stroke-width="2.5" opacity=".8"/>
<ellipse cx="150" cy="106" rx="96" ry="50" fill="url(#${i}d)" stroke="#031a0c" stroke-width="2"/>
<ellipse cx="150" cy="104" rx="90" ry="45" fill="#0f9a40" stroke="#6dff95" stroke-width="2"/>
<ellipse cx="150" cy="106" rx="54" ry="29" fill="none" stroke="#06491f" stroke-width="15"/>
<path d="M60 104 H98 M202 104 H240" stroke="#06491f" stroke-width="14" stroke-linecap="round"/>
<path d="M110 70 Q150 58 190 70" fill="none" stroke="#06491f" stroke-width="10" stroke-linecap="round"/>
<path d="M112 142 Q150 154 188 142" fill="none" stroke="#06491f" stroke-width="10" stroke-linecap="round"/>
<ellipse cx="150" cy="104" rx="40" ry="21" fill="url(#${i}c)"/>
<ellipse cx="150" cy="100" rx="58" ry="32" fill="url(#${i}g)"/>
<path d="M78 82 Q100 62 140 58" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".7" filter="url(#${i}f)"/>
<ellipse cx="136" cy="96" rx="14" ry="6" fill="#fff" opacity=".85"/>
</g>`};
const hand=(x,y,s=1)=>`<g transform="translate(${x},${y}) scale(${s})" stroke="${O}" stroke-width="5" stroke-linejoin="round"><path d="M-60 120 L-40 -20 Q-30 -60 10 -60 L80 -60 Q110 -50 100 -10 L90 120Z" fill="#7a4e36"/><rect x="-14" y="-110" width="30" height="70" rx="14" fill="#7a4e36"/><rect x="22" y="-120" width="30" height="80" rx="14" fill="#7a4e36"/><rect x="58" y="-110" width="28" height="70" rx="14" fill="#7a4e36"/><rect x="-46" y="-80" width="28" height="60" rx="14" fill="#7a4e36"/>${ring3d(30,-36,.3,-8)}</g>`;
const crowd=(seed,y,n,fill)=>{const r=rng(seed);let s='';for(let i=0;i<n;i++){const x=40+r()*720,h=.7+r()*.5;s+=`<g transform="translate(${x},${y}) scale(${h})" fill="${fill}" stroke="${O}" stroke-width="3"><circle cx="0" cy="-46" r="12"/><path d="M-16 0 L-12 -34 L12 -34 L16 0Z"/><path d="M-12 -30 L-34 -58 M12 -30 L34 -58" stroke="${O}" stroke-width="6" fill="none"/></g>`}return s};
const lamp=(x,y,c='#ffd66a')=>{const i='lp'+(uid++);return `<defs>${rad(i,c,.9)}</defs><circle cx="${x}" cy="${y}" r="90" fill="url(#${i})"/>`};

// ---------- panel art ----------
const A={
book(){const g='g'+uid++;const ids=uid++;
const sp=Array.from({length:46},(_,i)=>{const r=rng(i+9);return `<circle cx="${300+r()*340}" cy="${r()*330}" r="${1+r()*3.5}" fill="#b8ffd2" opacity="${.35+r()*.65}"/>`}).join('');
const puffs=Array.from({length:9},(_,i)=>`<circle cx="${440+Math.sin(i*1.7)*60+i*6}" cy="${230-i*24}" r="${28+i*7}" fill="#19e36b" opacity="${.20-i*.016}"/>`).join('');
const stripes=Array.from({length:6},(_,i)=>`<path d="M165 ${166+i*5} L605 ${131+i*5}" stroke="#bfae80" stroke-width="1.6"/>`).join('');
return svg(`<defs>${rad(g,'#19e36b',1)}<linearGradient id="t${ids}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#021208"/><stop offset="1" stop-color="#0a2a18"/></linearGradient><linearGradient id="cv${ids}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a4624"/><stop offset="1" stop-color="#4a2813"/></linearGradient></defs>
<rect width="800" height="500" fill="url(#t${ids})"/>
<ellipse cx="450" cy="440" rx="380" ry="58" fill="#000" opacity=".55"/>
${rays(462,227,26,640,'#19e36b',.2,5)}
<circle cx="462" cy="227" r="330" fill="url(#${g})" opacity=".85"/>
${puffs}
<g transform="translate(160 170)" stroke="${O}" stroke-width="6" stroke-linejoin="round">
<polygon points="0,0 165,150 165,206 0,56" fill="#3a2010"/><path d="M28 26 L28 82 M70 62 L70 118 M112 100 L112 156" stroke="#ffcf3a" stroke-width="7" fill="none"/>
<polygon points="440,-35 605,115 605,171 440,21" fill="#2d180c"/>
<polygon points="165,150 605,115 605,128 165,163" fill="#3a2010"/>
<polygon points="165,163 605,128 605,158 165,193" fill="#efe2b6"/>${stripes}
<polygon points="165,193 605,158 605,171 165,206" fill="#3a2010"/>
<g transform="matrix(1 -0.08 0.55 0.5 0 0)">
<rect x="0" y="0" width="440" height="300" rx="16" fill="url(#cv${ids})"/>
<rect x="20" y="20" width="400" height="260" rx="8" fill="none" stroke="#ffcf3a" stroke-width="9"/>
<rect x="36" y="36" width="368" height="228" rx="4" fill="none" stroke="#e0a82a" stroke-width="3"/>
${[[34,34],[406,34],[34,266],[406,266]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="17" fill="#ffcf3a"/><circle cx="${x}" cy="${y}" r="7" fill="#19e36b"/>`).join('')}
<circle cx="220" cy="150" r="82" fill="#2a1608" stroke="#ffcf3a" stroke-width="9"/>
<circle cx="220" cy="150" r="62" fill="#19e36b" stroke="${O}" stroke-width="5"/>
<circle cx="220" cy="150" r="44" fill="#0b2a18" stroke="#ffcf3a" stroke-width="6"/>
<circle cx="220" cy="150" r="22" fill="#eafff1" stroke="none"/>
<path d="M220 66 V90 M220 210 V234 M136 150 H160 M280 150 H304" stroke="#ffcf3a" stroke-width="9" stroke-linecap="round"/>
</g></g>
<circle cx="462" cy="227" r="52" fill="url(#${g})"/>${burst(462,227,22,70,12,'#c9ffdf',4,'none')}
${sp}`)},
city(){return svg(`<defs><linearGradient id="cg${uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b0f1f"/><stop offset=".7" stop-color="#6d2c34"/></linearGradient></defs><rect width="800" height="500" fill="url(#cg${uid})"/>${stars(35,3,800,200)}<circle cx="620" cy="110" r="46" fill="#c9a0a0" stroke="${O}" stroke-width="4" opacity=".7"/>${skyline(11,440,120,330,'#2a2136',.12,'#ffb15a',800,true)}${skyline(5,500,70,220,'#120e18',.2,'#ff8a3c',800,true)}${Array.from({length:60},(_,i)=>{const r=rng(i+40);const x=r()*800,y=r()*500;return `<line x1="${x}" y1="${y}" x2="${x-8}" y2="${y+30}" stroke="#bcd" stroke-width="1.5" opacity=".5"/>`}).join('')}`)},
crowd(){return svg(`<rect width="800" height="500" fill="#2a1520"/>${rays(400,500,18,700,'#ff5a3c',.12,8)}${skyline(31,380,100,260,'#1b1020',.1,'#ff9a50')}<rect y="400" width="800" height="100" fill="#120a12" stroke="${O}" stroke-width="4"/>${crowd(4,470,9,'#241624')}${burst(600,190,40,95,12,'#ff8a3c',3)}`)},
window(){const g='w'+uid++;return svg(`<defs>${rad(g,'#19e36b',.9)}</defs><rect width="800" height="500" fill="#5b3a32"/><rect x="0" y="380" width="800" height="120" fill="#7a5040" stroke="${O}" stroke-width="4"/>${lamp(130,150)}<rect x="250" y="40" width="300" height="300" fill="#071633" stroke="${O}" stroke-width="12"/>${stars(30,7,300,300).replace(/cx="([\d.]+)" cy="([\d.]+)"/g,(m,a,b)=>`cx="${250+ +a}" cy="${40+ +b}"`)}<path d="M400 40 V340 M250 190 H550" stroke="${O}" stroke-width="10"/><circle cx="470" cy="110" r="70" fill="url(#${g})"/>${burst(470,110,10,40,5,'#caffdd',2)}`)},
baby(){return svg(`<rect width="800" height="500" fill="#7a4f3a"/>${lamp(120,130)}${lamp(700,100,'#19e36b')}${rays(400,200,14,500,'#ffe9a8',.1,3)}${baby(400,260,1.7)}${burst(660,420,30,60,8,'#ffe45c',5)}`)},
grow(age,mouth,sh=false){return svg(`<defs><linearGradient id="gr${uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#143a5a"/><stop offset="1" stop-color="#0b5a44"/></linearGradient></defs><rect width="800" height="500" fill="url(#gr${uid})"/>${rays(400,260,16,560,'#19e36b',.12,age.length+2)}${hero(400,260,age==='kid'?1.35:1.5,{suit:false,age,mouth,shades:sh})}${stars(25,age.length,800,200)}`)},
ring(){return svg(`<rect width="800" height="500" fill="#020712"/>${stars(120,4)}${planet(650,130,86)}${rays(120,430,26,900,'#19e36b',.16,7)}${Array.from({length:9},(_,i)=>`<circle cx="${140+i*48}" cy="${430-i*24}" r="${40-i*3.5}" fill="#19e36b" opacity="${.05+i*.025}"/>`).join('')}${Array.from({length:7},(_,i)=>`<path d="M${60+i*10} ${440-i*14} H${380+i*10}" stroke="#7dffb0" stroke-width="3" opacity="${.15+i*.04}"/>`).join('')}${ring3d(520,235,1.05,-18)}${burst(520,235,70,150,12,'none',9,'#19e36b')}${Array.from({length:30},(_,i)=>{const r=rng(i+3);return `<circle cx="${r()*800}" cy="${r()*500}" r="${1+r()*2.5}" fill="#b8ffd2" opacity=".7"/>`}).join('')}`)},
ringhand(){const g='r'+uid++;return svg(`<defs>${rad(g,'#19e36b',1)}</defs><rect width="800" height="500" fill="#06150e"/>${rays(400,250,24,700,'#19e36b',.18,3)}<circle cx="470" cy="210" r="280" fill="url(#${g})"/>${hand(400,330,1.6)}${burst(468,260,40,100,14,'none',2,'#caffdd')}${stars(40,5)}`)},
suit(){return svg(`<rect width="800" height="500" fill="#031b10"/>${rays(400,230,30,700,'#19e36b',.2,6)}${burst(400,230,170,330,16,'#19e36b',3)}${burst(400,230,120,230,16,'#caffdd',4,'none')}${hero(400,300,1.55,{suit:true,mouth:'smirk'})}`)},
holo(){return svg(`<rect width="800" height="500" fill="#021a14"/>${stars(60,8)}<rect x="40" y="40" width="720" height="420" rx="16" fill="#0a4030" stroke="#19e36b" stroke-width="5" opacity=".95"/>${Array.from({length:50},(_,i)=>`<line x1="46" y1="${46+i*8}" x2="754" y2="${46+i*8}" stroke="#19e36b" opacity=".12"/>`).join('')}<g stroke="#19e36b" stroke-width="4" fill="none"><circle cx="640" cy="170" r="42"/><path d="M570 400 L585 230 Q640 215 695 230 L710 400"/></g>`)},
fly(){return svg(`<defs><linearGradient id="fl${uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a1c44"/><stop offset="1" stop-color="#1c6b6b"/></linearGradient></defs><rect width="800" height="500" fill="url(#fl${uid})"/>${stars(60,2,800,250)}${skyline(31,470,90,260,'#103550',.28,'#b6ffd0')}${skyline(32,520,60,170,'#071826',.3,'#7dffb0')}${Array.from({length:14},(_,i)=>`<path d="M${60-i*6} ${210+i*8} H${330-i*10}" stroke="#7dffb0" stroke-width="${3+i%3}" opacity=".5"/>`).join('')}${flyer(420,230,1)}`)},
shield(){const g='s'+uid++;return svg(`<defs>${rad(g,'#19e36b',.5)}</defs><rect width="800" height="500" fill="#2a1520"/>${rays(650,100,18,800,'#ff7a30',.14,6)}${skyline(41,420,90,230,'#2b1d30',.08,'#ff9a50')}${burst(690,140,50,140,14,'#ff9a30',8)}<rect y="410" width="800" height="90" fill="#150c14" stroke="${O}" stroke-width="4"/>${crowd(2,470,7,'#3a2a3a')}<circle cx="290" cy="360" r="210" fill="url(#${g})" stroke="#9dffc0" stroke-width="7"/><circle cx="290" cy="360" r="170" fill="none" stroke="#9dffc0" stroke-width="3" opacity=".6"/>${hero(520,250,.7,{suit:true,mouth:'flat'})}`)},
calma(){return svg(`<rect width="800" height="500" fill="#112a22"/>${rays(400,260,22,700,'#19e36b',.14,4)}${burst(400,230,200,350,18,'#1aa357',2)}${hero(400,310,1.5,{suit:true,mouth:'smirk',shades:false})}<g transform="translate(610,300) rotate(10)" stroke="${O}" stroke-width="5" stroke-linejoin="round"><path d="M-40 130 L-30 0 L40 0 L50 130Z" fill="#1fae5a"/><rect x="-34" y="-100" width="22" height="104" rx="11" fill="#7a4e36"/><rect x="-8" y="-114" width="22" height="116" rx="11" fill="#7a4e36"/><rect x="18" y="-104" width="22" height="108" rx="11" fill="#7a4e36"/><rect x="42" y="-82" width="20" height="86" rx="10" fill="#7a4e36"/><rect x="-60" y="-50" width="26" height="64" rx="12" fill="#7a4e36" transform="rotate(-25 -47 -20)"/></g>`)},
heart(){return svg(`<defs><linearGradient id="sn${uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2860"/><stop offset=".6" stop-color="#ff9a4a"/><stop offset="1" stop-color="#ffd27a"/></linearGradient></defs><rect width="800" height="500" fill="url(#sn${uid})"/><circle cx="600" cy="300" r="110" fill="#ffe9a0" stroke="${O}" stroke-width="5"/>${skyline(21,430,90,250,'#4a2a56',0,'#000')}${skyline(8,520,80,210,'#1f1430',.1,'#ffcf6a')}${hero(250,250,1.1,{suit:true,mouth:'smile',shades:false})}${hero(560,350,.78,{suit:false,age:'kid',mouth:'smile'})}<path d="M170 395 Q300 360 420 370" stroke="${O}" stroke-width="5" fill="none"/>`)},
heartbig(){const g='hb'+uid++;return svg(`<defs>${rad(g,'#19e36b',.9)}</defs><rect width="800" height="500" fill="#0b2a22"/>${rays(400,250,26,700,'#19e36b',.15,2)}<circle cx="400" cy="240" r="300" fill="url(#${g})"/><path d="M400 400 C150 260 170 90 300 90 C360 90 390 120 400 150 C410 120 440 90 500 90 C630 90 650 260 400 400Z" fill="#19e36b" stroke="${O}" stroke-width="8"/><path d="M290 130 Q230 140 220 200" fill="none" stroke="#eafff1" stroke-width="14" stroke-linecap="round" opacity=".8"/>`)},
back(){return svg(`<rect width="800" height="500" fill="#020712"/>${stars(140,5)}${planet(560,230,200)}<path d="M0 500 L0 420 Q200 380 400 430 L800 410 V500Z" fill="#171a22" stroke="${O}" stroke-width="5"/>${lamp(300,330,'#19e36b')}<g stroke="${O}" stroke-width="5" stroke-linejoin="round"><path d="M180 500 L200 330 Q300 290 400 330 L420 500Z" fill="#1fae5a"/><path d="M180 500 L200 330 L240 340 L228 500Z" fill="#0b6a35" stroke="none"/><rect x="274" y="268" width="52" height="50" fill="#5d3a28"/><ellipse cx="300" cy="235" rx="62" ry="72" fill="#171210"/><ellipse cx="238" cy="240" rx="12" ry="18" fill="#664230"/><ellipse cx="362" cy="240" rx="12" ry="18" fill="#664230"/></g>`)},
aurio(){const g='au'+uid++;return svg(`<defs>${rad(g,'#19e36b',.9)}<linearGradient id="gold${uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0a0"/><stop offset=".5" stop-color="#ffcf3a"/><stop offset="1" stop-color="#b9801a"/></linearGradient></defs><rect width="800" height="500" fill="#031208"/>${rays(400,250,36,800,'#19e36b',.2,9)}<circle cx="400" cy="250" r="360" fill="url(#${g})"/>${burst(400,250,190,370,20,'#0d5a31',5)}<text x="400" y="190" text-anchor="middle" font-family="Bangers,Impact" font-size="44" fill="#eafff1" stroke="#000" stroke-width="3" paint-order="stroke">O SEU NOME É...</text><text x="400" y="340" text-anchor="middle" font-family="Bangers,Impact" font-size="190" fill="url(#gold${uid})" stroke="#000" stroke-width="9" paint-order="stroke" letter-spacing="8">AURIO</text><text x="400" y="400" text-anchor="middle" font-family="Bangers,Impact" font-size="34" fill="#b6ffc8" stroke="#000" stroke-width="5" paint-order="stroke">21 DE DEZEMBRO · O NASCIMENTO DE UMA LENDA</text>`)},
party(){return svg(`<rect width="800" height="500" fill="#073a26"/>${rays(400,250,22,700,'#ffe45c',.1,5)}${Array.from({length:70},(_,i)=>{const r=rng(i+3);const c=['#19e36b','#ffcf3a','#fff','#6ec8ff','#ff7ab0'][i%5];return `<rect x="${r()*800}" y="${r()*500}" width="9" height="14" fill="${c}" transform="rotate(${r()*180} 400 250)" stroke="#000" stroke-width="1"/>`}).join('')}${[[90,'#ffcf3a'],[190,'#19e36b'],[610,'#ffcf3a'],[710,'#19e36b']].map(([x,c],i)=>`<line x1="${x}" y1="${150+i%2*20}" x2="${x+10}" y2="440" stroke="#ddd" stroke-width="3"/><ellipse cx="${x}" cy="${110+i%2*20}" rx="46" ry="58" fill="${c}" stroke="${O}" stroke-width="5"/>`).join('')}${hero(300,300,1.0,{suit:true,mouth:'smile',shades:true})}<g stroke="${O}" stroke-width="5" stroke-linejoin="round"><rect x="530" y="370" width="200" height="100" fill="#f4e8d0"/><rect x="530" y="370" width="200" height="30" fill="#19e36b"/><rect x="625" y="320" width="10" height="50" fill="#fff4c8"/><path d="M630 276 Q650 310 630 320 Q610 310 630 276Z" fill="#ffb02e"/></g><g stroke="${O}" stroke-width="5"><path d="M520 330 L520 380 Q520 400 540 400 H575 Q595 400 595 380 V330Z" fill="#fff"/><circle cx="557" cy="365" r="14" fill="#19e36b"/></g>`)}
};

// ---------- chapters ----------
const P=(cls,art,extra='',ar,rot)=>`<div class="panel ${cls}" style="${ar?`--ar:${ar};`:''}${rot?`--rot:${rot}deg;`:''}">${art}${extra}</div>`;
const cap=(pos,t,k='')=>`<div class="cap ${pos} ${k}">${t}</div>`;
const bub=(t,s)=>`<div class="bub" style="${s}">${t}</div>`;
const sfx=(t,s)=>`<div class="sfx" style="${s}">${t}</div>`;
const CH=[
{t:'Era uma vez...',a:1,html:[
 P('span12',A.book(),cap('bl','Era uma vez... num universo onde a escuridão ameaçava consumir a luz e a esperança parecia ter abandonado a humanidade.','dark')+cap('br','Mas o universo ainda não sabia no que se estava a meter...','gold')+sfx('ERA UMA VEZ...','left:50%;top:8px;transform:translateX(-50%) rotate(-3deg);white-space:nowrap'),'16/8.5')],
 say:'Existia uma força capaz de mudar o destino de toda a existência. Uma força alimentada pela vontade. Uma força que precisava de um novo guardião.'},
{t:'A cidade corrompida',a:2,html:[
 P('span8',A.city(),cap('tl','Naquele tempo, a cidade encontrava-se mergulhada no caos.','dark')+cap('br','A corrupção tomou conta das instituições e a injustiça dominava as ruas.')),
 P('span4',A.crowd(),cap('bc','Os inocentes já não sabiam a quem recorrer.','dark')+sfx('CRASH!','right:10px;top:6px'),'4/5',1.2)],
 say:'A humanidade precisava de um herói. Alguém com coragem, com força... e, acima de tudo, com uma paciência extraordinária. Infelizmente, a última qualidade não estava incluída no pacote.'},
{t:'O nascimento',a:3,html:[
 P('span4',A.window(),cap('tl','E então... no dia 21 de dezembro...','gold')+sfx('21 DEZ','left:14px;bottom:4px'),'4/5',-1),
 P('span8',A.baby(),cap('br','...nasceu um menino. Ainda incapaz de responder com sarcasmo a quem se aproximasse.')+bub('UÁÁÁ!','left:34px;top:24px'),'1.63')],
 say:'Naquele momento, ninguém imaginava o que o futuro lhe reservava. Mas o destino já tinha outros planos: começava a história de uma das personalidades mais difíceis de ignorar em todo o universo.'},
{t:'A personalidade',a:4,html:[
 P('span4',A.grow('kid','smile'),cap('tl','Era inteligente e observador...')+bub('Hehe!','right:14px;bottom:56px'),'4/5',-1.5),
 P('span4',A.grow('teen','smirk'),cap('tl','...com um humor... bastante particular.'),'4/5',1),
 P('span4',A.grow('adult','smirk'),cap('tl','O sarcasmo tornou-se a sua segunda língua.')+bub('Calma, calma...','left:8%;bottom:46px'),'4/5',-.8)],
 say:'Tinha uma resposta para quase tudo e uma piada para qualquer situação. E a expressão que viria a ser a sua assinatura: “Calma, calma...”'},
{t:'A escolha do anel',a:5,html:[
 P('span8',A.ring(),cap('tl','Até que chegou o dia. O anel percorreu galáxias à procura de alguém digno do seu poder.','dark')+sfx('ZOOOM!','right:12px;bottom:6px'),'1.63'),
 P('span4',A.ringhand(),cap('bc','Coragem. Determinação. Uma vontade inabalável.','dark'),'4/5',1.2),
 P('span4',A.suit(),cap('bc','Nascia um novo guardião da luz esmeralda.','gold')+sfx('KRAAA!','left:8px;top:2px'),'4/5',-1),
 P('span8',A.holo(),`<div class="cap tl dark" style="font-family:Bangers;font-size:clamp(18px,2.4vw,30px);color:#19e36b">GUARDIÕES DO UNIVERSO</div><div class="cap dark" style="left:6%;top:30%;max-width:68%;font-size:clamp(14px,1.9vw,24px)">“Após uma avaliação rigorosa, confirmamos que o candidato possui todas as qualidades necessárias... embora recomendemos formação adicional em contenção verbal.”</div>`,'1.63')],
 say:'Um homem com um coração suficientemente grande para proteger o universo... e uma língua suficientemente afiada para deixar os próprios inimigos sem resposta.'},
{t:'O herói que ninguém pediu',a:6,html:[
 P('span12',A.fly(),cap('tl','A cidade ganhou um novo protetor. Os criminosos começaram a tremer.','dark')+sfx('WHOOSH!','right:20px;top:8px'),'16/7'),
 P('span6',A.shield(),cap('bl','Os inocentes recuperaram a esperança.')+sfx('BOOM!','right:10px;top:4px')),
 P('span6',A.calma(),cap('tl','Enquanto outros ofereciam conforto, ele oferecia conselhos com uma observação bastante desnecessária.')+bub('Calma, calma...','right:12px;bottom:70px')+cap('br','“Da próxima vez, tenta não morrer. Dá muito trabalho.”','gold'))],
 say:'Era um herói. Mas definitivamente não era um diplomata.'},
{t:'Por detrás do sarcasmo',a:7,html:[
 P('span8',A.heart(),cap('tl','Mas por detrás de todas aquelas piadas... existia algo que o distinguia.','dark')+cap('br','Alguém que ouvia. Que aconselhava. Que procurava soluções.'),'1.63'),
 P('span4',A.heartbig(),cap('bc','Um coração enorme.','gold'),'4/5',1.4)],
 say:'Podia fazer uma piada sobre a tua situação... mas depois passaria horas a tentar ajudar-te a sair dela. A sua maior força nunca esteve no anel, mas na forma como cuidava dos outros.'},
{t:'O relatório final',a:8,html:[
 P('span12',A.holo(),`<div class="cap tl dark" style="font-family:Bangers;font-size:clamp(18px,2.6vw,34px);color:#19e36b">GUARDIÕES DO UNIVERSO — RELATÓRIO FINAL</div><div id="rep" style="position:absolute;left:7%;top:20%;width:60%;z-index:3;font-size:clamp(13px,1.9vw,24px);color:#d8ffe8;line-height:1.7">${[['Poder','Extraordinário',100],['Coragem','Inquestionável',98],['Lealdade','Absoluta',100],['Aconselhar os outros','Elevada',85],['Sentido de humor','Questionável',40],['Diplomacia','Em formação',25],['Capacidade de roast','Ameaça intergaláctica',100]].map(([a,b,v])=>`<div style="display:flex;gap:10px;align-items:center"><b style="width:36%">${a}</b><span style="flex:1;height:12px;background:#0007;border:2px solid #19e36b"><i style="display:block;height:100%;width:${v}%;background:#19e36b"></i></span><em style="width:34%;color:#ffe45c;font-style:normal">${b}</em></div>`).join('')}</div>${cap('br','Observação final: o candidato está APROVADO. Embora se recomende que alguns habitantes da Terra recebam formação emocional antes de interagir com ele.','gold')}`,'16/8')],
 say:''},
{t:'A revelação',a:9,html:[
 P('span6',A.back(),cap('tl','E assim... a história daquele pequeno menino tornou-se uma lenda.','dark')+cap('br','Quem é este homem? Quem é o guardião escolhido pelo universo?')+bub('?!','right:20px;top:20px')),
 P('span6',A.aurio(),cap('bc','...É AURIO.','gold'))],
 say:'Um guardião de coração gigante. De vontade inabalável. De humor imprevisível. E de uma capacidade extraordinária de transformar qualquer conversa numa sessão de comédia.'},
{t:'Feliz aniversário!',a:10,html:[
 P('span12',A.party(),cap('bl','Que nunca te faltem sonhos, motivos para sorrir e, naturalmente... pessoas para roastar.','gold')+sfx('FELIZ ANIVERSÁRIO, AURIO!','left:50%;top:6px;transform:translateX(-50%) rotate(-2deg);font-size:clamp(28px,6vw,80px);white-space:nowrap')+bub('Calma, calma... ainda há muitas aventuras!','right:5%;top:27%;font-size:clamp(14px,2.2vw,26px)'),'16/9.5')],
 say:'No final de todas as grandes histórias, o que importa são as pessoas que escolhemos proteger, as amizades e as memórias. Feliz aniversário, Aurio! Que a vontade esteja contigo. Sempre.'}
];
const main=document.getElementById('main');
main.innerHTML=CH.map((c,i)=>`<section class="chapter" data-i="${i+1}"><div class="ch-title"><span class="n">${i+1}</span><h2>${c.t}</h2><button class="play" data-i="${i+1}">▶ Ouvir</button></div><div class="grid">${c.html.join('')}</div>${c.say?`<div class="say">${c.say}</div>`:''}</section>`).join('');
let auto=true,cur=null;const aud=new Audio();
const play=i=>{aud.src=`audio/s${i}.mp3`;aud.play().catch(()=>{});cur=i;document.querySelectorAll('.play').forEach(b=>b.textContent=(+b.dataset.i===i?'🔊 A tocar':'▶ Ouvir'))};
document.querySelectorAll('.play').forEach(b=>b.onclick=()=>play(+b.dataset.i));
document.getElementById('stop').onclick=()=>{aud.pause();cur=null;document.querySelectorAll('.play').forEach(b=>b.textContent='▶ Ouvir')};
const ab=document.getElementById('auto');ab.onclick=()=>{auto=!auto;ab.textContent='🔊 Narração automática: '+(auto?'LIGADA':'DESLIGADA');ab.classList.toggle('off',!auto)};
aud.onended=()=>{if(auto&&cur&&cur<10){const n=cur+1;document.querySelector(`.chapter[data-i="${n}"]`).scrollIntoView({behavior:'smooth',block:'start'});play(n)}};
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in')}),{threshold:.12});
document.querySelectorAll('.panel').forEach(p=>io.observe(p));
const mo=document.getElementById('modal');
const openL=()=>{mo.classList.add('open');document.body.style.overflow='hidden'},closeL=()=>{mo.classList.remove('open');document.body.style.overflow=''};
document.getElementById('openLetter').onclick=openL;document.getElementById('closeLetter').onclick=closeL;
mo.onclick=e=>{if(e.target===mo)closeL()};document.addEventListener('keydown',e=>{if(e.key==='Escape')closeL()});
