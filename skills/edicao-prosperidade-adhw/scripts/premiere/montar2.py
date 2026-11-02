import json,sys,subprocess,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import cfg; C=cfg.load()
T=sys.argv[1]
def run(js):
    open(T+"/m.jsx","w").write(js); r=subprocess.run([T+"/pr.sh",T+"/m.jsx","300"],capture_output=True,text=True).stdout
    try: return json.loads(json.loads(r)["result"]["content"][0]["text"]).get("retorno")
    except Exception: return "ERRO "+r[:300]
for k in sys.argv[2:]:
    seq=cfg.seq(C,k); P=json.load(open(f"{T}/{k}_plano.json"))
    print(run(open(T+"/limpar2.jsx.tpl").read().replace("__SEQ__",json.dumps(seq))))
    P2={"seq":seq,"V":[v for v in P["V"] if v["tr"]==1],"A":P["A"]}
    for fase in ["V","A"]:
        print(run(open(T+"/montar.jsx.tpl").read().replace("__PLANO__",json.dumps(P2)).replace("__FASE__",json.dumps(fase))))
    print(run(open(T+"/zoom.jsx.tpl").read().replace("__SEQ__",json.dumps(seq)).replace("__Z__",json.dumps(P["Z"]))))
    print(run(open(T+"/fechar.jsx").read()))
