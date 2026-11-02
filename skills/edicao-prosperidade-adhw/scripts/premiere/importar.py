import json,sys,os,subprocess
T,J=sys.argv[1],sys.argv[2]
lotes=[("03.Medias/FIGURAS PUBLICAS",f"{J}/MEDIA/BANCO/FIGURAS PUBLICAS",".mp4")]
for bin_,pasta,ext in lotes:
    fs=sorted(os.path.join(pasta,f) for f in os.listdir(pasta) if f.endswith(ext))
    for i in range(0,len(fs),6):
        part=fs[i:i+6]
        js="""function bin(p){var parts=p.split('/'),cur=app.project.rootItem;for(var i=0;i<parts.length;i++){var f=null;for(var j=0;j<cur.children.numItems;j++){var c=cur.children[j];if(c.type==2&&String(c.name)==parts[i]){f=c;break;}}if(!f)f=cur.createBin(parts[i]);cur=f;}return cur;}
var b=bin(%s);var fs=%s;var ja={};for(var j=0;j<b.children.numItems;j++)ja[String(b.children[j].name)]=1;var n=0;
for(var i=0;i<fs.length;i++){var nm=fs[i].split('/').pop();if(ja[nm])continue;app.project.importFiles([fs[i]],true,b,false);n++;}
return {bin:%s,importados:n,total:b.children.numItems};"""%(json.dumps(bin_),json.dumps(part),json.dumps(bin_))
        open(T+"/imp.jsx","w").write(js)
        r=subprocess.run([T+"/pr.sh",T+"/imp.jsx"],capture_output=True,text=True).stdout
        try: print(json.loads(json.loads(r)["result"]["content"][0]["text"])["retorno"],flush=True)
        except Exception: print("ERRO",r[:300],flush=True)
