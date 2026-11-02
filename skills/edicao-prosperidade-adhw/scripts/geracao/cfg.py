"""Lê o job.json da pasta de trabalho (WORK). Procura subindo a partir do script e do diretório atual."""
import json, os
def load():
    for base in (os.path.dirname(os.path.abspath(__file__)), os.getcwd()):
        d = base
        for _ in range(4):
            p = os.path.join(d, "job.json")
            if os.path.exists(p):
                c = json.load(open(p)); c["_work"] = d; return c
            d = os.path.dirname(d)
    raise SystemExit("job.json não encontrado — crie a partir de assets/job_exemplo.json na pasta de trabalho")
def seq(c, k): return f"{k}{c['seq_sufixo']}"
