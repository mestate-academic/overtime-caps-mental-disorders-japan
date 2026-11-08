// Render spec_main.json / spec_supp.json to .docx (A4, Arial, tables & figures one per page)
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, ImageRun, PageBreak, AlignmentType, HeadingLevel, Footer, PageNumber,
  LevelFormat, LineNumberRestartFormat, VerticalAlign, PageOrientation
} = require('docx');

const OUT = 'output/intermediate/';
const FONT = 'Arial';
const TW = 9026; // A4 text width with 1" margins

const styles = {
  default: { document: { run: { font: FONT, size: 22 } } },
  paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { font: FONT, size: 26, bold: true }, paragraph: { spacing: { before: 360, after: 160 }, keepNext: true, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { font: FONT, size: 22, bold: true, italics: true }, paragraph: { spacing: { before: 240, after: 120 }, keepNext: true, outlineLevel: 1 } },
    { id: 'Title', name: 'Title', basedOn: 'Normal', next: 'Normal',
      run: { font: FONT, size: 30, bold: true }, paragraph: { spacing: { before: 0, after: 360 }, keepNext: true } },
  ],
};
const numbering = { config: [{ reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] };

const R = (runs, extra = {}) => runs.map(([t, b, i]) => new TextRun({ text: t, bold: !!b, italics: !!i, ...extra }));
const BODY_SP = { line: 360, after: 120 };
let PB=false; const pb = () => { PB=true; return null; };
const P = (o) => { if (PB) { o.pageBreakBefore = true; PB=false; } return new Paragraph(o); };
const border = { style: BorderStyle.SINGLE, size: 4, color: '808080' };
const borders = { top: border, bottom: border, left: border, right: border };

function table(t, fontSize = 18) {
  if (t.font) fontSize = t.font;
  const ncol = t.widths.length;
  const mk = (txt, w, hdr, first, opts = {}) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders, columnSpan: opts.span || 1,
    shading: (hdr || opts.group) ? { fill: hdr ? 'E7E6E6' : 'F2F2F2', type: ShadingType.CLEAR, color: 'auto' } : undefined,
    margins: { top: 50, bottom: 50, left: 80, right: 80 }, verticalAlign: VerticalAlign.CENTER,
    children: [P({ alignment: (first || opts.group) ? AlignmentType.LEFT : AlignmentType.CENTER,
      children: txt.replace(/\*\*/g, '').split('\n').map((line, i) => new TextRun({ text: line, bold: (hdr || opts.group) || ((/^\*\*/.test(txt)) && i === 0), size: fontSize, break: i > 0 ? 1 : undefined })) })],
  });
  const titleP = P({ spacing: { after: 160 }, keepNext: true, children: R(t.title, { size: 22 }) });
  const rows = [];
  if (t.groups) { let c = 0; rows.push(new TableRow({ tableHeader: true, children: t.groups.map(([lab, span]) => { const w = t.widths.slice(c, c + span).reduce((a, b) => a + b, 0); const cell = mk(lab, w, true, c === 0, { span }); c += span; return cell; }) })); }
  rows.push(new TableRow({ tableHeader: true, children: t.header.map((h, j) => mk(h, t.widths[j], true, j === 0)) }));
  for (const r of t.rows) {
    if (typeof r === 'string' && r.startsWith('§')) { rows.push(new TableRow({ cantSplit: true, children: [mk(r.slice(1), t.widths.reduce((a, b) => a + b, 0), false, true, { span: ncol, group: true })] })); continue; }
    rows.push(new TableRow({ cantSplit: true, children: r.map((c, j) => mk(c, t.widths[j], false, j === 0)) }));
  }
  const out = [ titleP, new Table({ width: { size: t.widths.reduce((a,b)=>a+b,0), type: WidthType.DXA }, columnWidths: t.widths, rows }) ];
  if (t.note) out.push(P({ spacing: { before: 120 }, children: [new TextRun({ text: t.note, size: 18 })] }));
  return out;
}

function figure(f, maxW = 600) {
  const [pw, ph] = f.px; const w = maxW, h = Math.round(maxW * ph / pw);
  return [
    P({ spacing: { after: 160 }, children: [new TextRun({ text: f.title, bold: true })] }),
    P({ alignment: AlignmentType.CENTER, children: [new ImageRun({ type: 'png', data: fs.readFileSync(f.path), transformation: { width: w, height: h }, altText: { title: f.title, description: f.title, name: f.title } })] }),
    P({ spacing: { before: 240, line: 300 }, children: [new TextRun({ text: f.title + ' ', bold: true }), new TextRun({ text: f.legend })] }),
  ];
}

const footer = () => new Footer({ children: [P({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] });
const page = { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } };

// ---------------- main manuscript ----------------
{
  const spec = JSON.parse(fs.readFileSync(OUT + 'spec_main.json'));
  const kids = [];
  let inRefs = false;
  for (const b of spec.blocks) {
    if (b.t === 'pb') { pb(); continue; }
    if (b.t === 'h1') { kids.push(P({ style: 'Title', children: [new TextRun(b.text)] })); continue; }
    if (b.t === 'h2') { inRefs = b.text === 'REFERENCES'; kids.push(P({ heading: HeadingLevel.HEADING_1, children: [new TextRun(b.text)] })); continue; }
    if (b.t === 'h3') { kids.push(P({ heading: HeadingLevel.HEADING_2, children: [new TextRun(b.text)] })); continue; }
    if (b.t === 'bullet') { kids.push(P({ numbering: { reference: 'bul', level: 0 }, spacing: BODY_SP, children: R(b.runs) })); continue; }
    if (b.t === 'ref') { kids.push(P({ spacing: { after: 80 }, indent: { left: 440, hanging: 440 }, children: [new TextRun(b.n + '.\t'), ...R(b.runs, { size: 20 })] })); continue; }
    kids.push(P({ spacing: BODY_SP, children: R(b.runs) }));
  }
  const sections = []; let cur = kids;
  const mkSec = (children, landscape) => ({ properties: { page: landscape ? { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: page.margin } : page, lineNumbers: { countBy: 1, restart: LineNumberRestartFormat.CONTINUOUS } }, footers: { default: footer() }, children });
  for (const t of spec.tables) {
    if (t.landscape) { sections.push(mkSec(cur, false)); PB = false; cur = [...table(t)]; sections.push(mkSec(cur, true)); cur = []; }
    else { if (cur.length) pb(); cur.push(...table(t)); }
  }
  for (const f of spec.figs) { pb(); cur.push(...figure(f)); }
  pb();
  cur.push(P({ spacing: BODY_SP, children: R(spec.supp_line) }));
  sections.push(mkSec(cur, false));
  const doc = new Document({ styles, numbering, creator: 'Hironori Uematsu', sections });
  Packer.toBuffer(doc).then(buf => fs.writeFileSync('manuscript/Manuscript_OEM_v8.docx', buf));
}

// ---------------- supplementary ----------------
{
  const spec = JSON.parse(fs.readFileSync(OUT + 'spec_supp.json'));
  const kids = [
    P({ style: 'Title', children: [new TextRun('Online supplemental material')] }),
    P({ spacing: { after: 240 }, children: [new TextRun({ text: spec.title, italics: true })] }),
    P({ heading: HeadingLevel.HEADING_1, children: [new TextRun('Contents')] }),
  ];
  const items = spec.tables.map(t => t.title.map(x => x[0]).join('')).concat(spec.figs.map(f => f.title + ' ' + f.legend.split('. ')[0] + '.'));
  // order: tables S1–S4, figures S1–S2, STROBE
  const strobe = items.splice(spec.tables.length-1, 1)[0]; items.push(strobe);
  for (const it of items) kids.push(P({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: it, size: 20 })] }));
  const tabs = spec.tables.slice(0, spec.tables.length-1), st = spec.tables[spec.tables.length-1];
  const secs=[]; let cur=kids;
  const sec=(children,land)=>({ properties: { page: land ? { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: page.margin } : page }, footers: { default: footer() }, children });
  for (const t of tabs) { if (t.landscape) { secs.push(sec(cur,false)); PB=false; secs.push(sec([...table(t)],true)); cur=[]; } else { if (cur.length) pb(); cur.push(...table(t)); } }
  for (const f of spec.figs) { pb(); cur.push(...figure(f, 560)); }
  pb(); cur.push(...table(st, 17)); secs.push(sec(cur,false));
  const doc = new Document({ styles, numbering, creator: 'Hironori Uematsu', sections: secs });
  Packer.toBuffer(doc).then(buf => fs.writeFileSync('manuscript/Supplementary_OEM_v6.docx', buf));
}
