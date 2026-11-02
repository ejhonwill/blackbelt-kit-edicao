import json,sys,os,base64,urllib.request
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import cfg; C=cfg.load()
W=sys.argv[1]; key=[l.split("=",1)[1].strip().strip('"') for l in open(os.path.expanduser("~/.config/hw-creative/.env")) if l.startswith("ELEVENLABS_API_KEY")][0]
V={k:b["voz"] for k,b in C["bodies"].items()}
C=json.load(open(W+"/voz/copy_en.json"))
for k in sys.argv[2:]:
    text=" ".join(C[k])
    body=json.dumps({"text":text,"model_id":"eleven_v4","output_format":"mp3_44100_192"}).encode()
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V[k]}/with-timestamps",data=body,headers={"xi-api-key":key,"Content-Type":"application/json"})
    try:
        d=json.load(urllib.request.urlopen(req,timeout=600))
    except urllib.error.HTTPError as e:
        print(k,"ERRO",e.code,e.read()[:300]); continue
    open(f"{W}/voz/{k}_VOZ_bruta_v01.mp3","wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d.get("alignment"),open(f"{W}/voz/{k}_VOZ_bruta_v01.align.json","w"))
    print(k,"ok",len(text),"chars",flush=True)
