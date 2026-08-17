"""Render repository Markdown docs as HTML using the showcase stylesheet."""

from __future__ import annotations

import html
import re
from pathlib import Path

from flask import Response

from version import PRODUCT_NAME


def _inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r'`([^`]+)`', r'<code>\1</code>', escaped)
    escaped = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        r'<a href="\2">\1</a>',
        escaped,
    )
    escaped = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', escaped)
    escaped = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', escaped)
    return escaped


def markdown_to_html(source: str) -> str:
    lines = source.replace('\r\n', '\n').split('\n')
    out: list[str] = []
    i = 0
    in_code = False
    code_lines: list[str] = []
    list_type: str | None = None

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f'</{list_type}>')
            list_type = None

    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            if in_code:
                out.append('<pre class="code-block"><code>')
                out.append(html.escape('\n'.join(code_lines)))
                out.append('</code></pre>')
                code_lines = []
                in_code = False
            else:
                close_list()
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if re.match(r'^\|(.+)\|$', line) and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i + 1]):
            close_list()
            headers = [cell.strip() for cell in line.strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and re.match(r'^\|(.+)\|$', lines[i]):
                rows.append([cell.strip() for cell in lines[i].strip('|').split('|')])
                i += 1
            out.append('<table>')
            out.append('<thead><tr>' + ''.join(f'<th>{_inline(h)}</th>' for h in headers) + '</tr></thead>')
            out.append('<tbody>')
            for row in rows:
                out.append('<tr>' + ''.join(f'<td>{_inline(c)}</td>' for c in row) + '</tr>')
            out.append('</tbody></table>')
            continue

        if not line.strip():
            close_list()
            i += 1
            continue

        heading = re.match(r'^(#{1,4})\s+(.*)$', line)
        if heading:
            close_list()
            level = len(heading.group(1))
            out.append(f'<h{level}>{_inline(heading.group(2))}</h{level}>')
            i += 1
            continue

        unordered = re.match(r'^[-*]\s+(.*)$', line)
        ordered = re.match(r'^\d+\.\s+(.*)$', line)
        if unordered or ordered:
            kind = 'ul' if unordered else 'ol'
            if list_type != kind:
                close_list()
                list_type = kind
                out.append(f'<{kind}>')
            item = unordered.group(1) if unordered else ordered.group(1)
            out.append(f'<li>{_inline(item)}</li>')
            i += 1
            continue

        close_list()
        out.append(f'<p>{_inline(line)}</p>')
        i += 1

    close_list()
    if in_code:
        out.append('<pre class="code-block"><code>')
        out.append(html.escape('\n'.join(code_lines)))
        out.append('</code></pre>')
    return '\n'.join(out)


def render_markdown_page(path: Path, title: str | None = None) -> Response:
    source = path.read_text(encoding='utf-8')
    heading = title
    for line in source.splitlines():
        if line.startswith('# '):
            heading = line[2:].strip()
            break
    heading = heading or path.name
    body = markdown_to_html(source)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>{html.escape(heading)} — {html.escape(PRODUCT_NAME)}</title>
  <link rel="stylesheet" href="/showcase/styles.css" />
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="brand-block">
      <span class="org">Michigan MindMend Inc.</span>
      <strong class="product">{html.escape(PRODUCT_NAME)}</strong>
    </div>
    <nav class="site-nav open" aria-label="Docs">
      <a href="/">Showcase</a>
      <a href="/docs/">Docs index</a>
      <a href="/api/v1/status">Status JSON</a>
    </nav>
  </header>
  <main id="main" class="section docs-article">
    {body}
  </main>
</body>
</html>
"""
    return Response(page, mimetype='text/html; charset=utf-8')
