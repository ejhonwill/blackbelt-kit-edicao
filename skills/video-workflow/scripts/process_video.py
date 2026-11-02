#!/usr/bin/env python3
"""
process_video.py — Prepara um vídeo para o workflow video-workflow.

O que faz:
  1. Lê a duração e detecta se há trilha de áudio (ffprobe).
  2. Auto-detecta o idioma da fala com Whisper (ou usa --lang para forçar).
  3. Transcreve a fala com timestamps (Whisper local; vários backends).
  4. Agrupa a transcrição em BLOCOS SEMÂNTICOS de ~10s (corta em fim de frase,
     nunca no meio da palavra), com tolerância configurável.
  5. Corta o vídeo em um arquivo por bloco.
  6. Extrai 1 frame representativo (meio do bloco) por bloco — para o Claude
     "ver" o que já está na tela e não sugerir B-roll redundante.
  7. Escreve blocos.json (máquina) e blocos.md (leitura humana).

Uso típico:
    python process_video.py /caminho/video.mp4 -o ./saida

Se já tem a transcrição (copy/VSL), pule o Whisper:
    python process_video.py video.mp4 -o ./saida --transcript copy.srt

Backends de transcrição tentados, nesta ordem:
    1. openai-whisper (import whisper)
    2. faster-whisper (from faster_whisper import WhisperModel)
    3. whisper CLI
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


# ----------------------------- util ffmpeg -----------------------------------

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def need(bin_name):
    if shutil.which(bin_name) is None:
        sys.exit(f"[ERRO] '{bin_name}' não encontrado no PATH. Instale antes de continuar.")


def probe_duration(video):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(video)])
    try:
        return float(r.stdout.strip())
    except ValueError:
        sys.exit(f"[ERRO] não consegui ler a duração de {video}\n{r.stderr}")


def probe_info(video):
    r = run(["ffprobe", "-v", "error",
             "-show_entries", "format=duration,size:stream=width,height",
             "-of", "json", str(video)])
    try:
        data = json.loads(r.stdout)
        fmt = data.get("format", {})
        streams = data.get("streams", [{}])
        vs = next((s for s in streams if s.get("width")), streams[0] if streams else {})
        return {
            "duration": float(fmt.get("duration", 0)),
            "width": vs.get("width"),
            "height": vs.get("height"),
        }
    except Exception:
        return {"duration": probe_duration(video), "width": None, "height": None}


def has_audio_stream(video):
    r = run(["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=index", "-of", "csv=p=0", str(video)])
    return bool(r.stdout.strip())


def fmt_ts(seconds):
    m, s = divmod(int(round(seconds)), 60)
    return f"{m:02d}:{s:02d}"


# --------------------------- auto-detecção de idioma -------------------------

def autodetect_language(video, model_size="small"):
    """Usa Whisper para detectar o idioma do áudio. Retorna código ISO ou None."""
    try:
        import whisper
        import warnings
        warnings.filterwarnings("ignore")
        print("[info] detectando idioma da fala...", flush=True)
        model = whisper.load_model(model_size)
        audio = whisper.load_audio(str(video))
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio)
        _, probs = model.detect_language(mel)
        detected = max(probs, key=probs.get)
        conf = probs[detected]
        print(f"[info] idioma detectado: {detected} (confiança: {conf:.0%})", flush=True)
        return detected, model  # devolve o model já carregado para reusar
    except Exception as e:
        print(f"[aviso] auto-detecção falhou ({e}), usando sem restrição de idioma.", flush=True)
        return None, None


# --------------------------- transcrição -------------------------------------

def parse_srt(path):
    """Lê um .srt e devolve [{start, end, text}]."""
    txt = Path(path).read_text(encoding="utf-8", errors="ignore")
    blocks = re.split(r"\n\s*\n", txt.strip())
    segs = []

    def to_sec(t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    for b in blocks:
        lines = [l for l in b.splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        time_line = next((l for l in lines if "-->" in l), None)
        if not time_line:
            continue
        a, _, c = time_line.partition("-->")
        text = " ".join(lines[lines.index(time_line) + 1:]).strip()
        segs.append({"start": to_sec(a.strip()), "end": to_sec(c.strip()), "text": text})
    return segs


def load_transcript_file(path):
    p = Path(path)
    if p.suffix.lower() == ".srt":
        return parse_srt(p)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "segments" in data:
            return [{"start": s["start"], "end": s["end"], "text": s["text"].strip()}
                    for s in data["segments"]]
        if isinstance(data, list):
            return data
    # .txt sem timestamps → um único segmento
    return [{"start": None, "end": None, "text": p.read_text(encoding="utf-8").strip()}]


def transcribe(video, lang, model_size, preloaded_model=None):
    """Tenta backends de Whisper. Devolve lista de segmentos com timestamps."""
    import warnings
    warnings.filterwarnings("ignore")

    # backend 1: openai-whisper (python)
    try:
        import whisper  # type: ignore
        print(f"[info] transcrevendo com openai-whisper ({model_size})...", flush=True)
        model = preloaded_model if preloaded_model else whisper.load_model(model_size)
        kwargs = {"verbose": False}
        if lang:
            kwargs["language"] = lang
        res = model.transcribe(str(video), **kwargs)
        detected_lang = res.get("language", lang or "unknown")
        print(f"[info] idioma na transcrição: {detected_lang}", flush=True)
        return [{"start": s["start"], "end": s["end"], "text": s["text"].strip()}
                for s in res["segments"]], detected_lang
    except ImportError:
        pass

    # backend 2: faster-whisper
    try:
        from faster_whisper import WhisperModel  # type: ignore
        print(f"[info] transcrevendo com faster-whisper ({model_size})...", flush=True)
        model = WhisperModel(model_size, compute_type="int8")
        kwargs = {}
        if lang:
            kwargs["language"] = lang
        segments, info = model.transcribe(str(video), **kwargs)
        detected_lang = info.language if hasattr(info, "language") else (lang or "unknown")
        return [{"start": s.start, "end": s.end, "text": s.text.strip()}
                for s in segments], detected_lang
    except ImportError:
        pass

    # backend 3: whisper CLI
    if shutil.which("whisper"):
        print(f"[info] transcrevendo com whisper CLI ({model_size})...", flush=True)
        tmp = Path("_whisper_tmp")
        tmp.mkdir(exist_ok=True)
        cmd = ["whisper", str(video), "--model", model_size,
               "--output_format", "json", "--output_dir", str(tmp)]
        if lang:
            cmd += ["--language", lang]
        run(cmd)
        js = next(tmp.glob("*.json"), None)
        if js:
            segs = load_transcript_file(js)
            shutil.rmtree(tmp, ignore_errors=True)
            return segs, lang or "unknown"
        shutil.rmtree(tmp, ignore_errors=True)

    sys.exit(
        "[ERRO] Nenhum backend de transcrição encontrado.\n"
        "  Opção A (recomendada):  pip install -U openai-whisper\n"
        "  Opção B (mais leve):    pip install faster-whisper\n"
        "  Opção C:                passe --transcript com a copy/SRT que você já tem."
    )


# --------------------------- blocagem semântica ------------------------------

def build_semantic_blocks(segments, total_dur, target, lo, hi):
    """Agrupa segmentos em blocos de ~target s, quebrando em fim de frase."""
    # sem timestamps → divisão por tempo fixo
    if not segments or segments[0].get("start") is None:
        full_text = " ".join(s["text"] for s in segments) if segments else ""
        words = full_text.split()
        n_blocks = max(1, int(round(total_dur / target)))
        per = max(1, len(words) // n_blocks) if words else 0
        blocks = []
        for i in range(n_blocks):
            start = i * (total_dur / n_blocks)
            end = min(total_dur, (i + 1) * (total_dur / n_blocks))
            chunk = " ".join(words[i * per:(i + 1) * per]) if words else ""
            blocks.append({"start": start, "end": end, "text": chunk})
        return blocks

    blocks = []
    cur = {"start": segments[0]["start"], "end": segments[0]["end"],
           "text": segments[0]["text"]}
    for seg in segments[1:]:
        dur = cur["end"] - cur["start"]
        ends_sentence = cur["text"].rstrip().endswith((".", "!", "?", "…"))
        if (dur >= target and ends_sentence) or dur >= hi:
            blocks.append(cur)
            cur = {"start": seg["start"], "end": seg["end"], "text": seg["text"]}
        else:
            cur["end"] = seg["end"]
            cur["text"] = (cur["text"] + " " + seg["text"]).strip()
    blocks.append(cur)

    # junta último bloco curtíssimo ao anterior
    if len(blocks) > 1 and (blocks[-1]["end"] - blocks[-1]["start"]) < lo:
        blocks[-2]["end"] = blocks[-1]["end"]
        blocks[-2]["text"] = (blocks[-2]["text"] + " " + blocks[-1]["text"]).strip()
        blocks.pop()
    return blocks


# --------------------------- corte + frames ----------------------------------

def cut_block(video, start, end, out_path):
    run(["ffmpeg", "-y", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
         "-i", str(video), "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "20", "-c:a", "aac", "-movflags", "+faststart",
         str(out_path)])


def grab_frame(video, t, out_path):
    run(["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(video),
         "-frames:v", "1", "-q:v", "2", str(out_path)])


# --------------------------------- main --------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Prepara vídeo para o workflow video-workflow.")
    ap.add_argument("video", help="caminho do vídeo de entrada")
    ap.add_argument("-o", "--out", default=None,
                    help="pasta de saída (padrão: <nome_video>_workflow/ ao lado do vídeo)")
    ap.add_argument("--target", type=float, default=10.0, help="duração-alvo do bloco (s)")
    ap.add_argument("--min", type=float, default=6.0, help="duração mínima do bloco (s)")
    ap.add_argument("--max", type=float, default=14.0, help="duração máxima do bloco (s)")
    ap.add_argument("--lang", default=None,
                    help="forçar idioma da fala (ex.: pt, en). Padrão: auto-detectado pelo Whisper")
    ap.add_argument("--whisper-model", default="small",
                    help="tamanho do modelo Whisper (tiny/base/small/medium/large)")
    ap.add_argument("--transcript",
                    help="usar transcrição pronta (.srt/.json/.txt) e pular o Whisper")
    ap.add_argument("--no-clips", action="store_true",
                    help="não cortar os arquivos de vídeo (só frames + json)")
    args = ap.parse_args()

    need("ffmpeg")
    need("ffprobe")
    video = Path(args.video).expanduser().resolve()
    if not video.exists():
        sys.exit(f"[ERRO] vídeo não encontrado: {video}")

    out = Path(args.out) if args.out else video.parent / f"{video.stem}_workflow"
    clips_dir = out / "blocos"
    frames_dir = out / "frames"
    for d in (out, clips_dir, frames_dir):
        d.mkdir(parents=True, exist_ok=True)

    info = probe_info(video)
    dur = info["duration"]
    audio = has_audio_stream(video)
    res = f"{info['width']}x{info['height']}" if info["width"] else "?"
    print(f"\n▶  Vídeo: {video.name}")
    print(f"   Duração: {fmt_ts(dur)} · {res} · áudio: {'sim' if audio else 'não'}")

    detected_lang = args.lang
    preloaded_model = None

    if args.transcript:
        print(f"[info] usando transcrição fornecida: {args.transcript}")
        segments = load_transcript_file(args.transcript)
        actual_lang = args.lang or "?"
    elif audio:
        # Auto-detect se --lang não foi passado
        if not args.lang:
            detected_lang, preloaded_model = autodetect_language(video, args.whisper_model)
        segments, actual_lang = transcribe(video, detected_lang, args.whisper_model, preloaded_model)
    else:
        print("[aviso] sem áudio e sem --transcript: blocos serão por tempo fixo.")
        segments = []
        actual_lang = "?"

    blocks = build_semantic_blocks(segments, dur, args.target, args.min, args.max)
    print(f"\n[info] {len(blocks)} blocos gerados.")

    manifest = {
        "source": str(video),
        "duration": round(dur, 2),
        "resolution": res,
        "has_audio": audio,
        "language": actual_lang,
        "n_blocks": len(blocks),
        "blocks": [],
    }

    md_lines = [
        "# Índice de blocos\n",
        f"Fonte: `{video.name}` · duração {fmt_ts(dur)} · idioma: {actual_lang} · {len(blocks)} blocos\n",
    ]

    for i, b in enumerate(blocks, 1):
        start, end = float(b["start"]), float(b["end"])
        mid = (start + end) / 2
        name = f"bloco_{i:02d}"
        clip = clips_dir / f"{name}.mp4"
        frame = frames_dir / f"{name}.jpg"

        print(f"   [{i:02d}/{len(blocks)}] {fmt_ts(start)}-{fmt_ts(end)}  {b['text'][:60]}…")

        if not args.no_clips:
            cut_block(video, start, end, clip)
        grab_frame(video, mid, frame)

        entry = {
            "n": i,
            "start": round(start, 2),
            "end": round(end, 2),
            "dur": round(end - start, 2),
            "ts": f"{fmt_ts(start)}-{fmt_ts(end)}",
            "language": actual_lang,
            "text": b["text"].strip(),
            "clip": str(clip) if not args.no_clips else None,
            "frame": str(frame),
        }
        manifest["blocks"].append(entry)
        md_lines.append(f"\n## Bloco {i:02d} · {entry['ts']} ({entry['dur']}s)")
        md_lines.append(f"- vídeo: `{entry['clip']}`")
        md_lines.append(f"- frame: `{entry['frame']}`")
        md_lines.append(f"- fala [{actual_lang}]: {entry['text'] or '(sem fala)'}")

    (out / "blocos.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "blocos.md").write_text("\n".join(md_lines), encoding="utf-8")

    print(f"\n✓  Saída em: {out.resolve()}")
    print(f"   - blocos.json  ({len(blocks)} blocos, idioma: {actual_lang})")
    print(f"   - blocos.md")
    print(f"   - blocos/      ({len(blocks)} clipes .mp4)")
    print(f"   - frames/      ({len(blocks)} frames .jpg)")
    print(f"\nBLOCOS_JSON:{out / 'blocos.json'}")


if __name__ == "__main__":
    main()
