p=r"c:\Users\yamme\Downloads\AURIO\comic\index.html"
s=open(p,encoding="utf8").read()
a=s.index("const ring3d=");b=s.index("const hand=")
new=r'''const ring3d=(x,y,sc=1,rot=0)=>{const i='rg'+(uid++);return `<defs>
<linearGradient id="${i}b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8dffb0"/><stop offset=".3" stop-color="#1fd45f"/><stop offset=".6" stop-color="#0b7a33"/><stop offset="1" stop-color="#03300f"/></linearGradient>
<linearGradient id="${i}w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a3a18"/><stop offset="1" stop-color="#37e87a"/></linearGradient>
<linearGradient id="${i}t" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a6ffc2"/><stop offset=".45" stop-color="#18c254"/><stop offset="1" stop-color="#075a24"/></linearGradient>
<radialGradient id="${i}c" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffffee"/><stop offset=".4" stop-color="#f6ff9c"/><stop offset=".75" stop-color="#5dff7c"/><stop offset="1" stop-color="#18c254"/></radialGradient>
<radialGradient id="${i}g"><stop offset="0" stop-color="#19e36b" stop-opacity=".8"/><stop offset="1" stop-color="#19e36b" stop-opacity="0"/></radialGradient></defs>
<g transform="translate(${x} ${y}) rotate(${rot}) scale(${sc}) translate(-150 -170)">
<circle cx="150" cy="150" r="240" fill="url(#${i}g)"/>
<path fill-rule="evenodd" d="M150 66 C226 66 264 112 264 172 C264 238 218 276 150 276 C82 276 36 238 36 172 C36 112 74 66 150 66Z M150 124 C190 124 216 148 216 186 C216 224 190 246 150 246 C110 246 84 224 84 186 C84 148 110 124 150 124Z" fill="url(#${i}b)" stroke="#021208" stroke-width="5"/>
<path fill-rule="evenodd" d="M150 124 C190 124 216 148 216 186 C216 224 190 246 150 246 C110 246 84 224 84 186 C84 148 110 124 150 124Z M150 140 C178 140 198 160 198 188 C198 218 178 234 150 234 C122 234 102 218 102 188 C102 160 122 140 150 140Z" fill="url(#${i}w)" stroke="#021208" stroke-width="3"/>
<path d="M52 196 Q60 252 120 266" fill="none" stroke="#d9ffe6" stroke-width="8" stroke-linecap="round" opacity=".7"/>
<path d="M252 180 Q246 236 196 262" fill="none" stroke="#9dffc0" stroke-width="6" stroke-linecap="round" opacity=".5"/>
<path d="M60 130 Q70 92 112 78" fill="none" stroke="#e8fff0" stroke-width="6" stroke-linecap="round" opacity=".6"/>
<ellipse cx="150" cy="112" rx="104" ry="58" fill="#04301a" stroke="#021208" stroke-width="5"/>
<ellipse cx="150" cy="100" rx="104" ry="58" fill="url(#${i}t)" stroke="#021208" stroke-width="5"/>
<ellipse cx="150" cy="100" rx="94" ry="50" fill="none" stroke="#e8fff0" stroke-width="3" opacity=".85"/>
<ellipse cx="150" cy="102" rx="82" ry="42" fill="#0d8d38" stroke="#04301a" stroke-width="3"/>
<ellipse cx="150" cy="102" rx="52" ry="27" fill="none" stroke="#05491f" stroke-width="14"/>
<path d="M68 102 H100 M200 102 H232" stroke="#05491f" stroke-width="13" stroke-linecap="round"/>
<path d="M112 70 Q150 60 188 70" fill="none" stroke="#05491f" stroke-width="9" stroke-linecap="round"/>
<path d="M112 134 Q150 144 188 134" fill="none" stroke="#05491f" stroke-width="9" stroke-linecap="round"/>
<ellipse cx="150" cy="102" rx="40" ry="20" fill="url(#${i}c)"/>
<ellipse cx="150" cy="98" rx="62" ry="32" fill="url(#${i}g)"/>
<path d="M62 84 Q90 56 136 54" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".75"/>
<ellipse cx="134" cy="94" rx="14" ry="5" fill="#fff" opacity=".9"/>
</g>`};
'''
s=s[:a]+new+s[b:]
open(p,"w",encoding="utf8").write(s)
a=s.index("<script>")+8;b=s.index("const main=")
t='<meta charset=utf8><style>body{margin:0;background:#111}div{display:inline-block;width:640px;height:400px;margin:4px}svg{width:100%;height:100%}</style><div id=a></div><div id=b></div><div id=c style="width:360px;height:360px"></div><script>'+s[a:b]+'document.getElementById("a").innerHTML=A.ring();document.getElementById("b").innerHTML=A.ringhand();document.getElementById("c").innerHTML=svg(ring3d(150,150,1,0),"0 0 300 300").replace("<svg","<svg style=\\"background:#667\\"")</script>'
open(r"c:\Users\yamme\Downloads\AURIO\build\ringtest.html","w",encoding="utf8").write(t)
