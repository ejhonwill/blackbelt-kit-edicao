#!/bin/zsh
# roda o CLI do HWStudio contra o site, com o token da config do MCP (sem imprimir)
eval "$(python3 -c "
import json,os,shlex
e=json.load(open(os.path.expanduser('~/.claude.json')))['mcpServers']['hwstudio']['env']
print('export HWSTUDIO_URL='+shlex.quote(e['HWSTUDIO_URL'])+'; export HWSTUDIO_TOKEN='+shlex.quote(e['HWSTUDIO_TOKEN']))
")"
exec python3 /Users/jhonwill/Documents/03_Apps/hwstudio/mcp/hwstudio_mcp.py "$@"
