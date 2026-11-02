#!/bin/bash
# Instala o Kit de Edição Black Belt no Claude Code desta máquina.
# Copia skills, agentes e padrões para ~/.claude e troca o caminho da máquina do Jhon pelo seu.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
C="$HOME/.claude"
mkdir -p "$C/skills" "$C/agents" "$C/padroes-blackbelt"
for s in "$DIR"/skills/*/; do
  n=$(basename "$s")
  if [ -e "$C/skills/$n" ] && [ "$1" != "--sobrescrever" ]; then echo "pulando skill $n (já existe; use --sobrescrever)"; continue; fi
  rm -rf "$C/skills/$n"; cp -R "$s" "$C/skills/$n"
done
for a in "$DIR"/agents/*.md; do
  n=$(basename "$a")
  if [ -e "$C/agents/$n" ] && [ "$1" != "--sobrescrever" ]; then echo "pulando agente $n (já existe; use --sobrescrever)"; continue; fi
  cp "$a" "$C/agents/$n"
done
cp "$DIR"/padroes/*.md "$C/padroes-blackbelt/"
# caminho da máquina do Jhon -> sua pasta
if [ "$HOME" != "/Users/jhonwill" ]; then
  grep -rIl "/Users/jhonwill" "$C/skills" "$C/agents" "$C/padroes-blackbelt" 2>/dev/null | while read f; do
    sed -i.bak "s#/Users/jhonwill#$HOME#g" "$f" && rm -f "$f.bak"
  done
fi
echo "Pronto. Reinicie o Claude Code. Leia ~/.claude/padroes-blackbelt/regras-gerais-upsell.md antes do primeiro upsell."
