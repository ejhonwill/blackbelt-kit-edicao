import json,sys,subprocess
T=sys.argv[1]
for k in sys.argv[2:]:
    subprocess.run(["python3","-I",T+"/plano.py",T,k])
    P=open(f"{T}/{k}_plano.json").read()
    for fase in ["V","A"]:
        js=open(T+"/montar.jsx.tpl").read().replace("__PLANO__",P).replace("__FASE__",json.dumps(fase))
        open(T+"/m.jsx","w").write(js)
        r=subprocess.run([T+"/pr.sh",T+"/m.jsx","300"],capture_output=True,text=True).stdout
        try: print(json.loads(json.loads(r)["result"]["content"][0]["text"]).get("retorno"),flush=True)
        except Exception: print(k,fase,"ERRO",r[:500],flush=True)
