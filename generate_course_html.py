"""
Generates a single-page, print-ready, colorful, PDF-convertible HTML crash course:
  agentic-ai-accelerated-crash-course.html

Reads all 8 verified Python labs from labs/ and embeds them completely with
syntax highlighting so the HTML is 100% self-contained.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LABS_DIR = BASE_DIR / "labs"
OUTPUT_HTML = BASE_DIR / "agentic-ai-accelerated-crash-course.html"

# Precompiled regex for fast, thread-safe Python syntax highlighting
_PY_TOKEN_RE = re.compile(
    r'(?P<comment>#[^\n]*)'
    r'|(?P<docstring>"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')'
    r'|(?P<string>f?"(?:\\.|[^"\\])*"|f?\'(?:\\.|[^\'\\])*\')'
    r'|(?P<decorator>@[a-zA-Z_][a-zA-Z0-9_.]*)'
    r'|(?P<keyword>\b(?:from|import|as|def|class|return|if|elif|else|for|while|in|not|and|or|is|None|True|False|try|except|raise|with|lambda|pass|break|continue|yield)\b)'
    r'|(?P<builtin>\b(?:str|int|float|bool|dict|list|tuple|set|object|Exception|KeyError|ValueError|RuntimeError|OverflowError|print|len|max|min|sum|range|next|zip|enumerate|dataclass|field|replace|deque|Counter|RLock|ThreadPoolExecutor)\b)'
    r'|(?P<number>\b\d+(?:\.\d+)?\b)'
)


def highlight_python(code: str) -> str:
    """Applies clean VS Code / Dracula-inspired HTML syntax highlighting."""
    out: list[str] = []
    pos = 0
    for match in _PY_TOKEN_RE.finditer(code):
        if match.start() > pos:
            out.append(html.escape(code[pos : match.start()]))
        kind = match.lastgroup
        text = html.escape(match.group())
        out.append(f'<span class="tok-{kind}">{text}</span>')
        pos = match.end()
    if pos < len(code):
        out.append(html.escape(code[pos:]))
    return "".join(out)


def read_lab_code(filename: str) -> str:
    raw = (LABS_DIR / filename).read_text(encoding="utf-8").strip()
    return highlight_python(raw)


def term_cards(items: list[tuple[str, str]], accent: str) -> str:
    cards = []
    for term, desc in items:
        cards.append(
            f'<div class="term-card" style="border-left-color:{accent};">'
            f'<div class="term-title" style="color:{accent};">{html.escape(term)}</div>'
            f'<div class="term-desc">{desc}</div>'
            f'</div>'
        )
    return '<div class="term-grid">' + "".join(cards) + "</div>"


def code_block(title: str, filename: str, highlighted: str, expected_output: str) -> str:
    return f"""
    <div class="code-card">
      <div class="code-header">
        <div class="code-dots"><span></span><span></span><span></span></div>
        <div class="code-title">{html.escape(title)} &mdash; <code>{html.escape(filename)}</code></div>
        <div class="code-badge">Python 3.10+ &bull; Thread-Safe</div>
      </div>
      <pre class="code-pre"><code>{highlighted}</code></pre>
      <div class="output-box">
        <div class="output-label">BEKLENEN TERMINAL ÇIKTISI (<code>python {html.escape(filename)}</code>)</div>
        <pre class="output-pre">{html.escape(expected_output.strip())}</pre>
      </div>
    </div>
    """


def build_html() -> str:
    lab1 = read_lab_code("mod01_structured_llm.py")
    lab2 = read_lab_code("mod02_tool_use_agent.py")
    lab3 = read_lab_code("mod03_memory_and_state.py")
    lab4 = read_lab_code("mod04_agentic_rag.py")
    lab5 = read_lab_code("mod05_mcp_client_server.py")
    lab6 = read_lab_code("mod06_stateful_workflow.py")
    lab7 = read_lab_code("mod07_production_guardrails.py")
    lab8 = read_lab_code("mod08_capstone_agent.py")

    css = """
    :root {
      --ink: #0f172a;
      --muted: #475569;
      --bg: #f8fafc;
      --paper: #ffffff;
      --border: #e2e8f0;
      --code-bg: #0f172a;
      --c0: #2563eb;
      --c1: #7c3aed;
      --c2: #0891b2;
      --c3: #059669;
      --c4: #d97706;
      --c5: #db2777;
      --c6: #4f46e5;
      --c7: #dc2626;
      --c8: #0d9488;
    }

    @page {
      size: A4;
      margin: 12mm 13mm 14mm 13mm;
    }

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      margin: 0;
      padding: 24px 16px 60px 16px;
      background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 45%, #ecfeff 100%);
      color: var(--ink);
      font-family: "Segoe UI", system-ui, -apple-system, Roboto, Arial, sans-serif;
      font-size: 13.5px;
      line-height: 1.58;
    }

    .sheet {
      max-width: 960px;
      margin: 0 auto;
      background: var(--paper);
      border-radius: 18px;
      box-shadow: 0 20px 55px rgba(15, 23, 42, 0.12);
      overflow: hidden;
    }

    /* Floating Print Bar */
    .print-bar {
      position: sticky;
      top: 12px;
      z-index: 100;
      max-width: 960px;
      margin: 0 auto 14px auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(8px);
      color: #fff;
      padding: 10px 18px;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(15, 23, 42, 0.25);
    }
    .print-bar-text { font-size: 13px; color: #cbd5e1; }
    .print-bar-text strong { color: #fff; }
    .print-btn {
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      color: #0f172a;
      font-weight: 800;
      border: none;
      border-radius: 8px;
      padding: 8px 16px;
      cursor: pointer;
      font-size: 13px;
    }
    .print-btn:hover { filter: brightness(1.08); }

    /* Cover */
    .cover {
      background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 48%, #0e7490 100%);
      color: #fff;
      padding: 46px 42px 38px 42px;
      position: relative;
      overflow: hidden;
    }
    .cover::after {
      content: "";
      position: absolute;
      width: 340px;
      height: 340px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(56,189,248,0.28), transparent 70%);
      top: -90px;
      right: -80px;
    }
    .cover-pill {
      display: inline-block;
      background: rgba(56, 189, 248, 0.2);
      border: 1px solid rgba(56, 189, 248, 0.5);
      color: #bae6fd;
      padding: 4px 12px;
      border-radius: 999px;
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin-bottom: 14px;
    }
    .cover h1 {
      margin: 0 0 12px 0;
      font-size: 31px;
      line-height: 1.2;
      font-weight: 800;
      letter-spacing: -0.02em;
    }
    .cover h1 span {
      background: linear-gradient(90deg, #38bdf8, #a78bfa, #34d399);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .cover-sub {
      font-size: 15px;
      color: #cbd5e1;
      max-width: 760px;
      margin: 0 0 24px 0;
    }
    .cover-stats {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }
    .stat-box {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 12px;
      padding: 12px 14px;
    }
    .stat-num { font-size: 19px; font-weight: 800; color: #38bdf8; }
    .stat-lbl { font-size: 11.5px; color: #e2e8f0; margin-top: 2px; }

    /* Content Wrapper */
    .content { padding: 28px 36px 36px 36px; }

    /* TOC */
    .toc-card {
      background: linear-gradient(135deg, #f8fafc, #eef2ff);
      border: 1px solid #c7d2fe;
      border-radius: 14px;
      padding: 18px 22px;
      margin-bottom: 24px;
    }
    .toc-title {
      font-size: 15px;
      font-weight: 800;
      color: #312e81;
      margin: 0 0 12px 0;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .toc-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px 18px;
    }
    .toc-item {
      display: flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      color: var(--ink);
      font-size: 12.5px;
      font-weight: 600;
      padding: 5px 8px;
      border-radius: 8px;
      background: rgba(255,255,255,0.75);
      border: 1px solid #e2e8f0;
    }
    .toc-dot {
      width: 22px;
      height: 22px;
      border-radius: 6px;
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    /* Module Header */
    .module {
      margin-top: 28px;
      padding-top: 6px;
      page-break-before: always;
      break-before: page;
    }
    .module-first {
      page-break-before: auto;
      break-before: auto;
    }
    .mod-banner {
      border-radius: 14px;
      padding: 16px 20px;
      color: #fff;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }
    .mod-tag {
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      opacity: 0.9;
    }
    .mod-banner h2 {
      margin: 2px 0 0 0;
      font-size: 20px;
      font-weight: 800;
      line-height: 1.25;
    }
    .mod-num-badge {
      font-size: 24px;
      font-weight: 900;
      background: rgba(255,255,255,0.2);
      border: 1px solid rgba(255,255,255,0.35);
      border-radius: 10px;
      padding: 6px 14px;
      flex-shrink: 0;
    }

    h3.sec-h {
      font-size: 14.5px;
      font-weight: 800;
      margin: 16px 0 8px 0;
      color: var(--ink);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    h3.sec-h .sec-pill {
      display: inline-block;
      font-size: 10.5px;
      font-weight: 800;
      color: #fff;
      padding: 2px 8px;
      border-radius: 999px;
    }

    p { margin: 0 0 9px 0; }
    ul, ol { margin: 4px 0 10px 0; padding-left: 20px; }
    li { margin-bottom: 4px; }
    code {
      background: #f1f5f9;
      color: #0f172a;
      padding: 1px 5px;
      border-radius: 4px;
      font-family: "Cascadia Code", Consolas, monospace;
      font-size: 12px;
      border: 1px solid #e2e8f0;
    }

    /* Analogy Box */
    .analogy-box {
      background: linear-gradient(135deg, #fffbeb, #fef3c7);
      border: 1px solid #fcd34d;
      border-left: 5px solid #d97706;
      border-radius: 10px;
      padding: 11px 15px;
      margin: 10px 0 12px 0;
      break-inside: avoid;
    }
    .analogy-title {
      font-size: 11.5px;
      font-weight: 800;
      color: #92400e;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }

    /* Key Terminology Grid */
    .term-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 9px;
      margin: 8px 0 14px 0;
    }
    .term-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 4px solid var(--c0);
      border-radius: 9px;
      padding: 9px 12px;
      break-inside: avoid;
    }
    .term-title {
      font-size: 12.5px;
      font-weight: 800;
      margin-bottom: 3px;
    }
    .term-desc {
      font-size: 12px;
      color: #334155;
      line-height: 1.45;
    }

    /* Visual Flow Diagram */
    .diagram-box {
      background: linear-gradient(135deg, #f8fafc, #f1f5f9);
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      padding: 14px 16px;
      margin: 10px 0 14px 0;
      break-inside: avoid;
    }
    .diagram-caption {
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #475569;
      margin-bottom: 10px;
    }
    .flow-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 6px;
      margin-bottom: 8px;
    }
    .flow-row:last-child { margin-bottom: 0; }
    .f-node {
      padding: 6px 10px;
      border-radius: 8px;
      font-size: 11.5px;
      font-weight: 700;
      color: #fff;
      box-shadow: 0 2px 6px rgba(15,23,42,0.1);
    }
    .f-node-light {
      padding: 6px 10px;
      border-radius: 8px;
      font-size: 11.5px;
      font-weight: 700;
      background: #fff;
      color: #0f172a;
      border: 1.5px solid #94a3b8;
    }
    .f-arrow {
      font-weight: 900;
      color: #64748b;
      font-size: 14px;
    }

    /* Code Card */
    .code-card {
      background: var(--code-bg);
      border-radius: 12px;
      overflow: hidden;
      margin: 10px 0 14px 0;
      border: 1px solid #1e293b;
      box-shadow: 0 8px 20px rgba(15,23,42,0.14);
    }
    .code-header {
      background: #1e293b;
      padding: 7px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      border-bottom: 1px solid #334155;
    }
    .code-dots { display: flex; gap: 5px; }
    .code-dots span { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
    .code-dots span:nth-child(1) { background: #ef4444; }
    .code-dots span:nth-child(2) { background: #f59e0b; }
    .code-dots span:nth-child(3) { background: #10b981; }
    .code-title { color: #e2e8f0; font-size: 11.5px; font-weight: 700; flex: 1; }
    .code-title code { background: rgba(255,255,255,0.1); color: #7dd3fc; border: none; font-size: 11px; }
    .code-badge {
      font-size: 10px;
      font-weight: 800;
      color: #34d399;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(52, 211, 153, 0.35);
      padding: 2px 8px;
      border-radius: 999px;
    }
    .code-pre {
      margin: 0;
      padding: 12px 14px;
      color: #e2e8f0;
      font-family: "Cascadia Code", Consolas, "Courier New", monospace;
      font-size: 10.6px;
      line-height: 1.44;
      white-space: pre-wrap;
      word-break: break-word;
      overflow-x: auto;
    }
    .code-pre code {
      background: transparent;
      color: inherit;
      padding: 0;
      border: none;
      font-size: inherit;
    }
    .tok-comment { color: #64748b; font-style: italic; }
    .tok-docstring { color: #94a3b8; }
    .tok-string { color: #86efac; }
    .tok-decorator { color: #fbbf24; font-weight: 700; }
    .tok-keyword { color: #c084fc; font-weight: 700; }
    .tok-builtin { color: #38bdf8; }
    .tok-number { color: #fb923c; }

    .output-box {
      background: #020617;
      border-top: 1px solid #334155;
      padding: 9px 14px;
      break-inside: avoid;
    }
    .output-label {
      font-size: 10px;
      font-weight: 800;
      color: #34d399;
      letter-spacing: 0.06em;
      margin-bottom: 4px;
    }
    .output-label code { background: transparent; border: none; color: #94a3b8; padding: 0; font-size: 10px; }
    .output-pre {
      margin: 0;
      color: #cbd5e1;
      font-family: "Cascadia Code", Consolas, monospace;
      font-size: 10.4px;
      line-height: 1.42;
      white-space: pre-wrap;
      word-break: break-word;
    }

    /* Pitfalls & Challenge Split */
    .split-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 10px;
      break-inside: avoid;
    }
    .pitfall-card {
      background: #fef2f2;
      border: 1px solid #fecaca;
      border-left: 4px solid #dc2626;
      border-radius: 10px;
      padding: 10px 13px;
    }
    .pitfall-title {
      font-size: 11.5px;
      font-weight: 800;
      color: #991b1b;
      text-transform: uppercase;
      margin-bottom: 5px;
    }
    .challenge-card {
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      border-left: 4px solid #059669;
      border-radius: 10px;
      padding: 10px 13px;
    }
    .challenge-title {
      font-size: 11.5px;
      font-weight: 800;
      color: #065f46;
      text-transform: uppercase;
      margin-bottom: 5px;
    }

    /* Tables */
    table.styled-table {
      width: 100%;
      border-collapse: collapse;
      margin: 10px 0 14px 0;
      font-size: 12px;
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid #cbd5e1;
      break-inside: avoid;
    }
    table.styled-table th {
      background: #1e293b;
      color: #fff;
      text-align: left;
      padding: 8px 10px;
      font-weight: 700;
    }
    table.styled-table td {
      padding: 7px 10px;
      border-top: 1px solid #e2e8f0;
      vertical-align: top;
    }
    table.styled-table tr:nth-child(even) td { background: #f8fafc; }

    /* Trap Cards */
    .traps-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin: 10px 0 14px 0;
      break-inside: avoid;
    }
    .trap-card {
      background: linear-gradient(180deg, #fff1f2, #ffffff);
      border: 1px solid #fda4af;
      border-top: 4px solid #e11d48;
      border-radius: 10px;
      padding: 11px 12px;
    }
    .trap-num {
      font-size: 10.5px;
      font-weight: 900;
      color: #e11d48;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .trap-h { font-size: 12.5px; font-weight: 800; color: #0f172a; margin: 3px 0 5px 0; }
    .trap-p { font-size: 11.8px; color: #334155; margin: 0; line-height: 1.45; }

    /* Roadmap 14-day */
    .roadmap-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin: 10px 0 14px 0;
      break-inside: avoid;
    }
    .day-card {
      background: #f0fdfa;
      border: 1px solid #99f6e4;
      border-left: 4px solid #0d9488;
      border-radius: 8px;
      padding: 8px 11px;
      font-size: 12px;
    }
    .day-badge { font-weight: 800; color: #0f766e; }

    /* Glossary */
    .glossary-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 7px 12px;
    }
    .gloss-item {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 7px 10px;
      font-size: 11.6px;
      line-height: 1.42;
      break-inside: avoid;
    }
    .gloss-item strong { color: #1e3a8a; }

    /* Print Media Overrides */
    @media print {
      body {
        background: #fff !important;
        padding: 0 !important;
        font-size: 11.5px !important;
        line-height: 1.48 !important;
      }
      .print-bar { display: none !important; }
      .sheet {
        max-width: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
      }
      .content { padding: 14px 4px 10px 4px !important; }
      .cover { border-radius: 12px !important; padding: 28px 28px 24px 28px !important; }
      .code-pre { font-size: 9.2px !important; line-height: 1.36 !important; padding: 9px 11px !important; }
      .output-pre { font-size: 9.2px !important; }
    }
    """

    html_doc = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Agentic AI Engineering 2027 — Hızlandırılmış Uygulamalı Kurs</title>
  <style>{css}</style>
</head>
<body>

  <div class="print-bar">
    <div class="print-bar-text">
      <strong>Agentic AI 2027 Crash Course</strong> &bull; Tek Sayfa, Eksiksiz Kodlu &amp; PDF Yazdırmaya Hazır (&lt;40 A4 Sayfası)
    </div>
    <button class="print-btn" onclick="window.print()">PDF Olarak Kaydet / Yazdır (Ctrl+P)</button>
  </div>

  <div class="sheet">
    <!-- COVER -->
    <header class="cover">
      <div class="cover-pill">Accelerated Hands-On Crash Course &bull; 2027 Edition</div>
      <h1>Agentic AI Engineering:<br/><span>Sıfırdan Production'a Uygulamalı Kurs</span></h1>
      <p class="cover-sub">
        Sıfırdan başlayan <strong>Junior Developer</strong>'lar için hazırlanmış; tüm teknik kavramları İngilizce orijinalleriyle,
        anlatımı kusursuz Türkçe ile sunan, %100 <em>Thread-Safe</em> ve hemen çalıştırılabilir 8 tam Python laboratuvarı içeren eksiksiz tek sayfa rehber.
      </p>
      <div class="cover-stats">
        <div class="stat-box"><div class="stat-num">9 Modül</div><div class="stat-lbl">Modül 0 &rarr; Capstone Proje</div></div>
        <div class="stat-box"><div class="stat-num">8 Tam Lab</div><div class="stat-lbl">Eksiksiz, Test Edilmiş Kod</div></div>
        <div class="stat-box"><div class="stat-num">33 Terim</div><div class="stat-lbl">Master Glossary &amp; Kartlar</div></div>
        <div class="stat-box"><div class="stat-num">&lt; 40 Sayfa</div><div class="stat-lbl">A4 Renkli PDF Uyumlu</div></div>
      </div>
    </header>

    <main class="content">
      <!-- TOC -->
      <nav class="toc-card">
        <div class="toc-title">Müfredat Haritası (İçindekiler)</div>
        <div class="toc-grid">
          <a class="toc-item" href="#mod0"><span class="toc-dot" style="background:var(--c0);">0</span>Kurulum ve Zihinsel Model (Setup &amp; Mental Model)</a>
          <a class="toc-item" href="#mod1"><span class="toc-dot" style="background:var(--c1);">1</span>LLM Engineering &amp; Structured Outputs</a>
          <a class="toc-item" href="#mod2"><span class="toc-dot" style="background:var(--c2);">2</span>Tool Use, Function Calling &amp; Agent Loop</a>
          <a class="toc-item" href="#mod3"><span class="toc-dot" style="background:var(--c3);">3</span>Agent Memory &amp; State Management</a>
          <a class="toc-item" href="#mod4"><span class="toc-dot" style="background:var(--c4);">4</span>RAG, Vector Databases &amp; Agentic RAG</a>
          <a class="toc-item" href="#mod5"><span class="toc-dot" style="background:var(--c5);">5</span>Model Context Protocol (MCP)</a>
          <a class="toc-item" href="#mod6"><span class="toc-dot" style="background:var(--c6);">6</span>Planning &amp; Multi-Agent Orchestration</a>
          <a class="toc-item" href="#mod7"><span class="toc-dot" style="background:var(--c7);">7</span>Production-Ready Engineering &amp; 3 Kritik Tuzak</a>
          <a class="toc-item" href="#mod8"><span class="toc-dot" style="background:var(--c8);">8</span>Capstone Mini-Project &amp; 14 Günlük Plan</a>
          <a class="toc-item" href="#glossary"><span class="toc-dot" style="background:#1e293b;">G</span>Master Glossary (33 Kritik Terim Sözlüğü)</a>
        </div>
      </nav>

      <!-- ================= MODÜL 0 ================= -->
      <section class="module module-first" id="mod0">
        <div class="mod-banner" style="background:linear-gradient(135deg,#1d4ed8,#2563eb,#0284c7);">
          <div>
            <div class="mod-tag">Başlangıç &amp; Mimari Temel</div>
            <h2>Modül 0: Kurulum ve Zihinsel Model (Setup &amp; Mental Model)</h2>
          </div>
          <div class="mod-num-badge">00</div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c0);">1</span> Ne Öğreneceğiz &amp; Neden Önemli?</h3>
        <p>Bir <strong>LLM</strong> (<em>Large Language Model</em>) API'sine soru sorup yanıt almak yalnızca birkaç satır kod sürer. Ancak gerçek bir şirkette çalışan yazılımlar tek bir soru-cevapla bitmez. Sistemin veritabanına bağlanması, konuşma geçmişini (<em>State</em>) koruması, planını güncellemesi ve hata aldığında kendini toparlaması gerekir.</p>
        <div class="analogy-box">
          <div class="analogy-title">Günlük Hayattan Benzetme</div>
          <strong>Klasik Prompt-and-Response</strong>, masasında yalnızca ansiklopedi bulunan bir danışmana benzer: tek seferde yanıt verir, telefon açamaz ve iki dakika sonra adınızı unutur. <strong>Agentic AI</strong> ise elinde telefonu, not defteri ve şirket ekranı olan bir operasyon uzmanına benzer: hedefi anlar, plan yapar, araçları kullanır, sonucu doğrular ve işi bitirip net bir rapor sunar.
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c0);">2</span> Key Terminology (Kritik Kavramlar ve Tanımlar)</h3>
        {term_cards([
          ("LLM (Large Language Model)", "Çok büyük metin verileriyle eğitilmiş, metin anlama ve üretme yeteneğine sahip yapay zekâ modelidir."),
          ("Prompt-and-Response", "Kullanıcının modele tek bir girdi (Prompt) gönderip tek bir yanıt aldığı statik etkileşim biçimidir."),
          ("Agentic AI", "Hedefe ulaşmak için plan yapan, harici araçlar (Tools) çağıran, bellek tutan ve adım adım ilerleyen sistem mimarisidir."),
          ("Production", "Yazılımın geliştirici bilgisayarından çıkıp gerçek kullanıcıların hizmetine sunulduğu canlı çalışma ortamıdır."),
          ("Virtual Environment (venv)", "Python projelerinin kütüphanelerini birbirinden izole eden, sürüm çakışmalarını önleyen sanal ortamdır."),
          ("Thread-Safety", "Birden fazla Thread aynı anda aynı koda eriştiğinde verinin bozulmaması ve sistemin tutarlı kalmasıdır."),
        ], "var(--c0)")}

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c0);">3</span> Adım Adım Teknik Anlatım</h3>
        <p>Unutmayın: <strong>Agent sihirli bir model türü değildir.</strong> <em>Agent</em>, bir <em>LLM</em>'in etrafına kontrollü bir döngü (<em>Agent Loop</em>), bellek (<em>State</em>) ve araç erişimi (<em>Tool Use</em>) eklenerek kurulan bir <strong>Software Architecture</strong> desenidir.</p>
        <div class="diagram-box">
          <div class="diagram-caption">Mimari Karşılaştırma: Klasik LLM vs. Agentic AI Döngüsü</div>
          <div class="flow-row">
            <span class="f-node-light">KLASİK:</span>
            <span class="f-node" style="background:#64748b;">Kullanıcı Prompt</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#475569;">LLM</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#334155;">Tek Cevap (Bitiş)</span>
          </div>
          <div class="flow-row">
            <span class="f-node-light">AGENTIC:</span>
            <span class="f-node" style="background:var(--c0);">Hedef</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:var(--c1);">1. Planning</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:var(--c3);">2. Memory &amp; State</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:var(--c2);">3. Tool / MCP / RAG</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:var(--c4);">4. Observe &amp; Loop</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#059669;">Nihai Yanıt</span>
          </div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c0);">4</span> Hands-On Lab (PowerShell Ortam Kurulumu)</h3>
        <div class="code-card">
          <div class="code-header">
            <div class="code-dots"><span></span><span></span><span></span></div>
            <div class="code-title">Modül 0 Kurulum Komutları &mdash; <code>PowerShell</code></div>
            <div class="code-badge">Zero API Key Required</div>
          </div>
          <pre class="code-pre"><code># 1. Kurs klasörüne geçin (PowerShell: $env:USERPROFILE | CMD: %USERPROFILE%)
cd $env:USERPROFILE\\agentic-ai-crash-course-2027

# 2. İzole Python Virtual Environment oluşturun ve aktif edin
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1

# 3. Python sürümünü doğrulayın (3.10+ olmalı)
python --version

# 4. (Opsiyonel) Gerçek API anahtarlarınız için şablonu kopyalayın
Copy-Item .env.example .env</code></pre>
          <div class="output-box">
            <div class="output-label">BEKLENEN ÇIKTI</div>
            <pre class="output-pre">Python 3.11.x (veya 3.10+ herhangi bir sürüm)</pre>
          </div>
        </div>

        <div class="split-grid">
          <div class="pitfall-card">
            <div class="pitfall-title">Common Pitfalls (Sık Hatalar)</div>
            <ul>
              <li><code>venv</code> açmadan tüm paketleri sistem Python'ına kurup sürüm çakışması yaşamak.</li>
              <li><em>API Key</em> bilgisini <code>.py</code> dosyasına düz metin yazıp GitHub'a göndermek.</li>
            </ul>
          </div>
          <div class="challenge-card">
            <div class="challenge-title">Mini Challenge (Pratik Görev)</div>
            <p><code>.env.example</code> dosyasına <code>APP_ENV=development</code> satırını ekleyin ve Python ile <code>os.getenv("APP_ENV", "local")</code> değerini okuyup doğrulayın.</p>
          </div>
        </div>
      </section>

      <!-- ================= MODÜL 1 ================= -->
      <section class="module" id="mod1">
        <div class="mod-banner" style="background:linear-gradient(135deg,#6d28d9,#7c3aed,#9333ea);">
          <div>
            <div class="mod-tag">Motoru Kontrol Etmek</div>
            <h2>Modül 1: LLM Engineering &amp; Structured Outputs</h2>
          </div>
          <div class="mod-num-badge">01</div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c1);">1</span> Ne Öğreneceğiz &amp; Neden Önemli?</h3>
        <p>Bir <em>Agent</em> inşa etmeden önce onun çekirdeği olan <em>LLM</em>'i öngörülebilir biçimde yönetmeyi öğrenmeliyiz. Yazılımda serbest metinle işlem yapmak kırılganlık yaratır. Örneğin bir destek biletini otomatik yönlendirecekseniz kodunuzun net, doğrulanmış bir JSON nesnesine ihtiyacı vardır.</p>
        <div class="analogy-box">
          <div class="analogy-title">Günlük Hayattan Benzetme</div>
          Müşteri restoranda siparişi ne kadar dağınık anlatırsa anlatsın, garson mutfağa <strong>standart bir sipariş fişi</strong> verir. <strong>Structured Outputs</strong> da dağınık insan dilini yazılımın güvenle işleyeceği standart veri sözleşmesine (<em>Schema</em>) dönüştürür.
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c1);">2</span> Key Terminology (Kritik Kavramlar ve Tanımlar)</h3>
        {term_cards([
          ("Tokenization", "Metnin LLM tarafından işlenebilmesi için küçük parçalara (Token) bölünmesidir. Maliyet ve hız sınırları Token üzerinden ölçülür."),
          ("Context Window", "Modelin tek bir istekte hafızasında tutabileceği maksimum Token kapasitesidir (girdi + çıktı toplamı)."),
          ("System Prompt", "Modele rolünü, kurallarını, sınırlarını ve çıktı biçimini öğreten en yüksek öncelikli yönergedir."),
          ("Temperature", "Modelin yaratıcılık/rastgelelik düzeyidir. Mühendislik ve JSON görevlerinde tutarlılık için 0.0 kullanılır."),
          ("Structured Outputs", "Modelin serbest metin yerine önceden tanımlanmış bir JSON şemasına birebir uyan çıktı üretmesidir."),
          ("Immutable Dataclass", "Oluşturulduktan sonra değiştirilemeyen (frozen=True) veri yapısıdır; çoklu Thread erişiminde %100 güvenlidir."),
        ], "var(--c1)")}

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c1);">3</span> Adım Adım Teknik Anlatım</h3>
        <div class="diagram-box">
          <div class="diagram-caption">4 Aşamalı Güvenli LLM Çağrı Hattı</div>
          <div class="flow-row">
            <span class="f-node" style="background:var(--c1);">1. Token Bütçe Kontrolü</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#6366f1;">2. System Prompt + Temp=0.0</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#0ea5e9;">3. LLM JSON Çıktısı</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#059669;">4. Schema Validation</span>
          </div>
        </div>
        <p>Kodda <code>re.compile(...)</code> desenini modül başında bir kez derleyerek gereksiz CPU yükünü engelleriz (<em>High Efficiency</em>). <code>LLMRequestConfig</code> sınıfını <code>frozen=True, slots=True</code> yaparak hem bellek kullanımını azaltır hem de <em>Thread-Safety</em> sağlarız.</p>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c1);">4</span> Hands-On Lab (Eksiksiz Çalıştırılabilir Kod)</h3>
        {code_block(
          "Structured Outputs & Token Budget Lab",
          "labs/mod01_structured_llm.py",
          lab1,
          '''Ham JSON Çıktısı: {"category": "billing", "priority": "high", "summary": "Kullanıcı ödeme veya fatura sorunu bildiriyor."}
Doğrulanmış Nesne: TicketClassification(category='billing', priority='high', summary='Kullanıcı ödeme veya fatura sorunu bildiriyor.')
Tahmini Token Sayısı: 18'''
        )}

        <div class="split-grid">
          <div class="pitfall-card">
            <div class="pitfall-title">Common Pitfalls</div>
            <ul>
              <li>LLM'den dönen JSON'ı doğrulama (<em>Schema Validation</em>) yapmadan doğrudan veritabanına yazmak.</li>
              <li>Türkçe metinlerde <code>1 kelime = 1 token</code> varsaymak (eklemeli dillerde katsayı ~1.3'tür).</li>
            </ul>
          </div>
          <div class="challenge-card">
            <div class="challenge-title">Mini Challenge</div>
            <p><code>allowed_categories</code> kümesine <code>"refund"</code> kategorisini ekleyin ve <em>"Ürünü iade etmek istiyorum"</em> metni için yeni kural yazıp testi tekrar çalıştırın.</p>
          </div>
        </div>
      </section>

      <!-- ================= MODÜL 2 ================= -->
      <section class="module" id="mod2">
        <div class="mod-banner" style="background:linear-gradient(135deg,#0e7490,#0891b2,#06b6d4);">
          <div>
            <div class="mod-tag">Modele Eller ve Gözler Kazandırmak</div>
            <h2>Modül 2: Tool Use, Function Calling &amp; Agent Loop</h2>
          </div>
          <div class="mod-num-badge">02</div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c2);">1</span> Ne Öğreneceğiz &amp; Neden Önemli?</h3>
        <p>Bir <em>LLM</em>, şirketinizin canlı veritabanındaki sipariş durumunu göremez ve kesin finansal hesaplamalarda hata yapabilir. <strong>Tool Use</strong> sayesinde model tahminde bulunmak yerine sizin yazdığınız güvenilir Python fonksiyonunu çağırır ve gerçek veriyi kullanarak yanıt üretir.</p>
        <div class="analogy-box">
          <div class="analogy-title">Günlük Hayattan Benzetme</div>
          Bir pilot uçağın yüksekliğini göz kararı tahmin etmez; kokpitteki altimetre aracına bakar ve kesin veriyi okur. <strong>Tool</strong>, <em>LLM</em>'in güvenilir kokpit göstergesidir.
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c2);">2</span> Key Terminology (Kritik Kavramlar ve Tanımlar)</h3>
        {term_cards([
          ("Tool", "Agent'ın dış dünyayla etkileşime girmek veya kesin işlem yapmak için çağırdığı Python fonksiyonu veya API aracıdır."),
          ("Function Calling", "LLM'in serbest metin yerine hangi fonksiyonu hangi parametrelerle çağırmak istediğini yapılandırılmış biçimde bildirmesidir."),
          ("Agent Loop (Think-Act-Observe)", "Agent'ın düşünüp araç çağırdığı, sonucu gözlemlediği ve hedefe ulaşana kadar tekrarladığı döngüdür."),
          ("Max Steps", "Agent'ın sonsuz döngüye girip API bütçenizi tüketmesini önleyen zorunlu maksimum adım sınırıdır."),
        ], "var(--c2)")}

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c2);">3</span> Adım Adım Teknik Anlatım</h3>
        <div class="diagram-box">
          <div class="diagram-caption">Think &rarr; Act &rarr; Observe Döngüsü (LLM Kodu Çalıştırmaz, Uygulamanız Çalıştırır!)</div>
          <div class="flow-row">
            <span class="f-node" style="background:var(--c2);">1. THINK (Hangi Tool?)</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#0284c7;">2. ACT (ToolRegistry.execute)</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#059669;">3. OBSERVE (JSON Sonuç)</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#0f172a;">4. Kullanıcıya Cevap</span>
          </div>
        </div>
        <p>Dikkat edilmesi gereken <em>Concurrency</em> detayı: <code>ThreadSafeToolRegistry.execute</code> içinde <code>self._lock</code> yalnızca aracı sözlükten okurken tutulur; araç fonksiyonu çalışırken kilit serbesttir. Böylece yavaş bir dış API çağrısı diğer kullanıcıları bloklamaz.</p>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c2);">4</span> Hands-On Lab (Eksiksiz Çalıştırılabilir Kod)</h3>
        {code_block(
          "Thread-Safe Tool Registry & Agent Loop",
          "labs/mod02_tool_use_agent.py",
          lab2,
          '''Siparişiniz (ORD-101) şu an 'Kargoda' durumunda. Tahmini teslimat: 2 gün.
Kargo hesaplaması tamamlandı: {'free_shipping': True, 'shipping_fee': 0.0}'''
        )}

        <div class="split-grid">
          <div class="pitfall-card">
            <div class="pitfall-title">Common Pitfalls</div>
            <ul>
              <li><em>Agent Loop</em> içine <code>max_steps</code> sınırı koymamak (sonsuz döngü ve maliyet riski).</li>
              <li>Araç içinde oluşan hatayı yakalamayıp (<code>try/except</code>) tüm uygulamayı çökertmek.</li>
            </ul>
          </div>
          <div class="challenge-card">
            <div class="challenge-title">Mini Challenge</div>
            <p><code>cancel_order(order_id)</code> aracını yazın. Sipariş durumu <code>"Teslim Edildi"</code> ise iptali reddeden güvenli kuralı <code>ThreadSafeToolRegistry</code> içine kaydedin.</p>
          </div>
        </div>
      </section>

      <!-- ================= MODÜL 3 ================= -->
      <section class="module" id="mod3">
        <div class="mod-banner" style="background:linear-gradient(135deg,#047857,#059669,#10b981);">
          <div>
            <div class="mod-tag">Unutmayan ve Karıştırmayan Sistemler</div>
            <h2>Modül 3: Agent Memory &amp; State Management</h2>
          </div>
          <div class="mod-num-badge">03</div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c3);">1</span> Ne Öğreneceğiz &amp; Neden Önemli?</h3>
        <p><em>LLM</em> API'leri doğası gereği <strong>Stateless</strong> çalışır; her yeni istekte bir önceki mesajınızı unutur. Tutarlı bir asistan oluşturmak için hem son konuşmaları (<em>Short-Term Memory</em>) hem de kalıcı kullanıcı tercihlerini (<em>Long-Term Memory</em>) kullanıcı bazlı izole biçimde yönetmeliyiz.</p>
        <div class="analogy-box">
          <div class="analogy-title">Günlük Hayattan Benzetme</div>
          Bir doktor her hastanın geçmişini ezberlemez. Masadaki güncel muayene notlarını (<strong>Short-Term Memory</strong>) ve hastanın kronik alerjilerinin yazılı olduğu dosyayı (<strong>Long-Term Memory</strong>) birlikte kullanır.
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c3);">2</span> Key Terminology (Kritik Kavramlar ve Tanımlar)</h3>
        {term_cards([
          ("Stateless", "Önceki isteklerin bilgisini otomatik olarak saklamayan sistem özelliğidir."),
          ("Short-Term Memory", "Aktif konuşma penceresindeki son N mesajı tutan kısa süreli bellektir."),
          ("Long-Term Memory", "Oturumlar kapansa bile saklanan kullanıcı tercihleri ve kalıcı gerçeklerdir."),
          ("Bounded Memory (deque)", "RAM sızıntısını ve Context Window aşımını önlemek için en eski mesajları otomatik düşüren sabit boyutlu kuyruktur."),
          ("Session Isolation", "Farklı kullanıcıların konuşma verilerinin birbirine kesinlikle karışmamasını sağlayan oturum ayrımıdır."),
          ("State Snapshot", "İç durumu korumak için dışarıya orijinal referans yerine güvenli kopya döndürme desenidir."),
        ], "var(--c3)")}

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c3);">3</span> Adım Adım Teknik Anlatım</h3>
        <div class="diagram-box">
          <div class="diagram-caption">Session İzolasyonlu &amp; Sınırlı Bellek Mimarisi</div>
          <div class="flow-row">
            <span class="f-node" style="background:var(--c3);">Session ID: user-01</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#0f766e;">RLock Koruması</span><span class="f-arrow">&rarr;</span>
            <span class="f-node-light">Short-Term: deque(maxlen=4)</span><span class="f-arrow">+</span>
            <span class="f-node-light">Long-Term: dict</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#0f172a;">Güvenli Snapshot</span>
          </div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c3);">4</span> Hands-On Lab (Eksiksiz Çalıştırılabilir Kod)</h3>
        {code_block(
          "Thread-Safe Memory & State Manager",
          "labs/mod03_memory_and_state.py",
          lab3,
          '''Long-Term Facts: {'preferred_language': 'Python', 'experience_level': 'Junior'}
Short-Term Mesaj Sayısı (maxlen=4): 4
  - [user] Soru 3: Agent Memory nasıl çalışır?
  - [user] Soru 4: Agent Memory nasıl çalışır?
  - [user] Soru 5: Agent Memory nasıl çalışır?
  - [user] Soru 6: Agent Memory nasıl çalışır?'''
        )}

        <div class="split-grid">
          <div class="pitfall-card">
            <div class="pitfall-title">Common Pitfalls</div>
            <ul>
              <li>Tüm kullanıcıların mesajlarını tek bir global Python listesinde tutup veri sızıntısına yol açmak.</li>
              <li>Sınırsız mesaj biriktirerek hem RAM'i şişirmek hem de <em>Context Rot</em> (dikkat dağılması) yaşamak.</li>
            </ul>
          </div>
          <div class="challenge-card">
            <div class="challenge-title">Mini Challenge</div>
            <p><code>ThreadSafeMemoryManager</code> içine yalnızca <code>short_term</code> kuyruğunu temizleyen ama <code>long_term_facts</code> verisini koruyan <code>clear_short_term(session_id)</code> metodunu ekleyin.</p>
          </div>
        </div>
      </section>

      <!-- ================= MODÜL 4 ================= -->
      <section class="module" id="mod4">
        <div class="mod-banner" style="background:linear-gradient(135deg,#b45309,#d97706,#f59e0b);">
          <div>
            <div class="mod-tag">Şirket Bilgisine Akıllı Erişim</div>
            <h2>Modül 4: RAG, Vector Databases &amp; Agentic RAG</h2>
          </div>
          <div class="mod-num-badge">04</div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c4);">1</span> Ne Öğreneceğiz &amp; Neden Önemli?</h3>
        <p>500 sayfalık şirket dokümanını her soruda <em>Prompt</em> içine yapıştıramazsınız. <strong>RAG</strong> (<em>Retrieval-Augmented Generation</em>), yalnızca soruyla ilgili paragrafları bulup modele verir. <strong>Agentic RAG</strong> ise ilk arama zayıf dönerse pes etmez; sorguyu yeniden yazarak (<em>Query Rewrite</em>) doğru bilgiyi yakalar.</p>
        <div class="analogy-box">
          <div class="analogy-title">Günlük Hayattan Benzetme</div>
          Açık kitap sınavında 500 sayfayı ezberlemezsiniz; içindekilerden ilgili 2 paragrafı bulup cevaplarsınız (<strong>RAG</strong>). İlk aradığınız kelimeyi bulamazsanız eş anlamlısıyla tekrar ararsınız (<strong>Agentic RAG</strong>).
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c4);">2</span> Key Terminology (Kritik Kavramlar ve Tanımlar)</h3>
        {term_cards([
          ("RAG", "LLM'in yanıt üretmeden önce harici bir bilgi tabanından ilgili metin parçalarını çekip bağlama eklemesidir."),
          ("Chunking", "Uzun dokümanların arama motorunun verimli bulabileceği küçük ve anlamlı parçalara (Chunk) bölünmesidir."),
          ("Embeddings & Vector DB", "Metinleri anlamsal sayısal vektörlere çeviren yapı ve bu vektörlerde hızlı arama yapan özel veritabanıdır."),
          ("Agentic RAG & Query Rewrite", "İlk arama skoru düşükse sorguyu otomatik iyileştirip tekrar arama yapan akıllı RAG döngüsüdür."),
        ], "var(--c4)")}

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c4);">3</span> Adım Adım Teknik Anlatım</h3>
        <div class="diagram-box">
          <div class="diagram-caption">Agentic RAG Karar Döngüsü</div>
          <div class="flow-row">
            <span class="f-node" style="background:var(--c4);">Kullanıcı Sorusu</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#ea580c;">Vector Search</span><span class="f-arrow">&rarr;</span>
            <span class="f-node-light">Skor &ge; 0.25?</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#059669;">EVET: Cevapla</span>
            <span class="f-arrow">|</span>
            <span class="f-node" style="background:#dc2626;">HAYIR: Query Rewrite &rarr; Tekrar Ara</span>
          </div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c4);">4</span> Hands-On Lab (Eksiksiz Çalıştırılabilir Kod)</h3>
        {code_block(
          "In-Memory Vector Store & Agentic RAG Query Rewrite",
          "labs/mod04_agentic_rag.py",
          lab4,
          '''Sorgu 1 (Net): [İlk Aramada Bulundu | Skor: 0.49] -> Müşteriler teslimattan itibaren 14 gün içinde ücretsiz kargo ile iade politikası kapsamında ürün iade edebilir.
Sorgu 2 (Belirsiz): [Agentic Query Rewrite Uygulandı | Yeni Skor: 0.40] -> Müşteriler teslimattan itibaren 14 gün içinde ücretsiz kargo ile iade politikası kapsamında ürün iade edebilir.'''
        )}

        <div class="split-grid">
          <div class="pitfall-card">
            <div class="pitfall-title">Common Pitfalls</div>
            <ul>
              <li><em>Chunk</em> boyutunu çok küçük tutup bağlamı koparmak veya çok büyük tutup gürültü üretmek.</li>
              <li>Benzerlik skorunu (<code>min_score</code>) kontrol etmeden alakasız metni modele verip halüsinasyon üretmek.</li>
            </ul>
          </div>
          <div class="challenge-card">
            <div class="challenge-title">Mini Challenge</div>
            <p><code>ThreadSafeVectorStore</code> içine kargo politikası dokümanı ekleyin ve <em>"teslimat parası öder miyim?"</em> sorusuyla <em>Query Rewrite</em> adımını test edin.</p>
          </div>
        </div>
      </section>

      <!-- ================= MODÜL 5 ================= -->
      <section class="module" id="mod5">
        <div class="mod-banner" style="background:linear-gradient(135deg,#be185d,#db2777,#ec4899);">
          <div>
            <div class="mod-tag">Agentic AI Dünyasının USB-C Standardı</div>
            <h2>Modül 5: Model Context Protocol (MCP)</h2>
          </div>
          <div class="mod-num-badge">05</div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c5);">1</span> Ne Öğreneceğiz &amp; Neden Önemli?</h3>
        <p>Bir şirkette 3 farklı AI uygulaması ve 5 farklı dış sistem (GitHub, Jira, Slack, SQL, Depo) olduğunda her çift için ayrı bağlantı kodu yazmak bakım kâbusudur (3 &times; 5 = 15 entegrasyon). <strong>Model Context Protocol (MCP)</strong>, bir aracı tek bir standartla sunmanızı ve tüm <em>Agent</em>'ların onu anında keşfedip kullanmasını sağlar.</p>
        <div class="analogy-box">
          <div class="analogy-title">Günlük Hayattan Benzetme</div>
          Eskiden her telefonun farklı şarj girişi vardı; bugün <strong>USB-C</strong> ile tek kablo her cihazda çalışır. <strong>MCP</strong>, yapay zekâ araçlarının USB-C standardıdır.
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c5);">2</span> Key Terminology (Kritik Kavramlar ve Tanımlar)</h3>
        {term_cards([
          ("Model Context Protocol (MCP)", "AI uygulamalarının harici araç ve veri kaynaklarına tek bir açık standartla bağlanmasını sağlayan protokoldür."),
          ("MCP Server", "Araçları (Tools) ve veri kaynaklarını JSON-RPC 2.0 formatında dış dünyaya sunan servis katmanıdır."),
          ("MCP Client", "Agent tarafında yaşayan; sunucudan araçları keşfeden (tools/list) ve çağıran (tools/call) istemcidir."),
          ("JSON-RPC 2.0", "Uzaktaki fonksiyonları standart JSON mesajlarıyla çağırmak için kullanılan hafif iletişim protokolüdür."),
        ], "var(--c5)")}

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c5);">3</span> Adım Adım Teknik Anlatım</h3>
        <div class="diagram-box">
          <div class="diagram-caption">Standart MCP Keşif (Discovery) ve Çağrı (Execution) Akışı</div>
          <div class="flow-row">
            <span class="f-node" style="background:var(--c5);">MCP Client (Agent)</span><span class="f-arrow">&rarr;</span>
            <span class="f-node-light">1. tools/list</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#9d174d;">MCP Server</span><span class="f-arrow">&rarr;</span>
            <span class="f-node-light">2. tools/call (SKU)</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#059669;">JSON-RPC Sonuç</span>
          </div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c5);">4</span> Hands-On Lab (Eksiksiz Çalıştırılabilir Kod)</h3>
        {code_block(
          "JSON-RPC 2.0 MCP Server & Client Discovery",
          "labs/mod05_mcp_client_server.py",
          lab5,
          '''MCP tools/list Yanıtı: {"jsonrpc": "2.0", "id": 1, "result": {"tools": [{"name": "check_inventory", "description": "Depo stok durumunu SKU koduna göre sorgular.", "inputSchema": {"type": "object", "properties": {"sku": {"type": "string"}}, "required": ["sku"]}}]}}
MCP tools/call Yanıtı: {"jsonrpc": "2.0", "id": 2, "result": {"sku": "SKU-LAPTOP-01", "in_stock": 12}}'''
        )}

        <div class="split-grid">
          <div class="pitfall-card">
            <div class="pitfall-title">Common Pitfalls</div>
            <ul>
              <li>Tek bir <em>MCP Server</em> içine 50 alakasız araç doldurup <em>LLM</em>'in seçim kalitesini düşürmek.</li>
              <li>Veritabanı silme gibi tehlikeli araçlara yetkilendirme (<em>Authorization</em>) koymadan erişim açmak.</li>
            </ul>
          </div>
          <div class="challenge-card">
            <div class="challenge-title">Mini Challenge</div>
            <p><code>SimpleMCPServer</code> içine <code>reserve_inventory</code> adında ikinci bir araç kaydedin ve <code>tools/list</code> çıktısında her iki aracın da listelendiğini doğrulayın.</p>
          </div>
        </div>
      </section>

      <!-- ================= MODÜL 6 ================= -->
      <section class="module" id="mod6">
        <div class="mod-banner" style="background:linear-gradient(135deg,#3730a3,#4f46e5,#6366f1);">
          <div>
            <div class="mod-tag">Çoklu Ajan Koordinasyonu &amp; Karar Matrisi</div>
            <h2>Modül 6: Planning &amp; Multi-Agent Orchestration</h2>
          </div>
          <div class="mod-num-badge">06</div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c6);">1</span> Ne Öğreneceğiz &amp; Neden Önemli?</h3>
        <p>Tek bir <em>Prompt</em> içine hem araştırma, hem yazma hem de kalite denetimi yüklediğinizde çıktı kalitesi düşer. Tıpkı bir yazılım ekibinde olduğu gibi rolleri (<strong>Planner</strong>, <strong>Writer</strong>, <strong>Reviewer</strong>) ayırmak ve aralarındaki geçişleri koşullu bir grafikle (<strong>Stateful Workflow</strong>) yönetmek çok daha kararlı sonuçlar verir.</p>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c6);">2</span> Key Terminology &amp; 2027 Framework Karar Matrisi</h3>
        {term_cards([
          ("Planning", "Büyük bir hedefi sıralı ve yürütülebilir küçük alt görevlere bölme sürecidir."),
          ("Stateful Workflow (Graph)", "Adımların Node, geçişlerin Edge olarak modellendiği ve ortak State nesnesinin aktarıldığı mimaridir."),
          ("Conditional Edge", "Bir düğümün çıktısına göre sıradaki adımın dinamik seçilmesidir (ör. onaylanmazsa geri dön)."),
          ("Trade-off", "Bir mimari seçimin kazandırdığı avantajlar karşılığında kabul edilen maliyet veya kısıttır."),
        ], "var(--c6)")}

        <table class="styled-table">
          <thead>
            <tr>
              <th>Framework / Araç</th>
              <th>Temel Yaklaşım</th>
              <th>En Güçlü Senaryo</th>
              <th>Mimari Trade-off</th>
            </tr>
          </thead>
          <tbody>
            <tr><td><strong>LangGraph</strong></td><td>Graf tabanlı <em>Stateful Workflow</em></td><td>Karmaşık döngüler &amp; <em>Production</em> kontrolü</td><td>Graf yapısını tasarlamak başta daha fazla disiplin ister.</td></tr>
            <tr><td><strong>CrewAI</strong></td><td>Rol tabanlı ekip (<em>Role / Goal</em>)</td><td>Hızlı prototip, araştırma &amp; içerik akışları</td><td>Çok ince <em>State</em> kontrolünde esneklik azalabilir.</td></tr>
            <tr><td><strong>OpenAI Agents SDK</strong></td><td>Hafif, minimalist <em>Handoff</em> döngüsü</td><td>Sade, düşük soyutlamalı hızlı ajanlar</td><td>Karmaşık graf dallanmalarını elle yönetmek gerekir.</td></tr>
            <tr><td><strong>AutoGen</strong></td><td>Sohbet tabanlı çoklu ajan</td><td>Kod yazma &amp; doğrulama tartışmaları</td><td>Sınırlandırılmazsa yüksek <em>Token</em> tüketebilir.</td></tr>
            <tr><td><strong>n8n</strong></td><td>Görsel <em>Low-Code Automation</em></td><td>Slack, CRM, e-posta iş süreçleri</td><td>Özel <em>Concurrency</em> mantığı için kod tabanlı çözümler üstündür.</td></tr>
          </tbody>
        </table>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c6);">3</span> Adım Adım Teknik Anlatım</h3>
        <div class="diagram-box">
          <div class="diagram-caption">LangGraph Benzeri Koşullu Geçişli (Conditional Edge) Graf Motoru</div>
          <div class="flow-row">
            <span class="f-node" style="background:var(--c6);">Planner Node</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#0284c7;">Writer Node</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#d97706;">Reviewer Node</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#dc2626;">Red: Writer'a Dön</span>
            <span class="f-arrow">|</span>
            <span class="f-node" style="background:#059669;">Onay: END</span>
          </div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c6);">4</span> Hands-On Lab (Eksiksiz Çalıştırılabilir Kod)</h3>
        {code_block(
          "Immutable State Graph Engine (Planner -> Writer -> Reviewer)",
          "labs/mod06_stateful_workflow.py",
          lab6,
          '''[GRAPH] Çalıştırılan Node: planner
[GRAPH] Çalıştırılan Node: writer
[GRAPH] Çalıştırılan Node: reviewer
[GRAPH] Reviewer reddetti -> Writer düğümüne geri dönülüyor.
[GRAPH] Çalıştırılan Node: writer
[GRAPH] Çalıştırılan Node: reviewer

--- SONUÇ ---
Onay Durumu: True
Revizyon Sayısı: 2
Nihai Taslak: Agentic AI State Management kapsamlı özet -> Agentic AI State Management nedir? | Neden Production ortamında kritik önem taşır? | Basit bir uygulama örneği. Örnek: State izole edilmelidir.'''
        )}

        <div class="split-grid">
          <div class="pitfall-card">
            <div class="pitfall-title">Common Pitfalls</div>
            <ul>
              <li>Tek <em>LLM</em> çağrısıyla çözülecek basit bir iş için gereksiz yere 4 ajan kurup gecikmeyi katlamak.</li>
              <li>Düğümler arasında paylaşılan <em>State</em>'i yerinde değiştirip (<em>Mutate</em>) hata ayıklamayı zorlaştırmak.</li>
            </ul>
          </div>
          <div class="challenge-card">
            <div class="challenge-title">Mini Challenge</div>
            <p><code>reviewer_node</code> içine <code>"Production"</code> kelimesi zorunluluğu ekleyin ve <code>writer_node</code>'un revizyonda bu kuralı geçmesini sağlayın.</p>
          </div>
        </div>
      </section>

      <!-- ================= MODÜL 7 ================= -->
      <section class="module" id="mod7">
        <div class="mod-banner" style="background:linear-gradient(135deg,#991b1b,#dc2626,#ef4444);">
          <div>
            <div class="mod-tag">Canlı Ortam Dayanıklılığı &amp; Kariyer Koruması</div>
            <h2>Modül 7: Production-Ready Engineering &amp; 3 Kritik Tuzak</h2>
          </div>
          <div class="mod-num-badge">07</div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c7);">1</span> Ne Öğreneceğiz &amp; Neden Önemli?</h3>
        <p>Kendi bilgisayarınızda çalışan bir prototip yapmak kolaydır; zor olan onu canlı ortamda (<em>Production</em>) ayakta tutmaktır. API'ler <code>429 Rate Limit</code> döndürebilir veya bir <em>Prompt</em> değişikliği eski davranışları bozabilir. <strong>Observability</strong>, <strong>Retry/Fallback</strong> ve <strong>Evaluation</strong> canlı sistemin sigortasıdır.</p>
        <div class="analogy-box">
          <div class="analogy-title">Günlük Hayattan Benzetme</div>
          <strong>Observability</strong> uçağın kara kutusu, <strong>Fallback</strong> yedek motoru, <strong>Evaluation</strong> ise her bakım sonrası yapılan test uçuşudur.
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c7);">2</span> Key Terminology &amp; LoRA/QLoRA Ne Zaman Gerekir?</h3>
        {term_cards([
          ("Observability (LangSmith Mantığı)", "Agent'ın her adımındaki süreyi, hataları ve araç çağrılarını Trace/Span olarak kayıt altına almaktır."),
          ("Evaluation (Evals)", "Agent yanıtlarının doğruluk ve format kriterlerine göre otomatik test setleriyle ölçülmesidir."),
          ("Retry & Fallback", "Geçici hatalarda artan bekleme süresiyle (Exponential Backoff) yeniden denemek; olmazsa yedek modele geçmektir."),
          ("LoRA / QLoRA", "Güncel veri için RAG kullanılır; LoRA/QLoRA yalnızca çok özel üslup veya küçük açık model optimizasyonu gerektiğinde tercih edilir."),
        ], "var(--c7)")}

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c7);">3</span> 2027 Yolculuğunda Kaçınmanız Gereken 3 Kritik Tuzak</h3>
        <div class="traps-grid">
          <div class="trap-card">
            <div class="trap-num">Tuzak #1</div>
            <div class="trap-h">Temelleri Atlayıp Framework Ezberlemek</div>
            <p class="trap-p">Python, API, <em>Evaluation</em> ve <em>Software Architecture</em> bilmeden yalnızca <em>LangChain</em> ezberlemek risklidir. Framework'ler değişir, mühendislik temelleri kalıcıdır.</p>
          </div>
          <div class="trap-card">
            <div class="trap-num">Tuzak #2</div>
            <div class="trap-h">Her Aracı Aynı Anda Öğrenmeye Çalışmak</div>
            <p class="trap-p">Aynı hafta 5 farklı aracı kurmak zihinsel dağınıklık yaratır. Önce mimari <em>Trade-off</em>'ları anlayıp projenize uyan <strong>tek bir</strong> araçta derinleşin.</p>
          </div>
          <div class="trap-card">
            <div class="trap-num">Tuzak #3</div>
            <div class="trap-h">Kurs Biriktirmek (Tutorial Hell)</div>
            <p class="trap-p">Pasif video izlemek sizi <em>AI Engineer</em> yapmaz. Tek bir rota seçip klavyeye dokunun ve gerçek bir problem çözen çalışan bir <em>Agent</em> inşa edin.</p>
          </div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c7);">4</span> Hands-On Lab (Eksiksiz Çalıştırılabilir Kod)</h3>
        {code_block(
          "Retry, Fallback, Observability Trace & Evaluation",
          "labs/mod07_production_guardrails.py",
          lab7,
          '''Nihai Cevap: İade süresi 14 gündür ve kargo ücretsizdir.
Evaluation Raporu: {'passed': True, 'missing_keywords': []}

--- OBSERVABILITY TRACE ---
  [ERROR] primary_llm (0.00 ms) -> attempt=1: 429 Rate Limit Exceeded
  [ERROR] primary_llm (0.01 ms) -> attempt=2: 429 Rate Limit Exceeded
  [ERROR] primary_llm (0.01 ms) -> attempt=3: 429 Rate Limit Exceeded
  [OK] fallback_llm (0.00 ms) -> fallback_triggered'''
        )}

        <div class="split-grid">
          <div class="pitfall-card">
            <div class="pitfall-title">Common Pitfalls</div>
            <ul>
              <li>Canlı sistemde yapılandırılmış <em>Trace</em> yerine düz <code>print()</code> kullanmak.</li>
              <li><code>401 Invalid API Key</code> gibi kalıcı hatalarda gereksiz <em>Retry</em> döngüsüne girmek.</li>
            </ul>
          </div>
          <div class="challenge-card">
            <div class="challenge-title">Mini Challenge</div>
            <p><code>unstable_primary</code> fonksiyonunu 2. denemede başarılı olacak biçimde değiştirin ve <em>Fallback</em> tetiklenmeden işlemin bittiğini <em>Trace</em> çıktısında gözlemleyin.</p>
          </div>
        </div>
      </section>

      <!-- ================= MODÜL 8 ================= -->
      <section class="module" id="mod8">
        <div class="mod-banner" style="background:linear-gradient(135deg,#115e59,#0d9488,#14b8a6);">
          <div>
            <div class="mod-tag">Tüm Parçaların Birleşimi</div>
            <h2>Modül 8: Capstone Mini-Project &amp; 14 Günlük Pratik Planı</h2>
          </div>
          <div class="mod-num-badge">08</div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c8);">1</span> Ne Öğreneceğiz &amp; Neden Önemli?</h3>
        <p>Bu bitirme projesinde <em>Tool Use</em>, <em>RAG</em>, <em>Session Memory</em> ve <em>Observability</em> katmanlarını tek bir sistemde birleştiriyor ve <code>ThreadPoolExecutor</code> ile 4 eşzamanlı (<em>Concurrent</em>) müşteri isteğini aynı anda güvenle işliyoruz.</p>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c8);">2</span> Key Terminology (Kritik Kavramlar ve Tanımlar)</h3>
        {term_cards([
          ("Concurrency", "Birden fazla kullanıcı isteğinin aynı zaman aralığında paralel olarak işlenebilmesidir."),
          ("Race Condition", "Paralel Thread'lerin paylaşılan veriyi kilitsiz değiştirmesi sonucu oluşan tutarsızlık hatasıdır."),
          ("Routing", "Kullanıcı niyetine göre isteğin doğru alt bileşene (Tool, RAG veya Fallback) yönlendirilmesidir."),
          ("Latency", "İsteğin sisteme girmesi ile yanıtın dönmesi arasında geçen milisaniye cinsinden süredir."),
        ], "var(--c8)")}

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c8);">3</span> Capstone Uçtan Uca Mimari Akışı</h3>
        <div class="diagram-box">
          <div class="diagram-caption">Eşzamanlı (Concurrent) Production Support Agent</div>
          <div class="flow-row">
            <span class="f-node" style="background:var(--c8);">4 Paralel İstek (ThreadPool)</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#0f766e;">Session State (RLock)</span><span class="f-arrow">&rarr;</span>
            <span class="f-node-light">Routing: Tool / RAG / Fallback</span><span class="f-arrow">&rarr;</span>
            <span class="f-node" style="background:#0f172a;">TraceSpan + Yanıt</span>
          </div>
        </div>

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c8);">4</span> Hands-On Lab (Eksiksiz Capstone Kodu)</h3>
        {code_block(
          "End-to-End Concurrent Production Support Agent",
          "labs/mod08_capstone_agent.py",
          lab8,
          '''[sess-1] Soru: ORD-500 siparişim ne durumda?
[sess-1] Yanıt: [Tool:OrderLookup] ORD-500 durumu -> Hazırlanıyor (Tahmini kargo: Yarın)

[sess-2] Soru: Ürünü beğenmezsem iade süresi kaç gün?
[sess-2] Yanıt: [RAG:Policy] Teslimattan itibaren 14 gün içinde ücretsiz iade hakkınız vardır.

[sess-3] Soru: Kulaklıkların garanti süresi ne kadar?
[sess-3] Yanıt: [RAG:Policy] Tüm elektronik ürünlerde 24 ay resmi distribütör garantisi bulunur.

[sess-1] Soru: Teşekkürler, peki ORD-501 nerede?
[sess-1] Yanıt: [Tool:OrderLookup] ORD-501 durumu -> Kargoda (Takip No: TR998877)

--- CAPSTONE OBSERVABILITY TRACES ---
  sess-1 | tool_order_lookup | 0.026 ms | SUCCESS
  sess-2 | rag_policy_search | 0.009 ms | SUCCESS
  sess-3 | rag_policy_search | 0.008 ms | SUCCESS
  sess-1 | tool_order_lookup | 0.009 ms | SUCCESS'''
        )}

        <h3 class="sec-h"><span class="sec-pill" style="background:var(--c8);">5</span> 14 Günlük Hemen Uygulanabilir Pratik Planı</h3>
        <div class="roadmap-grid">
          <div class="day-card"><span class="day-badge">Gün 1–2:</span> Modül 0 &amp; 1'i çalıştırın; kendi JSON şemanızı (ör. CV özetleyici) tasarlayın.</div>
          <div class="day-card"><span class="day-badge">Gün 3–4:</span> Modül 2'ye 2 yeni <em>Tool</em> (döviz çevirici, tarih hesaplayıcı) ekleyin.</div>
          <div class="day-card"><span class="day-badge">Gün 5–6:</span> Modül 3'teki belleği JSON dosyasına kaydedip geri yükleyin (<em>Persistence</em>).</div>
          <div class="day-card"><span class="day-badge">Gün 7–8:</span> Modül 4'ü kendi ders/iş notlarınızla farklı <code>chunk_size</code> değerlerinde test edin.</div>
          <div class="day-card"><span class="day-badge">Gün 9–10:</span> Modül 5'te 2 farklı aracı tek <em>MCP Server</em> üzerinden dışarı açın.</div>
          <div class="day-card"><span class="day-badge">Gün 11–12:</span> Modül 6'da 3 düğümlü kendi <em>Stateful Workflow</em> onay grafınızı kurun.</div>
          <div class="day-card" style="grid-column:span 2;"><span class="day-badge">Gün 13–14:</span> Modül 7 &amp; 8'i birleştirip gerçek bir <em>LLM API</em> (veya yerel <em>Ollama</em>) bağlayın, <em>Evaluation</em> testlerini geçip GitHub portföyünüzde yayınlayın.</div>
        </div>
      </section>

      <!-- ================= MASTER GLOSSARY ================= -->
      <section class="module" id="glossary">
        <div class="mod-banner" style="background:linear-gradient(135deg,#0f172a,#1e293b,#334155);">
          <div>
            <div class="mod-tag">Hızlı Referans Sözlüğü</div>
            <h2>Master Glossary (33 Kritik Teknik Terim)</h2>
          </div>
          <div class="mod-num-badge">A–Z</div>
        </div>

        <div class="glossary-grid">
          <div class="gloss-item"><strong>Agent Loop:</strong> Hedefe ulaşana kadar <em>Think &rarr; Act &rarr; Observe</em> adımlarını tekrarlayan yürütme döngüsüdür.</div>
          <div class="gloss-item"><strong>Agent Memory:</strong> Konuşma geçmişini (<em>Short-Term</em>) ve kalıcı bilgileri (<em>Long-Term</em>) saklama katmanıdır.</div>
          <div class="gloss-item"><strong>Agentic AI:</strong> Planlama, araç kullanımı, bellek ve öz-değerlendirme yapabilen hedef odaklı sistem mimarisidir.</div>
          <div class="gloss-item"><strong>Agentic RAG:</strong> Zayıf arama sonuçlarını fark edip sorguyu yeniden yazarak (<em>Query Rewrite</em>) tekrar arayan RAG modelidir.</div>
          <div class="gloss-item"><strong>Bounded Memory:</strong> Bellek taşmasını önlemek için yalnızca son N kaydı tutan sabit boyutlu yapıdır (<code>deque</code>).</div>
          <div class="gloss-item"><strong>Chunking:</strong> Uzun dokümanların vektör aramasına uygun küçük parçalara bölünmesidir.</div>
          <div class="gloss-item"><strong>Concurrency:</strong> Birden fazla isteğin aynı zaman aralığında paralel olarak işlenebilmesidir.</div>
          <div class="gloss-item"><strong>Conditional Edge:</strong> Graf akışında mevcut <em>State</em>'e göre sıradaki düğümün dinamik belirlenmesidir.</div>
          <div class="gloss-item"><strong>Context Window:</strong> Modelin tek istekte işleyebileceği maksimum <em>Token</em> kapasitesidir.</div>
          <div class="gloss-item"><strong>Cosine Similarity:</strong> İki vektör arasındaki anlamsal yakınlığı 0.0–1.0 arasında ölçen metriktir.</div>
          <div class="gloss-item"><strong>Deployment:</strong> Uygulamanın gerçek kullanıcıların erişebileceği canlı sunucuya alınmasıdır.</div>
          <div class="gloss-item"><strong>Embeddings:</strong> Metinleri anlamsal olarak karşılaştırılabilir sayısal vektörlere dönüştüren temsillerdir.</div>
          <div class="gloss-item"><strong>Evaluation (Evals):</strong> <em>Agent</em> çıktılarının doğruluk ve format kriterlerine göre otomatik ölçülmesidir.</div>
          <div class="gloss-item"><strong>Fallback:</strong> Birincil servis başarısız olduğunda devreye giren güvenli yedek çalışma yoludur.</div>
          <div class="gloss-item"><strong>Function Calling:</strong> <em>LLM</em>'in çağrılacak fonksiyonu ve parametrelerini yapılandırılmış biçimde bildirmesidir.</div>
          <div class="gloss-item"><strong>Immutable State:</strong> Oluşturulduktan sonra yerinde değiştirilmeyen, <em>Thread-Safe</em> durum nesnesidir.</div>
          <div class="gloss-item"><strong>JSON-RPC 2.0:</strong> <em>MCP</em> iletişiminde kullanılan hafif JSON tabanlı uzak fonksiyon çağrı protokolüdür.</div>
          <div class="gloss-item"><strong>Latency:</strong> İsteğin gönderilmesi ile yanıtın alınması arasında geçen toplam bekleme süresidir.</div>
          <div class="gloss-item"><strong>LLM (Large Language Model):</strong> Büyük ölçekli metin verileriyle eğitilmiş dil modelidir.</div>
          <div class="gloss-item"><strong>LoRA / QLoRA:</strong> Büyük modelleri düşük bellek maliyetiyle belirli bir alana uyarlayan <em>Fine-Tuning</em> tekniğidir.</div>
          <div class="gloss-item"><strong>Max Steps:</strong> Sonsuz döngüyü ve beklenmeyen API maliyetini önleyen adım sınırıdır.</div>
          <div class="gloss-item"><strong>Model Context Protocol (MCP):</strong> AI uygulamalarını harici araçlara bağlayan açık standart protokoldür.</div>
          <div class="gloss-item"><strong>Multi-Agent Orchestration:</strong> Birden fazla uzman <em>Agent</em>'ın kurallı iş akışıyla birlikte yönetilmesidir.</div>
          <div class="gloss-item"><strong>Observability:</strong> Sistemin iç adımlarını, sürelerini ve hatalarını <em>Trace</em> kayıtlarıyla izleyebilme yeteneğidir.</div>
          <div class="gloss-item"><strong>Planning:</strong> Karmaşık hedefi sıralı ve doğrulanabilir alt görevlere ayırma sürecidir.</div>
          <div class="gloss-item"><strong>Prompt-and-Response:</strong> Tek seferlik girdi-çıktı mantığına dayanan statik <em>LLM</em> kullanımıdır.</div>
          <div class="gloss-item"><strong>Race Condition:</strong> Paralel <em>Thread</em>'lerin paylaşılan veriyi kontrolsüz değiştirmesiyle oluşan hatadır.</div>
          <div class="gloss-item"><strong>RAG:</strong> Modelin yanıt üretmeden önce harici bilgi tabanından ilgili veriyi çekip kullanmasıdır.</div>
          <div class="gloss-item"><strong>Retry &amp; Exponential Backoff:</strong> Geçici hatalarda artan bekleme süreleriyle kontrollü yeniden deneme stratejisidir.</div>
          <div class="gloss-item"><strong>State Management:</strong> Çok adımlı akışlarda verinin tutarlı ve izole biçimde yönetilmesidir.</div>
          <div class="gloss-item"><strong>Structured Outputs:</strong> Model çıktısının katı bir JSON şemasına birebir uymasıdır.</div>
          <div class="gloss-item"><strong>Thread-Safety:</strong> Çoklu <em>Thread</em> erişiminde veri bütünlüğünün kilit veya değişmezlikle korunmasıdır.</div>
          <div class="gloss-item"><strong>Tokenization &amp; Vector DB:</strong> Metnin <em>Token</em>'lara ayrılması ve <em>Embedding</em> vektörlerinin hızlı aranmasıdır.</div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""
    return html_doc


def main() -> None:
    content = build_html()
    OUTPUT_HTML.write_text(content, encoding="utf-8")
    print(f"Created: {OUTPUT_HTML} ({len(content):,} bytes)")


if __name__ == "__main__":
    main()
