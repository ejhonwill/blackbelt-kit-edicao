import json,sys,subprocess,os
def call(name,args,timeout=170):
    tok=json.load(open(os.path.expanduser('~/.editor-black-belt/mcp-ppro.json')))['token']
    body=json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":name,"arguments":args}})
    r=subprocess.run(["curl","-sS","-m",str(timeout),"-X","POST","http://127.0.0.1:7842/mcp","-H","Authorization: Bearer "+tok,"-H","Content-Type: application/json","-H","Accept: application/json, text/event-stream","-d",body],capture_output=True,text=True).stdout
    try: d=json.loads(r)["result"]; return d["content"][0]["text"],d.get("isError")
    except Exception: return r[:500],True
