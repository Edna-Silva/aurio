import re
p=r"c:\Users\yamme\Downloads\AURIO\comic\index.html"
s=open(p,encoding="utf8").read()
ring3d = r'''const ring3d=(x,y,sc=1,rot=0)=>{const i='rg'+(uid++);return `<defs>
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
'''
s=s.replace("const hand=",ring3d+"const hand=",1)
a=s.index("ring(){");b=s.index("ringhand(){")
newring='''ring(){return svg(`<rect width="800" height="500" fill="#020712"/>${stars(120,4)}${planet(650,130,86)}${rays(120,430,26,900,'#19e36b',.16,7)}${Array.from({length:9},(_,i)=>`<circle cx="${140+i*48}" cy="${430-i*24}" r="${40-i*3.5}" fill="#19e36b" opacity="${.05+i*.025}"/>`).join('')}${Array.from({length:7},(_,i)=>`<path d="M${60+i*10} ${440-i*14} H${380+i*10}" stroke="#7dffb0" stroke-width="3" opacity="${.15+i*.04}"/>`).join('')}${ring3d(520,235,1.05,-18)}${burst(520,235,70,150,12,'none',9,'#19e36b')}${Array.from({length:30},(_,i)=>{const r=rng(i+3);return `<circle cx="${r()*800}" cy="${r()*500}" r="${1+r()*2.5}" fill="#b8ffd2" opacity=".7"/>`}).join('')}`)},
'''
s=s[:a]+newring+s[b:]
old='<ellipse cx="68" cy="-46" rx="20" ry="26" fill="#19e36b" opacity=".9"/><ellipse cx="68" cy="-46" rx="12" ry="18" fill="#eafff1" stroke="none"/>'
assert old in s
s=s.replace(old,'${ring3d(30,-36,.3,-8)}')
open(p,"w",encoding="utf8").write(s)
