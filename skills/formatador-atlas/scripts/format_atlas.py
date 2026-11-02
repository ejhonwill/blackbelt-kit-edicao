#!/usr/bin/env python3
"""
Formatador Atlas — Gera .docx premium para dissecações de VSL
Uso: python format_atlas.py <meta.json> <mod1.md> <mod2.md> <mod3.md> <mod4.md> <output.docx>
"""

import json, sys, re, os
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from lxml import etree

# ─── COLOR SCHEME ─────────────────────────────────────────────
class C:
    """Color constants"""
    # Module colors: (dark, light, accent)
    MOD1 = ('1B4F72', 'D4E6F1', '2E86C1')  # Lead - Blue
    MOD2 = ('1E8449', 'D5F5E3', '27AE60')  # Storytelling - Green
    MOD3 = ('7D6608', 'FEF9E7', 'F39C12')  # Tese - Gold
    MOD4 = ('922B21', 'FADBD8', 'E74C3C')  # Fechamento - Red
    DASH = ('2C3E50', 'ECF0F1', '3498DB')  # Dashboard - Navy
    WHITE = 'FFFFFF'
    BLACK = '1A1A1A'
    GRAY = 'F8F9FA'
    GRAY_MED = 'BDC3C7'
    GRAY_DARK = '7F8C8D'

MODULE_COLORS = [C.MOD1, C.MOD2, C.MOD3, C.MOD4]
MODULE_NAMES = [
    'DISSECAÇÃO DA LEAD',
    'DISSECAÇÃO DO STORYTELLING',
    'DISSECAÇÃO DA TESE DE MARKETING',
    'DISSECAÇÃO DO FECHAMENTO / OFERTA'
]

def rgb(hex_color):
    return RGBColor(int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))

def set_cell_shading(cell, color):
    """Set cell background color"""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_border(cell, **kwargs):
    """Set cell borders: top, bottom, left, right with (size, color)"""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}></w:tcBorders>')
    for edge, (size, color) in kwargs.items():
        border = parse_xml(
            f'<w:{edge} {nsdecls("w")} w:val="single" w:sz="{size}" w:space="0" w:color="{color}"/>'
        )
        tcBorders.append(border)
    tcPr.append(tcBorders)

def set_paragraph_border_left(paragraph, color, size=12):
    """Add left border to paragraph"""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="{size}" w:space="6" w:color="{color}"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)

def set_paragraph_shading(paragraph, color):
    """Add background shading to paragraph"""
    pPr = paragraph._p.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}" w:val="clear"/>')
    pPr.append(shd)

def set_paragraph_border_bottom(paragraph, color, size=4):
    """Add bottom border to paragraph"""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="{size}" w:space="4" w:color="{color}"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)

def set_paragraph_borders(paragraph, color, size=4):
    """Add all borders to paragraph"""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{size}" w:space="4" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{size}" w:space="4" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="{int(size*1.5)}" w:space="6" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="{size}" w:space="4" w:color="{color}"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)


# ─── TEXT FORMATTING ──────────────────────────────────────────
def add_formatted_run(paragraph, text, bold=False, italic=False, size=11, color=C.BLACK, font='Arial'):
    """Add a formatted run to a paragraph"""
    run = paragraph.add_run(text)
    run.font.name = font
    run.font.size = Pt(size)
    run.font.color.rgb = rgb(color)
    run.bold = bold
    run.italic = italic
    return run

def add_inline_formatted_text(paragraph, text, base_bold=False, base_size=11, base_color=C.BLACK):
    """Parse **bold** and *italic* markdown inline formatting"""
    # Process bold first, then italic within segments
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            inner = part[2:-2]
            add_formatted_run(paragraph, inner, bold=True, size=base_size, color=base_color)
        else:
            # Check for italic
            sub_parts = re.split(r'(\*[^*]+\*)', part)
            for sub in sub_parts:
                if sub.startswith('*') and sub.endswith('*') and not sub.startswith('**'):
                    inner = sub[1:-1]
                    add_formatted_run(paragraph, inner, italic=True, bold=base_bold, size=base_size, color=base_color)
                else:
                    if sub:
                        add_formatted_run(paragraph, sub, bold=base_bold, size=base_size, color=base_color)


# ─── DOCUMENT BUILDER ─────────────────────────────────────────
class AtlasDocBuilder:
    def __init__(self, meta, modules_md):
        self.meta = meta
        self.modules_md = modules_md
        self.doc = Document()
        self._setup_styles()

    def _setup_styles(self):
        """Configure document styles"""
        style = self.doc.styles['Normal']
        style.font.name = 'Arial'
        style.font.size = Pt(11)
        style.font.color.rgb = rgb(C.BLACK)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.space_before = Pt(3)

        # Page setup
        section = self.doc.sections[0]
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    def build(self, output_path):
        """Build the complete document"""
        self._add_cover()
        self._add_dashboard()
        self._add_flow_map()
        self._add_toc()

        for i in range(4):
            self._add_module_divider(i)
            self._add_module_content(i)

        self.doc.save(output_path)
        size_kb = os.path.getsize(output_path) / 1024
        print(f"Document created: {output_path}")
        print(f"Size: {size_kb:.1f} KB")

    # ─── COVER PAGE ───────────────────────────────────────────
    def _add_cover(self):
        # Spacer
        for _ in range(6):
            self.doc.add_paragraph()

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_formatted_run(p, 'DISSECAÇÃO COMPLETA DE VSL', bold=True, size=26, color=C.DASH[0])

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_border_bottom(p, C.DASH[2], 6)
        add_formatted_run(p, self.meta.get('vsl_name', 'VSL'), bold=True, size=22, color=C.DASH[2])

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_formatted_run(p, self.meta.get('product_type', ''), size=14, color=C.GRAY_DARK)

        self.doc.add_paragraph()

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_formatted_run(p, 'Agente Atlas — Dissecação Profunda', size=12, color=C.GRAY_DARK, italic=True)

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_formatted_run(p, self.meta.get('date', ''), size=11, color=C.GRAY_DARK)

        self.doc.add_page_break()

    # ─── DASHBOARD ────────────────────────────────────────────
    def _add_dashboard(self):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(16)
        set_paragraph_border_bottom(p, C.DASH[2], 4)
        add_formatted_run(p, 'FICHA TÉCNICA DA VSL', bold=True, size=16, color=C.DASH[0])

        items = [
            ('VSL / PRODUTO', f"{self.meta.get('vsl_name', 'N/A')} — {self.meta.get('product_type', '')}"),
            ('DATA', self.meta.get('date', 'N/A')),
            ('FORMATO DA LEAD', self.meta.get('formato_lead', 'N/A')),
            ('TOM DOMINANTE', self.meta.get('tom', 'N/A')),
            ('FOCO', self.meta.get('foco', 'N/A')),
            ('MUP (MECANISMO DO PROBLEMA)', self.meta.get('mup', 'N/A')),
            ('MUS (MECANISMO DA SOLUÇÃO)', self.meta.get('mus', 'N/A')),
            ('NOME CHICLETE — PROBLEMA', self.meta.get('nome_chiclete_problema', 'N/A')),
            ('NOME CHICLETE — SOLUÇÃO', self.meta.get('nome_chiclete_solucao', 'N/A')),
            ('INGREDIENTES HERO', ', '.join(self.meta.get('ingredientes_hero', []))),
            ('SUPERESTRUTURAS', ', '.join(self.meta.get('superestruturas', []))),
            ('VARIANTES DE LEAD', str(self.meta.get('lead_variants', 'N/A'))),
            ('PREMISSAS / LOGIC POINTS', f"{self.meta.get('total_premissas', '—')} premissas / {self.meta.get('total_logic_points', '—')} logic points"),
            ('BLOCOS LEAD / FECHAMENTO', f"{self.meta.get('total_blocos_lead', '—')} blocos lead / {self.meta.get('total_blocos_fechamento', '—')} blocos fechamento"),
        ]

        table = self.doc.add_table(rows=len(items), cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        for i, (label, value) in enumerate(items):
            row = table.rows[i]
            # Label cell
            cell_l = row.cells[0]
            cell_l.width = Inches(2.2)
            set_cell_shading(cell_l, C.DASH[0])
            p = cell_l.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            add_formatted_run(p, label, bold=True, size=9, color=C.WHITE)

            # Value cell
            cell_v = row.cells[1]
            cell_v.width = Inches(4.3)
            bg = C.DASH[1] if i % 2 == 0 else C.WHITE
            set_cell_shading(cell_v, bg)
            p = cell_v.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            add_formatted_run(p, value, size=10, color=C.BLACK)

        # Personagens
        personagens = self.meta.get('personagens', [])
        if personagens:
            self.doc.add_paragraph()
            p = self.doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            add_formatted_run(p, 'PERSONAGENS PRINCIPAIS', bold=True, size=13, color=C.DASH[0])

            pt = self.doc.add_table(rows=1 + len(personagens), cols=3)
            pt.alignment = WD_TABLE_ALIGNMENT.CENTER
            pt.autofit = False

            # Header
            for ci, header in enumerate(['PERSONAGEM', 'TIPO', 'FUNÇÃO']):
                cell = pt.rows[0].cells[ci]
                set_cell_shading(cell, C.DASH[0])
                p = cell.paragraphs[0]
                add_formatted_run(p, header, bold=True, size=9, color=C.WHITE)

            # Data
            for ri, pers in enumerate(personagens):
                vals = [pers.get('nome', ''), pers.get('tipo', ''), pers.get('funcao_curta', '')]
                for ci, val in enumerate(vals):
                    cell = pt.rows[ri + 1].cells[ci]
                    bg = C.DASH[1] if ri % 2 == 0 else C.WHITE
                    set_cell_shading(cell, bg)
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    add_formatted_run(p, val, size=9, color=C.BLACK)

        self.doc.add_page_break()

    # ─── FLOW MAP ─────────────────────────────────────────────
    def _add_flow_map(self):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(16)
        add_formatted_run(p, 'MAPA DE FLUXO DA VSL', bold=True, size=16, color=C.DASH[0])

        flow = self.meta.get('flow_summary', {})
        stages = [
            ('LEAD', flow.get('lead', ''), C.MOD1),
            ('STORYTELLING', flow.get('storytelling', ''), C.MOD2),
            ('TESE', flow.get('tese', ''), C.MOD3),
            ('FECHAMENTO', flow.get('fechamento', ''), C.MOD4),
        ]

        # Header row
        ft = self.doc.add_table(rows=2, cols=4)
        ft.alignment = WD_TABLE_ALIGNMENT.CENTER
        ft.autofit = False

        for ci, (label, summary, colors) in enumerate(stages):
            # Label cell (top)
            cell = ft.rows[0].cells[ci]
            set_cell_shading(cell, colors[0])
            set_cell_border(cell, top=(6, colors[0]), bottom=(6, colors[0]), left=(6, colors[0]), right=(6, colors[0]))
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            add_formatted_run(p, label, bold=True, size=10, color=C.WHITE)

            # Summary cell (bottom)
            cell = ft.rows[1].cells[ci]
            set_cell_shading(cell, colors[1])
            set_cell_border(cell, top=(4, colors[2]), bottom=(4, colors[2]), left=(4, colors[2]), right=(4, colors[2]))
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            add_formatted_run(p, summary, size=8, color=colors[0])

        # Stats boxes
        self.doc.add_paragraph()
        stats = [
            (str(self.meta.get('total_premissas', '—')), 'Premissas', C.MOD3),
            (str(self.meta.get('total_logic_points', '—')), 'Logic Points', C.MOD3),
            (str(self.meta.get('total_blocos_lead', '—')), 'Blocos Lead', C.MOD1),
            (str(self.meta.get('total_blocos_fechamento', '—')), 'Blocos Fechamento', C.MOD4),
        ]

        st = self.doc.add_table(rows=2, cols=4)
        st.alignment = WD_TABLE_ALIGNMENT.CENTER
        st.autofit = False

        for ci, (value, label, colors) in enumerate(stats):
            # Value
            cell = st.rows[0].cells[ci]
            set_cell_shading(cell, colors[1])
            set_cell_border(cell, top=(4, colors[2]), left=(4, colors[2]), right=(4, colors[2]))
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(0)
            add_formatted_run(p, value, bold=True, size=18, color=colors[0])

            # Label
            cell = st.rows[1].cells[ci]
            set_cell_shading(cell, colors[1])
            set_cell_border(cell, bottom=(4, colors[2]), left=(4, colors[2]), right=(4, colors[2]))
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(4)
            add_formatted_run(p, label, size=8, color=C.GRAY_DARK)

        self.doc.add_page_break()

    # ─── TOC ──────────────────────────────────────────────────
    def _add_toc(self):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(20)
        add_formatted_run(p, 'SUMÁRIO', bold=True, size=16, color=C.DASH[0])

        # Add TOC field
        paragraph = self.doc.add_paragraph()
        run = paragraph.add_run()
        fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
        run._r.append(fldChar1)
        run2 = paragraph.add_run()
        instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText>')
        run2._r.append(instrText)
        run3 = paragraph.add_run()
        fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
        run3._r.append(fldChar2)
        run4 = paragraph.add_run('[Atualize o sumário: selecione, clique com botão direito → "Atualizar campo"]')
        run4.font.color.rgb = rgb(C.GRAY_DARK)
        run4.font.size = Pt(10)
        run4.italic = True
        run5 = paragraph.add_run()
        fldChar3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
        run5._r.append(fldChar3)

        self.doc.add_page_break()

    # ─── MODULE DIVIDER ───────────────────────────────────────
    def _add_module_divider(self, mod_index):
        colors = MODULE_COLORS[mod_index]

        for _ in range(6):
            self.doc.add_paragraph()

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_formatted_run(p, f'MÓDULO {mod_index + 1}', bold=True, size=14, color=C.GRAY_DARK)

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(12)
        set_paragraph_shading(p, colors[1])
        set_paragraph_borders(p, colors[2], 6)
        add_formatted_run(p, MODULE_NAMES[mod_index], bold=True, size=22, color=colors[0])

        self.doc.add_page_break()

    # ─── MODULE CONTENT (MARKDOWN PARSER) ─────────────────────
    def _add_module_content(self, mod_index):
        colors = MODULE_COLORS[mod_index]
        md = self.modules_md[mod_index]
        lines = md.split('\n')
        i = 0
        table_rows = []
        blockquote_lines = []

        def flush_blockquote():
            nonlocal blockquote_lines
            if blockquote_lines:
                text = ' '.join(blockquote_lines)
                text = text.replace('**', '').replace('"', '"').replace('"', '"')
                p = self.doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.3)
                p.paragraph_format.right_indent = Inches(0.3)
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(6)
                set_paragraph_border_left(p, colors[2], 10)
                set_paragraph_shading(p, C.GRAY)
                add_formatted_run(p, text, italic=True, size=10, color='555555', font='Georgia')
                blockquote_lines = []

        def flush_table():
            nonlocal table_rows
            if table_rows:
                self._add_formatted_table(table_rows, colors)
                table_rows = []

        while i < len(lines):
            line = lines[i]
            trimmed = line.strip()

            # Empty line
            if not trimmed:
                flush_blockquote()
                flush_table()
                i += 1
                continue

            # Horizontal rule
            if re.match(r'^-{3,}$', trimmed) or re.match(r'^\*{3,}$', trimmed):
                flush_blockquote()
                flush_table()
                i += 1
                continue

            # Table row
            if trimmed.startswith('|') and trimmed.endswith('|'):
                flush_blockquote()
                # Skip separator rows
                if re.match(r'^\|[\s\-:|]+\|$', trimmed):
                    i += 1
                    continue
                cells = [c.strip() for c in trimmed[1:-1].split('|')]
                table_rows.append(cells)
                i += 1
                continue
            elif table_rows:
                flush_table()

            # Blockquote
            if trimmed.startswith('> ') or trimmed == '>':
                flush_table()
                blockquote_lines.append(trimmed.lstrip('> ').strip())
                i += 1
                continue
            elif blockquote_lines:
                flush_blockquote()

            # Headings
            if trimmed.startswith('#### '):
                flush_table(); flush_blockquote()
                text = trimmed[5:]
                p = self.doc.add_paragraph()
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(4)
                add_inline_formatted_text(p, text, base_bold=True, base_size=11, base_color=colors[0])
                i += 1
                continue

            if trimmed.startswith('### ') and not trimmed.startswith('#### '):
                flush_table(); flush_blockquote()
                text = trimmed[4:]
                p = self.doc.add_heading(level=3)
                p.paragraph_format.space_before = Pt(12)
                p.paragraph_format.space_after = Pt(6)
                # Clear default run and add custom
                for r in p.runs:
                    r.text = ''
                add_inline_formatted_text(p, text, base_bold=True, base_size=12, base_color=colors[0])
                i += 1
                continue

            if trimmed.startswith('## ') and not trimmed.startswith('### '):
                flush_table(); flush_blockquote()
                text = trimmed[3:]
                p = self.doc.add_heading(level=2)
                p.paragraph_format.space_before = Pt(16)
                p.paragraph_format.space_after = Pt(8)
                set_paragraph_border_left(p, colors[2], 16)
                for r in p.runs:
                    r.text = ''
                add_formatted_run(p, text.replace('**', ''), bold=True, size=14, color=colors[2])
                i += 1
                continue

            if trimmed.startswith('# ') and not trimmed.startswith('## '):
                flush_table(); flush_blockquote()
                text = trimmed[2:]
                p = self.doc.add_heading(level=1)
                p.paragraph_format.space_before = Pt(20)
                p.paragraph_format.space_after = Pt(10)
                set_paragraph_shading(p, colors[1])
                set_paragraph_border_bottom(p, colors[2], 8)
                for r in p.runs:
                    r.text = ''
                add_formatted_run(p, text.replace('**', ''), bold=True, size=18, color=colors[0])
                i += 1
                continue

            # Combo detected
            if trimmed.startswith('**Combo detectado:**') or trimmed.startswith('**Combo detectado:'):
                flush_table(); flush_blockquote()
                content = re.sub(r'^\*\*Combo detectado:\*\*\s*', '', trimmed)
                p = self.doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.15)
                p.paragraph_format.right_indent = Inches(0.15)
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(10)
                set_paragraph_borders(p, colors[2], 4)
                set_paragraph_shading(p, colors[1])
                add_formatted_run(p, 'COMBO: ', bold=True, size=10, color=colors[0])
                add_formatted_run(p, content, size=10, color=C.BLACK)
                i += 1
                continue

            # Bullet point
            if trimmed.startswith('- ') or trimmed.startswith('* '):
                flush_table(); flush_blockquote()
                content = re.sub(r'^[-*]\s+', '', trimmed)
                p = self.doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.25)
                p.paragraph_format.first_line_indent = Inches(-0.15)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                add_formatted_run(p, '  \u2022  ', size=11, color=colors[2])
                add_inline_formatted_text(p, content, base_size=11, base_color=C.BLACK)
                i += 1
                continue

            # Numbered list
            num_match = re.match(r'^(\d+)\.\s+', trimmed)
            if num_match:
                flush_table(); flush_blockquote()
                content = re.sub(r'^\d+\.\s+', '', trimmed)
                p = self.doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.25)
                p.paragraph_format.first_line_indent = Inches(-0.2)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                add_formatted_run(p, f'{num_match.group(1)}.  ', bold=True, size=11, color=colors[2])
                add_inline_formatted_text(p, content, base_size=11, base_color=C.BLACK)
                i += 1
                continue

            # Logic points (A → B →)
            logic_match = re.match(r'^\*\*([A-Z])\s*[→→]\*\*\s*(.*)', trimmed)
            if logic_match:
                flush_table(); flush_blockquote()
                p = self.doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.15)
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                add_formatted_run(p, f'{logic_match.group(1)} → ', bold=True, size=11, color=colors[2])
                add_inline_formatted_text(p, logic_match.group(2), base_size=11, base_color=C.BLACK)
                i += 1
                continue

            # Regular paragraph
            flush_table(); flush_blockquote()
            p = self.doc.add_paragraph()
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            add_inline_formatted_text(p, trimmed, base_size=11, base_color=C.BLACK)
            i += 1

        flush_blockquote()
        flush_table()

    def _add_formatted_table(self, rows, colors):
        """Add a professionally formatted table"""
        if not rows:
            return

        num_cols = max(len(r) for r in rows)
        table = self.doc.add_table(rows=len(rows), cols=num_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = True

        for ri, row in enumerate(rows):
            is_header = ri == 0
            is_odd = ri % 2 == 1

            for ci in range(num_cols):
                cell_text = row[ci].strip() if ci < len(row) else ''
                cell = table.rows[ri].cells[ci]

                if is_header:
                    set_cell_shading(cell, colors[0])
                    text_color = C.WHITE
                elif is_odd:
                    set_cell_shading(cell, colors[1])
                    text_color = C.BLACK
                else:
                    set_cell_shading(cell, C.WHITE)
                    text_color = C.BLACK

                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                add_inline_formatted_text(p, cell_text, base_bold=is_header, base_size=9 if is_header else 10, base_color=text_color if is_header else C.BLACK)


# ─── MAIN ─────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 7:
        print('Usage: python format_atlas.py <meta.json> <mod1.md> <mod2.md> <mod3.md> <mod4.md> <output.docx>')
        sys.exit(1)

    meta_path, mod1, mod2, mod3, mod4, output = sys.argv[1:7]

    with open(meta_path, 'r') as f:
        meta = json.load(f)

    modules = []
    for path in [mod1, mod2, mod3, mod4]:
        with open(path, 'r') as f:
            modules.append(f.read())

    builder = AtlasDocBuilder(meta, modules)
    builder.build(output)

if __name__ == '__main__':
    main()
