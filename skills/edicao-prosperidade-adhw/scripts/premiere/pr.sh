#!/bin/bash
# uso: pr.sh arquivo.jsx  -> roda via pr_extendscript (Tools PRO 7842)
TOK=$(python3 -I -c "import json,os;print(json.load(open(os.path.expanduser('~/.editor-black-belt/mcp-ppro.json')))['token'])")
COD=$(python3 -I -c "import json,sys;print(json.dumps(open(sys.argv[1]).read()))" "$1")
curl -sS -m ${2:-170} -X POST http://127.0.0.1:7842/mcp -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
 -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"pr_extendscript\",\"arguments\":{\"codigo\":$COD}}}"
