---
name: cortar-aula
description: Corta silencios e tempo morto de aulas gravadas (video) usando a receita aprovada "corte suave" — ffmpeg local, sem motion, sem legenda, com margem generosa pra nunca cortar palavra. Use quando pedirem "corta essa aula", "tira os silencios", "edita a aula", "remove o tempo morto" ou apontarem um arquivo/pasta de aula gravada (.mov/.mp4) pedindo edicao. Serve para 1 video ou uma pasta inteira. NAO e pra gerar/legendar/adicionar motion — so remove pausas.
---

# Cortar aula (corte de silencios)

Ferramenta local que remove pausas/tempo morto de aulas gravadas mantendo a fala intacta.

## Um video
```bash
python3 "/Users/jhonwill/Ferramentas/CorteDeAulas/cortar_aula.py" "CAMINHO/AULA 01.mov"
```
Salva ao lado com sufixo `(corte suave)`. Para escolher a saida: `-o "SAIDA.mov"`.

## Pasta inteira
```bash
python3 "/Users/jhonwill/Ferramentas/CorteDeAulas/cortar_pasta.py" "CAMINHO/Aula Gravada" "CAMINHO/Aula Editada"
```

## Receita aprovada (padrao "suave")
- `silencedetect=noise=-32dB:d=0.6`. Corta so o miolo: `KEEP_AFTER=0.34s`, `KEEP_BEFORE=0.42s`, so corta se sobrar `>=0.20s`.
- Render: `libx264 preset medium crf 19 yuv420p` + `aac 192k` + faststart.
- Se comer palavra, afrouxe com `--dur 0.8`.
