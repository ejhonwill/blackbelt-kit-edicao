import json,subprocess,sys,os,urllib.request
H=os.path.expanduser("~/.npm-global/bin/higgsfield")
jobs=json.load(open(sys.argv[1])); outdir=sys.argv[2]; ext=sys.argv[3] if len(sys.argv)>3 else "png"
pend=0
for name,jid in jobs.items():
    dst=f"{outdir}/{name}.{ext}"
    if os.path.exists(dst): continue
    r=subprocess.run([H,"generate","get",jid,"--json"],capture_output=True,text=True).stdout
    try: d=json.JSONDecoder().raw_decode(r[r.find('{'):])[0]
    except Exception: print(name,"?",r[:120]); pend+=1; continue
    st=d.get("status"); url=d.get("result_url") or (d.get("result") or {}).get("url")
    if st in("completed","succeeded","done") and url:
        urllib.request.urlretrieve(url,dst); print(name,"baixado")
    else:
        print(name,st); pend+= st not in("failed","nsfw","canceled")
print("PENDENTES",pend)
