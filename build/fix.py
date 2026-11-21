import re,subprocess
d=[float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"audio/s{i}.mp3"])) for i in range(1,11)]
s=open("make.py",encoding="utf8").read()
it=iter(d)
s=re.sub(r"^\((\d+),\[",lambda m:f"({next(it)+1.0:.2f},[",s,flags=re.M)
s=s.replace("Aurio_O_Livro_das_Lendas_animatic.mp4","build\\silent.mp4")
open("make.py","w",encoding="utf8").write(s)
with open("list.txt","w") as f:
    for i in range(1,11): f.write(f"file 'audio/s{i}.mp3'\nfile 'pad.wav'\n")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","1","pad.wav"])
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i","list.txt","-ar","24000","-ac","1","narration.wav"])
