#!/bin/bash
# Chama uma ferramenta do Tools PRO no Premiere por JSON-RPC direto — para quando o tool MCP nao
# reconecta numa sessao ja aberta. O token NUNCA fica gravado aqui: e lido na hora do registro do MCP
# (escopo local ao cwd /Users/jhonwill — fora dele o `claude mcp get` volta vazio).
# uso: pr_rpc.sh <ferramenta> '<json de argumentos>'     ex.: pr_rpc.sh pr_sequencias_listar '{}'
set -euo pipefail
CFG=$(cd "$HOME" && claude mcp get toolspro-pr 2>/dev/null)
URL=$(echo "$CFG" | grep -oE 'https?://[^ ]+' | head -1)
AUTH=$(echo "$CFG" | grep -oiE 'Authorization: *[^ ]+ +[^ ]+' | head -1 | sed -E 's/^[Aa]uthorization: *//')
[ -n "$URL" ] && [ -n "$AUTH" ] || { echo "toolspro-pr nao registrado (rode de /Users/jhonwill)" >&2; exit 2; }
curl -s -m 120 -X POST "$URL" -H 'Content-Type: application/json' -H "Authorization: $AUTH" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$1\",\"arguments\":${2:-{\}}}}"
