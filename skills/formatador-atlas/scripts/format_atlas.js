#!/usr/bin/env node
/**
 * Formatador Atlas — Gera .docx premium para dissecações de VSL
 *
 * Uso: node format_atlas.js <meta.json> <mod1.md> <mod2.md> <mod3.md> <mod4.md> <output.docx>
 */

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, PageBreak
} = require('docx');

// ─── COLOR SCHEME ─────────────────────────────────────────────
const COLORS = {
  mod1: { dark: '1B4F72', light: 'D4E6F1', accent: '2E86C1', name: 'LEAD' },
  mod2: { dark: '1E8449', light: 'D5F5E3', accent: '27AE60', name: 'STORYTELLING' },
  mod3: { dark: '7D6608', light: 'FEF9E7', accent: 'F39C12', name: 'TESE DE MARKETING' },
  mod4: { dark: '922B21', light: 'FADBD8', accent: 'E74C3C', name: 'FECHAMENTO / OFERTA' },
  dash: { dark: '2C3E50', medium: '34495E', light: 'ECF0F1', accent: '3498DB' },
  white: 'FFFFFF',
  black: '1A1A1A',
  gray: 'F8F9FA',
  grayMed: 'BDC3C7',
  grayDark: '7F8C8D'
};

const MODULE_COLORS = [COLORS.mod1, COLORS.mod2, COLORS.mod3, COLORS.mod4];

// ─── CONSTANTS ────────────────────────────────────────────────
const PAGE_WIDTH = 12240;
const MARGIN = 1440;
const CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN); // 9360
const BORDER_NONE = { style: BorderStyle.NONE, size: 0 };
const BORDERS_NONE = { top: BORDER_NONE, bottom: BORDER_NONE, left: BORDER_NONE, right: BORDER_NONE };

function thinBorder(color = 'CCCCCC') {
  const b = { style: BorderStyle.SINGLE, size: 1, color };
  return { top: b, bottom: b, left: b, right: b };
}

function cellMargins() {
  return { top: 60, bottom: 60, left: 100, right: 100 };
}

// ─── PARSE ARGS ───────────────────────────────────────────────
const args = process.argv.slice(2);
if (args.length < 6) {
  console.error('Usage: node format_atlas.js <meta.json> <mod1.md> <mod2.md> <mod3.md> <mod4.md> <output.docx>');
  process.exit(1);
}

const [metaPath, mod1Path, mod2Path, mod3Path, mod4Path, outputPath] = args;
const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
const modules = [mod1Path, mod2Path, mod3Path, mod4Path].map(p => fs.readFileSync(p, 'utf8'));

// ─── MARKDOWN PARSER ──────────────────────────────────────────
function parseMarkdownToElements(md, moduleColor) {
  const lines = md.split('\n');
  const elements = [];
  let i = 0;
  let inTable = false;
  let tableRows = [];
  let inBlockquote = false;
  let blockquoteLines = [];

  function flushBlockquote() {
    if (blockquoteLines.length > 0) {
      elements.push(createQuoteBlock(blockquoteLines.join(' '), moduleColor));
      blockquoteLines = [];
      inBlockquote = false;
    }
  }

  function flushTable() {
    if (tableRows.length > 0) {
      elements.push(createFormattedTable(tableRows, moduleColor));
      tableRows = [];
      inTable = false;
    }
  }

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // Empty line
    if (trimmed === '') {
      flushBlockquote();
      flushTable();
      i++;
      continue;
    }

    // Horizontal rule
    if (/^-{3,}$/.test(trimmed) || /^\*{3,}$/.test(trimmed)) {
      flushBlockquote();
      flushTable();
      // Skip — we use module-colored spacing instead of HR lines
      i++;
      continue;
    }

    // Table row
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      flushBlockquote();
      // Skip separator rows
      if (/^\|[\s\-:|]+\|$/.test(trimmed)) {
        i++;
        continue;
      }
      const cells = trimmed.slice(1, -1).split('|').map(c => c.trim());
      if (!inTable) {
        inTable = true;
      }
      tableRows.push(cells);
      i++;
      continue;
    } else if (inTable) {
      flushTable();
    }

    // Blockquote
    if (trimmed.startsWith('> ') || trimmed === '>') {
      flushTable();
      inBlockquote = true;
      blockquoteLines.push(trimmed.replace(/^>\s?/, ''));
      i++;
      continue;
    } else if (inBlockquote) {
      flushBlockquote();
    }

    // Heading H1
    if (trimmed.startsWith('# ') && !trimmed.startsWith('## ')) {
      flushTable();
      flushBlockquote();
      const text = trimmed.replace(/^#\s+/, '');
      elements.push(createModuleHeading(text, moduleColor, HeadingLevel.HEADING_1));
      i++;
      continue;
    }

    // Heading H2
    if (trimmed.startsWith('## ') && !trimmed.startsWith('### ')) {
      flushTable();
      flushBlockquote();
      const text = trimmed.replace(/^##\s+/, '');
      elements.push(createSectionHeading(text, moduleColor, HeadingLevel.HEADING_2));
      i++;
      continue;
    }

    // Heading H3
    if (trimmed.startsWith('### ') && !trimmed.startsWith('#### ')) {
      flushTable();
      flushBlockquote();
      const text = trimmed.replace(/^###\s+/, '');
      elements.push(createSubHeading(text, moduleColor, HeadingLevel.HEADING_3));
      i++;
      continue;
    }

    // Heading H4
    if (trimmed.startsWith('#### ')) {
      flushTable();
      flushBlockquote();
      const text = trimmed.replace(/^####\s+/, '');
      elements.push(new Paragraph({
        spacing: { before: 160, after: 80 },
        children: parseInlineFormatting(text, { bold: true, size: 22, color: moduleColor.dark, font: 'Arial' })
      }));
      i++;
      continue;
    }

    // Combo detected line
    if (trimmed.startsWith('**Combo detectado:**') || trimmed.startsWith('**Combo detectado:')) {
      flushTable();
      flushBlockquote();
      elements.push(createComboBlock(trimmed, moduleColor));
      i++;
      continue;
    }

    // Regular paragraph (with inline formatting)
    flushTable();
    flushBlockquote();
    elements.push(createParagraph(trimmed, moduleColor));
    i++;
  }

  flushBlockquote();
  flushTable();

  return elements;
}

// ─── INLINE FORMATTING ──────────────────────────────────────
function parseInlineFormatting(text, baseStyle = {}) {
  const runs = [];
  // Simple regex-based bold/italic parser
  const regex = /\*\*([^*]+)\*\*|__([^_]+)__|_([^_]+)_|\*([^*]+)\*/g;
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(text)) !== null) {
    // Add text before match
    if (match.index > lastIndex) {
      runs.push(new TextRun({
        text: text.slice(lastIndex, match.index),
        font: 'Arial',
        size: 22,
        ...baseStyle
      }));
    }

    const boldText = match[1] || match[2];
    const italicText = match[3] || match[4];

    if (boldText) {
      runs.push(new TextRun({
        text: boldText,
        bold: true,
        font: 'Arial',
        size: 22,
        ...baseStyle
      }));
    } else if (italicText) {
      runs.push(new TextRun({
        text: italicText,
        italics: true,
        font: 'Arial',
        size: 22,
        ...baseStyle
      }));
    }

    lastIndex = regex.lastIndex;
  }

  // Add remaining text
  if (lastIndex < text.length) {
    runs.push(new TextRun({
      text: text.slice(lastIndex),
      font: 'Arial',
      size: 22,
      ...baseStyle
    }));
  }

  if (runs.length === 0) {
    runs.push(new TextRun({ text, font: 'Arial', size: 22, ...baseStyle }));
  }

  return runs;
}

// ─── HEADING CREATORS ─────────────────────────────────────────
function createModuleHeading(text, color, level) {
  return new Paragraph({
    heading: level,
    spacing: { before: 360, after: 200 },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 6, color: color.accent, space: 4 }
    },
    shading: { fill: color.light, type: ShadingType.CLEAR },
    children: [
      new TextRun({
        text: text,
        bold: true,
        size: 36,
        color: color.dark,
        font: 'Arial'
      })
    ]
  });
}

function createSectionHeading(text, color, level) {
  return new Paragraph({
    heading: level,
    spacing: { before: 280, after: 160 },
    border: {
      left: { style: BorderStyle.SINGLE, size: 12, color: color.accent, space: 6 }
    },
    children: [
      new TextRun({
        text: text,
        bold: true,
        size: 28,
        color: color.accent,
        font: 'Arial'
      })
    ]
  });
}

function createSubHeading(text, color, level) {
  return new Paragraph({
    heading: level,
    spacing: { before: 200, after: 120 },
    children: parseInlineFormatting(text, { bold: true, size: 24, color: color.dark, font: 'Arial' })
  });
}

// ─── BLOCKQUOTE ──────────────────────────────────────────────
function createQuoteBlock(text, color) {
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    indent: { left: 400, right: 400 },
    border: {
      left: { style: BorderStyle.SINGLE, size: 8, color: color.accent, space: 8 },
      top: BORDER_NONE, bottom: BORDER_NONE, right: BORDER_NONE
    },
    shading: { fill: COLORS.gray, type: ShadingType.CLEAR },
    children: [
      new TextRun({
        text: text.replace(/\*\*/g, '').replace(/"/g, '"').replace(/"/g, '"'),
        italics: true,
        size: 20,
        color: '555555',
        font: 'Georgia'
      })
    ]
  });
}

// ─── COMBO BLOCK ─────────────────────────────────────────────
function createComboBlock(text, color) {
  const content = text.replace(/^\*\*Combo detectado:\*\*\s*/, '');
  return new Paragraph({
    spacing: { before: 100, after: 160 },
    indent: { left: 200, right: 200 },
    border: {
      top: { style: BorderStyle.SINGLE, size: 2, color: color.accent },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: color.accent },
      left: { style: BorderStyle.SINGLE, size: 6, color: color.accent },
      right: { style: BorderStyle.SINGLE, size: 2, color: color.accent }
    },
    shading: { fill: color.light, type: ShadingType.CLEAR },
    children: [
      new TextRun({ text: 'COMBO: ', bold: true, size: 20, color: color.dark, font: 'Arial' }),
      new TextRun({ text: content, size: 20, color: COLORS.black, font: 'Arial' })
    ]
  });
}

// ─── PARAGRAPH ───────────────────────────────────────────────
function createParagraph(text, color) {
  // Detect bullet points
  if (text.startsWith('- ') || text.startsWith('* ')) {
    const content = text.replace(/^[-*]\s+/, '');
    return new Paragraph({
      spacing: { before: 40, after: 40 },
      indent: { left: 360, hanging: 200 },
      children: [
        new TextRun({ text: '  \u2022  ', font: 'Arial', size: 22, color: color.accent }),
        ...parseInlineFormatting(content, { color: COLORS.black })
      ]
    });
  }

  // Detect numbered items (1. 2. etc or A → B → etc)
  const numMatch = text.match(/^(\d+)\.\s+/);
  if (numMatch) {
    const content = text.replace(/^\d+\.\s+/, '');
    return new Paragraph({
      spacing: { before: 40, after: 40 },
      indent: { left: 360, hanging: 300 },
      children: [
        new TextRun({ text: `${numMatch[1]}.  `, bold: true, font: 'Arial', size: 22, color: color.accent }),
        ...parseInlineFormatting(content, { color: COLORS.black })
      ]
    });
  }

  // Logic point (A → B →)
  const logicMatch = text.match(/^\*\*([A-Z])\s*[→→]\*\*\s*(.*)/);
  if (logicMatch) {
    return new Paragraph({
      spacing: { before: 60, after: 60 },
      indent: { left: 200 },
      children: [
        new TextRun({ text: `${logicMatch[1]} → `, bold: true, font: 'Arial', size: 22, color: color.accent }),
        ...parseInlineFormatting(logicMatch[2], { color: COLORS.black })
      ]
    });
  }

  return new Paragraph({
    spacing: { before: 80, after: 80 },
    children: parseInlineFormatting(text, { color: COLORS.black })
  });
}

// ─── TABLE CREATOR ──────────────────────────────────────────
function createFormattedTable(rows, color) {
  if (rows.length === 0) return new Paragraph({ children: [] });

  const numCols = Math.max(...rows.map(r => r.length));
  const colWidth = Math.floor(CONTENT_WIDTH / numCols);
  const columnWidths = Array(numCols).fill(colWidth);
  // Adjust last column to fill remainder
  columnWidths[numCols - 1] = CONTENT_WIDTH - (colWidth * (numCols - 1));

  const tableRows = rows.map((row, rowIndex) => {
    const isHeader = rowIndex === 0;
    const isOddRow = rowIndex % 2 === 1;

    const cells = [];
    for (let c = 0; c < numCols; c++) {
      const cellText = (row[c] || '').trim();
      const bgColor = isHeader ? color.dark : (isOddRow ? color.light : COLORS.white);
      const textColor = isHeader ? COLORS.white : COLORS.black;

      cells.push(new TableCell({
        borders: thinBorder(isHeader ? color.dark : COLORS.grayMed),
        width: { size: columnWidths[c], type: WidthType.DXA },
        shading: { fill: bgColor, type: ShadingType.CLEAR },
        margins: cellMargins(),
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({
          spacing: { before: 40, after: 40 },
          children: parseInlineFormatting(cellText, {
            bold: isHeader,
            size: isHeader ? 20 : 20,
            color: textColor,
            font: 'Arial'
          })
        })]
      }));
    }

    return new TableRow({ children: cells });
  });

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths,
    rows: tableRows
  });
}

// ─── DASHBOARD (FICHA TÉCNICA) ───────────────────────────────
function createDashboard(meta) {
  const elements = [];

  // Title: "FICHA TÉCNICA"
  elements.push(new Paragraph({
    spacing: { before: 200, after: 200 },
    alignment: AlignmentType.CENTER,
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.dash.accent, space: 6 }
    },
    children: [
      new TextRun({ text: 'FICHA TÉCNICA DA VSL', bold: true, size: 32, color: COLORS.dash.dark, font: 'Arial' })
    ]
  }));

  // Dashboard table: 2 columns (label | value)
  const dashItems = [
    ['VSL / PRODUTO', `${meta.vsl_name || 'N/A'} — ${meta.product_type || ''}`],
    ['DATA', meta.date || 'N/A'],
    ['FORMATO DA LEAD', meta.formato_lead || 'N/A'],
    ['TOM DOMINANTE', meta.tom || 'N/A'],
    ['FOCO', meta.foco || 'N/A'],
    ['MUP (MECANISMO DO PROBLEMA)', meta.mup || 'N/A'],
    ['MUS (MECANISMO DA SOLUÇÃO)', meta.mus || 'N/A'],
    ['NOME CHICLETE — PROBLEMA', meta.nome_chiclete_problema || 'N/A'],
    ['NOME CHICLETE — SOLUÇÃO', meta.nome_chiclete_solucao || 'N/A'],
    ['INGREDIENTES HERO', (meta.ingredientes_hero || []).join(', ') || 'N/A'],
    ['SUPERESTRUTURAS', (meta.superestruturas || []).join(', ') || 'N/A'],
    ['VARIANTES DE LEAD', String(meta.lead_variants || 'N/A')],
    ['TOTAL PREMISSAS', String(meta.total_premissas || 'N/A')],
    ['TOTAL LOGIC POINTS', String(meta.total_logic_points || 'N/A')],
    ['BLOCOS DE LEAD', String(meta.total_blocos_lead || 'N/A')],
    ['BLOCOS DE FECHAMENTO', String(meta.total_blocos_fechamento || 'N/A')]
  ];

  const labelWidth = 3200;
  const valueWidth = CONTENT_WIDTH - labelWidth;

  const dashRows = dashItems.map(([label, value], idx) => {
    const isAlt = idx % 2 === 0;
    return new TableRow({
      children: [
        new TableCell({
          borders: thinBorder(COLORS.dash.dark),
          width: { size: labelWidth, type: WidthType.DXA },
          shading: { fill: COLORS.dash.dark, type: ShadingType.CLEAR },
          margins: cellMargins(),
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            children: [new TextRun({ text: label, bold: true, size: 18, color: COLORS.white, font: 'Arial' })]
          })]
        }),
        new TableCell({
          borders: thinBorder(COLORS.grayMed),
          width: { size: valueWidth, type: WidthType.DXA },
          shading: { fill: isAlt ? COLORS.dash.light : COLORS.white, type: ShadingType.CLEAR },
          margins: cellMargins(),
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            children: [new TextRun({ text: value, size: 20, color: COLORS.black, font: 'Arial' })]
          })]
        })
      ]
    });
  });

  elements.push(new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [labelWidth, valueWidth],
    rows: dashRows
  }));

  // Personagens table
  if (meta.personagens && meta.personagens.length > 0) {
    elements.push(new Paragraph({ spacing: { before: 300, after: 120 }, children: [
      new TextRun({ text: 'PERSONAGENS PRINCIPAIS', bold: true, size: 26, color: COLORS.dash.dark, font: 'Arial' })
    ]}));

    const pCols = 3;
    const pColW = Math.floor(CONTENT_WIDTH / pCols);
    const pColWidths = [pColW, pColW, CONTENT_WIDTH - (pColW * 2)];

    const pHeader = new TableRow({
      children: ['PERSONAGEM', 'TIPO', 'FUNÇÃO'].map((h, ci) => new TableCell({
        borders: thinBorder(COLORS.dash.dark),
        width: { size: pColWidths[ci], type: WidthType.DXA },
        shading: { fill: COLORS.dash.medium, type: ShadingType.CLEAR },
        margins: cellMargins(),
        children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, size: 18, color: COLORS.white, font: 'Arial' })] })]
      }))
    });

    const pRows = meta.personagens.map((p, ri) => new TableRow({
      children: [p.nome || '', p.tipo || '', p.funcao_curta || ''].map((v, ci) => new TableCell({
        borders: thinBorder(COLORS.grayMed),
        width: { size: pColWidths[ci], type: WidthType.DXA },
        shading: { fill: ri % 2 === 0 ? COLORS.dash.light : COLORS.white, type: ShadingType.CLEAR },
        margins: cellMargins(),
        children: [new Paragraph({ children: [new TextRun({ text: v, size: 20, color: COLORS.black, font: 'Arial' })] })]
      }))
    }));

    elements.push(new Table({
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
      columnWidths: pColWidths,
      rows: [pHeader, ...pRows]
    }));
  }

  return elements;
}

// ─── FLOW MAP ────────────────────────────────────────────────
function createFlowMap(meta) {
  const elements = [];

  elements.push(new Paragraph({
    spacing: { before: 300, after: 200 },
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({ text: 'MAPA DE FLUXO DA VSL', bold: true, size: 32, color: COLORS.dash.dark, font: 'Arial' })
    ]
  }));

  const flow = meta.flow_summary || {};
  const stages = [
    { label: 'LEAD', summary: flow.lead || '', color: COLORS.mod1 },
    { label: 'STORYTELLING', summary: flow.storytelling || '', color: COLORS.mod2 },
    { label: 'TESE', summary: flow.tese || '', color: COLORS.mod3 },
    { label: 'FECHAMENTO', summary: flow.fechamento || '', color: COLORS.mod4 }
  ];

  // Create flow as a table: 4 colored cells with arrows between
  const cellWidth = Math.floor(CONTENT_WIDTH / 4);
  const colWidths = [cellWidth, cellWidth, cellWidth, CONTENT_WIDTH - (cellWidth * 3)];

  const headerRow = new TableRow({
    children: stages.map((s, ci) => new TableCell({
      borders: {
        top: { style: BorderStyle.SINGLE, size: 3, color: s.color.dark },
        bottom: { style: BorderStyle.SINGLE, size: 3, color: s.color.dark },
        left: { style: BorderStyle.SINGLE, size: 3, color: s.color.dark },
        right: { style: BorderStyle.SINGLE, size: 3, color: s.color.dark }
      },
      width: { size: colWidths[ci], type: WidthType.DXA },
      shading: { fill: s.color.dark, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 80, right: 80 },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: s.label, bold: true, size: 20, color: COLORS.white, font: 'Arial' })]
      })]
    }))
  });

  // Arrow row
  const arrowRow = new TableRow({
    children: stages.map((s, ci) => new TableCell({
      borders: BORDERS_NONE,
      width: { size: colWidths[ci], type: WidthType.DXA },
      shading: { fill: COLORS.white, type: ShadingType.CLEAR },
      margins: { top: 20, bottom: 20, left: 40, right: 40 },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: ci < 3 ? '\u25BC' : '\u25BC', size: 18, color: s.color.accent, font: 'Arial' })]
      })]
    }))
  });

  // Summary row
  const summaryRow = new TableRow({
    children: stages.map((s, ci) => new TableCell({
      borders: {
        top: { style: BorderStyle.SINGLE, size: 2, color: s.color.accent },
        bottom: { style: BorderStyle.SINGLE, size: 2, color: s.color.accent },
        left: { style: BorderStyle.SINGLE, size: 2, color: s.color.accent },
        right: { style: BorderStyle.SINGLE, size: 2, color: s.color.accent }
      },
      width: { size: colWidths[ci], type: WidthType.DXA },
      shading: { fill: s.color.light, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 80, right: 80 },
      verticalAlign: VerticalAlign.TOP,
      children: [new Paragraph({
        spacing: { before: 0, after: 0 },
        children: [new TextRun({ text: s.summary, size: 16, color: s.color.dark, font: 'Arial' })]
      })]
    }))
  });

  elements.push(new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, arrowRow, summaryRow]
  }));

  // Stats row below flow map
  elements.push(new Paragraph({ spacing: { before: 200, after: 60 }, children: [] }));

  const statsItems = [
    { label: 'Premissas', value: String(meta.total_premissas || '—'), color: COLORS.mod3 },
    { label: 'Logic Points', value: String(meta.total_logic_points || '—'), color: COLORS.mod3 },
    { label: 'Blocos Lead', value: String(meta.total_blocos_lead || '—'), color: COLORS.mod1 },
    { label: 'Blocos Fechamento', value: String(meta.total_blocos_fechamento || '—'), color: COLORS.mod4 }
  ];

  const sColWidth = Math.floor(CONTENT_WIDTH / 4);
  const sColWidths = [sColWidth, sColWidth, sColWidth, CONTENT_WIDTH - (sColWidth * 3)];

  const statsRow = new TableRow({
    children: statsItems.map((s, ci) => new TableCell({
      borders: thinBorder(s.color.accent),
      width: { size: sColWidths[ci], type: WidthType.DXA },
      shading: { fill: s.color.light, type: ShadingType.CLEAR },
      margins: { top: 60, bottom: 60, left: 60, right: 60 },
      verticalAlign: VerticalAlign.CENTER,
      children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 20 },
          children: [new TextRun({ text: s.value, bold: true, size: 28, color: s.color.dark, font: 'Arial' })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: s.label, size: 16, color: COLORS.grayDark, font: 'Arial' })]
        })
      ]
    }))
  });

  elements.push(new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: sColWidths,
    rows: [statsRow]
  }));

  return elements;
}

// ─── COVER PAGE ──────────────────────────────────────────────
function createCoverPage(meta) {
  return [
    new Paragraph({ spacing: { before: 3000 }, children: [] }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      children: [new TextRun({
        text: 'DISSECAÇÃO COMPLETA DE VSL',
        bold: true, size: 52, color: COLORS.dash.dark, font: 'Arial'
      })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 100 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.dash.accent, space: 12 } },
      children: [new TextRun({
        text: meta.vsl_name || 'VSL',
        bold: true, size: 44, color: COLORS.dash.accent, font: 'Arial'
      })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 200, after: 100 },
      children: [new TextRun({
        text: meta.product_type || '',
        size: 28, color: COLORS.grayDark, font: 'Arial'
      })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 400 },
      children: [new TextRun({
        text: `Agente Atlas \u2014 Dissecação Profunda`,
        size: 24, color: COLORS.grayDark, font: 'Arial', italics: true
      })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 100 },
      children: [new TextRun({
        text: meta.date || '',
        size: 22, color: COLORS.grayDark, font: 'Arial'
      })]
    }),
    new Paragraph({ children: [new PageBreak()] })
  ];
}

// ─── MODULE DIVIDER PAGE ─────────────────────────────────────
function createModuleDivider(moduleNum, moduleName, color) {
  return [
    new Paragraph({ pageBreakBefore: true, spacing: { before: 2500 }, children: [] }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 100 },
      children: [new TextRun({
        text: `MÓDULO ${moduleNum}`,
        bold: true, size: 28, color: COLORS.grayDark, font: 'Arial'
      })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      border: {
        bottom: { style: BorderStyle.SINGLE, size: 6, color: color.accent, space: 10 },
        top: { style: BorderStyle.SINGLE, size: 6, color: color.accent, space: 10 }
      },
      shading: { fill: color.light, type: ShadingType.CLEAR },
      children: [new TextRun({
        text: moduleName,
        bold: true, size: 44, color: color.dark, font: 'Arial'
      })]
    }),
    new Paragraph({ spacing: { before: 200 }, children: [] }),
    new Paragraph({ children: [new PageBreak()] })
  ];
}

// ─── BUILD DOCUMENT ──────────────────────────────────────────
async function buildDocument() {
  const moduleNames = ['DISSECAÇÃO DA LEAD', 'DISSECAÇÃO DO STORYTELLING', 'DISSECAÇÃO DA TESE DE MARKETING', 'DISSECAÇÃO DO FECHAMENTO / OFERTA'];

  // Collect all children
  const allChildren = [];

  // Cover page
  allChildren.push(...createCoverPage(meta));

  // Dashboard
  allChildren.push(...createDashboard(meta));
  allChildren.push(new Paragraph({ children: [new PageBreak()] }));

  // Flow Map
  allChildren.push(...createFlowMap(meta));
  allChildren.push(new Paragraph({ children: [new PageBreak()] }));

  // Table of Contents
  allChildren.push(new Paragraph({
    spacing: { before: 200, after: 300 },
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'SUMÁRIO', bold: true, size: 32, color: COLORS.dash.dark, font: 'Arial' })]
  }));
  allChildren.push(new TableOfContents("Sumário", { hyperlink: true, headingStyleRange: "1-3" }));
  allChildren.push(new Paragraph({ children: [new PageBreak()] }));

  // Modules
  for (let m = 0; m < 4; m++) {
    const color = MODULE_COLORS[m];
    // Module divider
    allChildren.push(...createModuleDivider(m + 1, moduleNames[m], color));

    // Module content
    const content = parseMarkdownToElements(modules[m], color);
    allChildren.push(...content);
  }

  const doc = new Document({
    styles: {
      default: {
        document: { run: { font: 'Arial', size: 22 } }
      },
      paragraphStyles: [
        {
          id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 36, bold: true, font: 'Arial' },
          paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
        },
        {
          id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 28, bold: true, font: 'Arial' },
          paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 }
        },
        {
          id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 24, bold: true, font: 'Arial' },
          paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
        }
      ]
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE_WIDTH, height: 15840 },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }
        }
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.grayMed, space: 4 } },
            children: [
              new TextRun({ text: `Dissecação Atlas \u2014 ${meta.vsl_name || 'VSL'}`, size: 16, color: COLORS.grayDark, font: 'Arial', italics: true })
            ]
          })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            border: { top: { style: BorderStyle.SINGLE, size: 1, color: COLORS.grayMed, space: 4 } },
            children: [
              new TextRun({ text: 'Página ', size: 16, color: COLORS.grayDark, font: 'Arial' }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: COLORS.grayDark, font: 'Arial' })
            ]
          })]
        })
      },
      children: allChildren
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`Document created: ${outputPath}`);
  console.log(`Size: ${(buffer.length / 1024).toFixed(1)} KB`);
  console.log(`Modules: 4`);
  console.log(`Dashboard items: ${16 + (meta.personagens || []).length}`);
}

buildDocument().catch(err => {
  console.error('Error creating document:', err.message);
  process.exit(1);
});
