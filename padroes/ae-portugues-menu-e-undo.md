---
name: ae-portugues-menu-e-undo
description: O After do usuário está em PT-BR — findMenuCommandId('Undo') devolve 0 e executeCommand(0) falha calado
metadata:
  type: reference
---

O After Effects deste Mac está em **português**. Consequência que já custou um botão mentiroso no
Organizar: `app.findMenuCommandId('Undo')` devolve **0**, porque lá o item do menu se chama
"Desfazer" (id 2371 nesta instalação, mas esse número não é estável entre versões).

E `app.executeCommand(0)` **não faz nada e não lança erro** — a função retornava `ok:true` e o painel
dizia "Desfeito" com o projeto intacto.

**Como fazer:** usar o **id numérico** do comando, que independe do idioma — `app.executeCommand(16)`
é Editar > Desfazer. E **provar** que funcionou: tirar uma assinatura do projeto (pastas:soltos:total)
antes e depois, e só reportar sucesso se ela mudou.

É o mesmo tipo de armadilha de [[premiere-ptbr-nomes-de-efeito]]: API que casa por nome falha calada
num app localizado. Vale para qualquer `findMenuCommandId` e para qualquer busca por nome de efeito,
menu ou preset em Adobe daqui.
