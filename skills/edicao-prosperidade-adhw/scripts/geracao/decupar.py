# Decupagem por silêncio real: cada pausa > MAX vira ALVO, mantendo 0.15 s de borda dos dois lados (nunca encosta em fala).
import sys,subprocess,re
W,k=sys.argv[1],sys.argv[2]; src=f"{W}/voz/{k}_VOZ_bruta_v01.mp3"
MAXP,ALVO,BORDA=0.42,0.32,0.15
r=subprocess.run(["ffmpeg","-hide_banner","-i",src,"-af","silencedetect=n=-42dB:d=0.3","-f","null","-"],capture_output=True,text=True).stderr
ss=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",r)]; se=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",r)]
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
keep=[];cur=0.0
for a,b in zip(ss,se):
    if a<0.05: cur=max(0,b-0.12); continue
    if b>=dur-0.05: keep.append((cur,min(dur,a+0.35))); cur=None; break
    if b-a>MAXP:
        ca=a+BORDA; cb=b-BORDA-max(0,ALVO-2*BORDA)
        if cb>ca: keep.append((cur,ca)); cur=cb
if cur is not None: keep.append((cur,dur))
sel="+".join(f"between(t,{a:.3f},{b:.3f})" for a,b in keep)
out=f"{W}/voz/{k}_VOZ_decupada_v02.wav"
subprocess.run(["ffmpeg","-v","error","-i",src,"-af",f"aselect='{sel}',asetpts=N/SR/TB,loudnorm=I=-16:TP=-1.5:LRA=7","-ar","48000","-ac","1",out,"-y"],check=True)
open(f"{W}/voz/{k}_VOZ_decupada_v02.keep.txt","w").write("\n".join(f"{a:.3f} {b:.3f}" for a,b in keep))
nd=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],capture_output=True,text=True).stdout)
print(f"{k}: {dur:.1f}s -> {nd:.1f}s, {len(keep)} trechos")
