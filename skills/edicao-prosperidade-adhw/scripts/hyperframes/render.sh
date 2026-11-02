#!/bin/bash
# uso: render.sh <pasta HYPERFRAMES> <versao> B01 B02 ...   (2 renders por vez)
export PATH=/opt/homebrew/opt/node@24/bin:$PATH
P="$1"; V="$2"; shift 2
r(){ cd "$P/$1" && npx -y hyperframes@0.8.143 check >/dev/null 2>&1 && npx -y hyperframes@0.8.143 render --format mov --fps 25 --output "$P/$1_OVERLAY_hyperframes_$V.mov" 2>&1 | grep -E "MB ·|rror" | sed "s/^/$1 /" || echo "$1 CHECK FALHOU — rode npx hyperframes check na pasta"; }
while [ $# -gt 0 ]; do r $1 & if [ -n "$2" ]; then r $2 & fi; wait; shift; [ $# -gt 0 ] && shift; done
echo FIM
