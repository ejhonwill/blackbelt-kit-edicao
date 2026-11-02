import os,re,subprocess,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import cfg; C=cfg.load()
from concurrent.futures import ThreadPoolExecutor
M=sys.argv[1]; os.chdir(M)
for d in ["HEYGEN/SEM AUDIO","BANCO/TRANSICOES/SEM AUDIO","AUDIO/SFX/NORMALIZADOS","AUDIO/TRILHA/POR BODY"]: os.makedirs(d,exist_ok=True)
def ff(*a): subprocess.run(["ffmpeg","-v","error",*a,"-y"],check=True)
jobs=[]
for f in sorted(os.listdir("HEYGEN")):
    if f.endswith(".mp4"): jobs.append(("-i",f"HEYGEN/{f}","-map","0:v","-c","copy",f"HEYGEN/SEM AUDIO/{f[:-4]}_mute.mp4"))
for f in sorted(os.listdir("BANCO/TRANSICOES")):
    if f.endswith(".mp4"): jobs.append(("-i",f"BANCO/TRANSICOES/{f}","-map","0:v","-c","copy",f"BANCO/TRANSICOES/SEM AUDIO/{f[:-4]}_mute.mp4"))
jobs.append(("-i","BANCO/CTA/learn more.mov","-map","0:v","-c","copy","BANCO/CTA/learn more_mute.mov"))
for f in sorted(os.listdir("AUDIO/SFX")):
    if f.endswith(".mp3"):
        n=re.sub(r"[^A-Za-z0-9]+","_",f[:-4].replace(" ( By Ashish Editz )","").replace(" - SFX Producer","").replace(" Sound Effect","")).strip("_")
        jobs.append(("-i",f"AUDIO/SFX/{f}","-af","loudnorm=I=-22:TP=-3","-ar","48000",f"AUDIO/SFX/NORMALIZADOS/SFX_{n}.wav"))
MUS={k:b["trilha"] for k,b in C["bodies"].items()}
for k,m in MUS.items():
    d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"HEYGEN/{k}_AVATAR_heygen-IV_v01.mp4"],capture_output=True,text=True).stdout)
    jobs.append(("-i",f"AUDIO/TRILHA/{m}","-t",f"{d:.3f}","-af",f"loudnorm=I=-34:TP=-9,afade=t=in:d=1.0,afade=t=out:st={d-2.5:.3f}:d=2.5","-ar","48000","-ac","2",f"AUDIO/TRILHA/POR BODY/{k}_TRILHA_v01.wav"))
with ThreadPoolExecutor(6) as ex: list(ex.map(lambda a: ff(*a),jobs))
for d in ["HEYGEN/SEM AUDIO","BANCO/TRANSICOES/SEM AUDIO","AUDIO/SFX/NORMALIZADOS","AUDIO/TRILHA/POR BODY"]: print(d,sorted(os.listdir(d)))
