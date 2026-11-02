#!/usr/bin/env python3
"""Conteúdo de cada b-roll do mecanismo e da oferta, colado no que está sendo dito.

Três famílias, herdadas da abertura: FOTO (gente idosa real, luz doméstica),
OBJETO (macro de coisa gasta, sem marca) e COLAGEM (recorte editorial com marcador
laranja, que é a família gráfica da referência).
"""
import json, os
S = os.path.dirname(os.path.abspath(__file__))

MEC = {
"B01":("FOTO","an elderly woman in her seventies reading a handwritten letter at a kitchen table, morning light, moved expression"),
"B02":("COLAGEM","a stack of cut-out handwritten letters and note cards fanned across the frame, a few circled with an orange marker"),
"B03":("FOTO","a doctor's hands leafing through a thick paper file of patient notes on a desk, reading glasses beside it"),
"B04":("COLAGEM","a torn calendar strip showing two and three months, marked with orange marker arrows"),
"B05":("FOTO","a man in his late sixties pausing mid-thought at a desk, eyebrows raised in genuine surprise, home office"),
"B06":("OBJETO","a single amber glass dropper bottle standing alone on a breakfast table beside a coffee cup, morning light"),
"B07":("OBJETO","a hand holding a glass dropper above a spoon at a breakfast table, one drop hanging"),
"B08":("FOTO","an older couple at a dining table, the wife pointing at something on the table while the husband listens"),
"B09":("COLAGEM","three cut-out plates of food arranged in a row with orange marker arrows pointing from each toward a cut-out brain illustration"),
"B10":("FOTO","a close shot of an older man eating a home-cooked lunch at a kitchen table, fork mid-air, warm light"),
"B11":("FOTO","a macro of a brain model on a desk with tiny points of light travelling along its folds, dark study"),
"B12":("OBJETO","an electrician's worn hands twisting two copper wires together, close macro, warm work light"),
"B13":("FOTO","an elderly woman looking up from a photo album with sudden clear recognition on her face"),
"B14":("FOTO","an older man greeting a neighbour over a garden fence, saying their name with confidence"),
"B15":("FOTO","a grandfather telling a long story to two grandchildren on a porch step, hands gesturing"),
"B16":("OBJETO","a finger snapping, frozen mid-snap, against a plain warm-grey background, macro"),
"B17":("COLAGEM","cut-out botanical leaves and roots arranged in a neat circle, orange marker check mark drawn over them"),
"B18":("OBJETO","a cup of herbal tea steaming on a wooden table beside a folded newspaper, soft window light"),
"B19":("FOTO","an older woman drinking tea at her kitchen window, calm and unhurried, late afternoon"),
"B20":("FOTO","a woman in her early eighties sitting in a bright Arizona living room, about to speak to camera, adobe wall behind"),
}
OFE = {
"B01":("OBJETO","three glass dropper bottles standing in a row on a kitchen shelf, morning light"),
"B02":("OBJETO","an empty glass dropper bottle lying on its side on a bathroom counter, last drop gone"),
"B03":("COLAGEM","cut-out warehouse shelves with most slots empty, a few remaining boxes circled in orange marker"),
"B04":("FOTO","a warehouse manager in his fifties on the phone in a half-empty stockroom, clipboard in hand"),
"B05":("COLAGEM","a torn calendar strip of five months in a row with an orange marker arrow stretching across all of them"),
"B06":("FOTO","young green shoots growing in dark soil in a greenhouse tray, shallow focus, patient and slow"),
"B07":("COLAGEM","a cut-out progress bar stopped at the halfway point, the unfinished half struck through with orange marker"),
"B08":("FOTO","a man in his sixties lying awake in bed at night, eyes open, faint window light on his face"),
"B09":("FOTO","a family photograph frame on a hallway table showing a father, a mother and a grown child"),
"B10":("FOTO","an elderly person sitting alone on a sofa in a dim living room, seen from the doorway, left behind"),
"B11":("OBJETO","a cardboard shipping box open on a packing table with tissue paper and a packing slip"),
"B12":("OBJETO","a roll of packing tape and a shipping label on a worn packing bench, macro"),
"B13":("COLAGEM","cut-out icons of a box and a delivery van with orange marker check marks drawn over both"),
"B14":("FOTO","a middle-aged daughter with her arm around her elderly mother on a porch, both calm"),
"B15":("FOTO","an elderly couple holding hands across a kitchen table, only the hands in frame"),
"B16":("COLAGEM","cut-out portraits of several older people arranged in a grid, the centre one circled in orange marker"),
"B17":("FOTO","a woman in her seventies at a laptop on a kitchen table, hand on the mouse, decided expression"),
"B18":("OBJETO","a plain kraft shipping box on a doorstep in morning light, no printing on it"),
"B19":("COLAGEM","cut-out paper price tags scattered across the frame, one of them circled heavily with orange marker"),
"B20":("OBJETO","a single worn leather wallet closed on a wooden table, macro, nothing taken out of it"),
"B21":("FOTO","a warehouse worker sealing a box on a packing line, seen over the shoulder"),
"B22":("OBJETO","extra glass dropper bottles being nested into a shipping box with tissue paper, hands only"),
"B23":("OBJETO","a sealed shipping box sliding along a warehouse conveyor, motion blur behind it"),
"B24":("FOTO","a woman in her late sixties signing for a delivery at her front door, relieved smile"),
"B25":("OBJETO","an older person's index finger about to press a key on a laptop, macro, warm light"),
"B26":("FOTO","an elderly man opening a delivery box on his kitchen counter, morning light through the window"),
"B27":("FOTO","a dinner table set for two in the evening, a plate served, warm lamp light"),
"B28":("COLAGEM","cut-out portraits of six older people arranged around the frame, orange marker quotation marks drawn beside them"),
}
json.dump({"05_MEDICO_MECANISMO":MEC,"07_MEDICO_OFERTA":OFE}, open(f"{S}/broll_novos.json","w"), indent=1)
from collections import Counter
for sec,d in [("MECANISMO",MEC),("OFERTA",OFE)]:
    c=Counter(v[0] for v in d.values())
    print(f"{sec}: {len(d)} planos -> {dict(c)}")
print("total:", len(MEC)+len(OFE))
