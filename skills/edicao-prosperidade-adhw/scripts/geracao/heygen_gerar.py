import json,subprocess,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import cfg; C=cfg.load()
W=sys.argv[1]; HG=os.path.expanduser("~/.local/bin/heygen")
SEL={k:b["avatar"] for k,b in C["bodies"].items()}
EXP={k:b.get("expressividade","medium") for k,b in C["bodies"].items()}
M=json.load(open(W+"/heygen/motion.json")); log=W+"/heygen/ids.json"
ids=json.load(open(log)) if os.path.exists(log) else {}
def up(p):
    r=json.loads(subprocess.run([HG,"asset","create","--file",p],capture_output=True,text=True).stdout)
    d=r.get("data",r); return d.get("asset_id") or d.get("id")
for k in sys.argv[2:]:
    if ids.get(k,{}).get("video_id"): print(k,"já criado"); continue
    jpg=f"{W}/heygen/{k}_avatar.jpg"
    subprocess.run(["ffmpeg","-v","error","-i",f"{W}/avatars/{SEL[k]}.png","-q:v","2",jpg,"-y"],check=True)
    img=up(jpg); aud=up(f"{W}/voz/{k}_VOZ_decupada_v02.wav")
    body={"type":"image","image":{"type":"asset_id","asset_id":img},"audio_asset_id":aud,"aspect_ratio":"9:16","resolution":"1080p","fit":"cover","expressiveness":EXP[k],"motion_prompt":M[k],"output_format":"mp4","title":f"{C['produto']} {k} Avatar IV v01"}
    r=subprocess.run([HG,"video","create","-d",json.dumps(body)],capture_output=True,text=True)
    try: d=json.loads(r.stdout); d=d.get("data",d); vid=d.get("video_id") or d.get("id")
    except Exception: vid=None
    ids[k]={"img":img,"aud":aud,"video_id":vid,"err":None if vid else (r.stdout+r.stderr)[-400:]}
    json.dump(ids,open(log,"w"),indent=1); print(k,ids[k],flush=True)
