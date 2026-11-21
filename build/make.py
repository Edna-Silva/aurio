import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
SRC=r"C:\Users\yamme\AppData\Local\Temp\claude\c7dc91baca7aa393\367ddd93-4555-42d4-81f7-a0c0097f4f70\images\1.png"
OUT=r"c:\Users\yamme\Downloads\AURIO\build\silent.mp4"
im=Image.open(SRC).convert("RGB")
rows=[(0,232),(236,450),(454,660)]
cols=[[(0,365),(367,750),(752,1138),(1141,1536)],
      [(0,343),(345,748),(750,1082),(1084,1536)],
      [(0,417),(419,844),(846,1175),(1177,1536)]]
P=[]
for (y0,y1),cs in zip(rows,cols):
    for x0,x1 in cs: P.append(im.crop((x0+2,y0+2,x1-2,y1-2)))
W,H,FPS=1280,720,30
f=lambda n,s:ImageFont.truetype(r"C:\Windows\Fonts\%s"%n,s)
sub=f("georgia.ttf",34); big=f("georgiab.ttf",120); mid=f("georgiab.ttf",44)
# (duration s, panel indexes, subtitle lines)
S=[
(24.76,[0],["Era uma vez...","Num universo onde a escuridão ameaçava consumir a luz,","existia uma força capaz de mudar o destino de toda a existência.","Uma força que precisava de um novo guardião.","Mas o universo ainda não sabia no que se estava a meter..."]),
(30.52,[1],["Naquele tempo, a cidade encontrava-se mergulhada no caos.","A corrupção tinha tomado conta das instituições.","A humanidade precisava de um herói.","E, acima de tudo... alguém com uma paciência extraordinária.","Infelizmente, a última qualidade não estava incluída no pacote."]),
(31.67,[2],["E então... No dia 21 de dezembro, nasceu um menino.","Ninguém imaginava o que o futuro lhe reservava.","Ainda incapaz de responder com sarcasmo a quem se aproximasse.","Começava a história de uma das personalidades","mais difíceis de ignorar em todo o universo."]),
(27.18,[3],["Os anos passaram.","Era inteligente, observador e tinha um sentido de humor... bastante particular.","Uma piada para qualquer situação.","O sarcasmo tornou-se a sua segunda língua.","E a sua assinatura... “Calma, calma...”"]),
(44.15,[4,6,5],["Até que chegou o dia. O anel procurou alguém digno do seu poder.","Um homem com um coração suficientemente grande para proteger o universo...","...e uma língua suficientemente afiada para deixar os inimigos sem resposta.","Nascia um novo guardião da luz esmeralda.","“Após uma avaliação rigorosa, confirmamos que o candidato possui todas as qualidades necessárias... embora recomendemos formação adicional em contenção verbal.”"]),
(39.78,[7,8],["A cidade ganhou um novo protetor.","Enquanto outros ofereciam conforto, ele oferecia conselhos","acompanhados de uma observação bastante desnecessária.","E quando tudo parecia fora de controlo... “Calma, calma...”","Era um herói. Mas definitivamente não era um diplomata."]),
(32.70,[10,9],["Mas por detrás de todas aquelas piadas... um coração enorme.","Alguém que ouvia. Que aconselhava. Que procurava soluções.","Podia fazer uma piada sobre a tua situação...","mas depois passaria horas a tentar ajudar-te a sair dela."]),
(37.05,[5],["Poder: Extraordinário. Coragem: Inquestionável. Lealdade: Absoluta.","Sentido de humor: Questionável. Diplomacia: Em formação.","Capacidade de roast: Uma ameaça à estabilidade intergaláctica.","Observação final: o candidato está aprovado."]),
(28.36,[11],["E assim... a história daquele pequeno menino tornou-se uma lenda.","Quem é o guardião escolhido pelo universo?","","O seu nome... é AURIO."]),
(42.28,[10,11],["No final, o que importa são as pessoas que escolhemos proteger.","Que nunca te faltem sonhos, motivos para sorrir e, naturalmente... pessoas para roastar.","Calma, calma... Ainda há muitas aventuras por viver.","Feliz aniversário, Aurio!  QUE A VONTADE ESTEJA CONTIGO. SEMPRE."]),
]
def cover(p,t):
    z=1.0+0.10*t
    pw,ph=p.size; s=max(W/pw,H/ph)*z
    nw,nh=int(pw*s),int(ph*s)
    r=p.resize((nw,nh),Image.LANCZOS)
    x=(nw-W)//2; y=(nh-H)//2
    return r.crop((x,y,x+W,y+H))
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-c:v","libx264","-pix_fmt","yuv420p","-crf","20",OUT],stdin=subprocess.PIPE)
def wrap(d,txt,font,maxw):
    words,lines,cur=txt.split(),[],""
    for w in words:
        c=(cur+" "+w).strip()
        if d.textlength(c,font=font)>maxw and cur: lines.append(cur);cur=w
        else: cur=c
    return lines+[cur]
for si,(dur,pans,lines) in enumerate(S):
    n=int(dur*FPS)
    for i in range(n):
        t=i/n
        pi=pans[min(int(t*len(pans)),len(pans)-1)]
        lt=(t*len(pans))%1 if len(pans)>1 else t
        fr=cover(P[pi],lt)
        fade=min(1,i/15,(n-i)/15)
        d=ImageDraw.Draw(fr,"RGBA")
        li=min(int(t*len(lines)),len(lines)-1); txt=lines[li]
        if txt:
            ls=wrap(d,txt,sub,W-160); h=len(ls)*44+30
            d.rectangle((0,H-h-30,W,H),fill=(0,0,0,170))
            for k,l in enumerate(ls):
                w=d.textlength(l,font=sub); d.text(((W-w)/2,H-h-15+k*44),l,font=sub,fill=(235,255,235))
        if si==8 and t>0.7:
            a=int(255*min(1,(t-0.7)/0.2))
            w=d.textlength("AURIO",font=big); d.text(((W-w)/2,H/2-90),"AURIO",font=big,fill=(240,200,80,a),stroke_width=3,stroke_fill=(20,90,30,a))
            w=d.textlength("21 DE DEZEMBRO",font=mid); d.text(((W-w)/2,H/2+50),"21 DE DEZEMBRO",font=mid,fill=(160,255,120,a))
        if fade<1: fr=Image.blend(Image.new("RGB",(W,H)),fr,fade)
        ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
