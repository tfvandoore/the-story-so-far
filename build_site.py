#!/usr/bin/env python3
"""
Build 'The Story So Far' as a static HTML page.
Same design language as Ari's Big Five (celestial navy + warm gold).
Single-page layout with floating table of contents.
"""

import re
import os

# ── Paths ────────────────────────────────────────────────────────────
SOURCE_MD = os.path.join(
    os.path.dirname(__file__),
    '..', '..', 'Aris place', 'the-story-so-far.md'
)
OUTPUT_HTML = os.path.join(os.path.dirname(__file__), 'index.html')

# ── CSS ──────────────────────────────────────────────────────────────
CSS = '''
:root {
    --text: #1a1a1a;
    --text-secondary: #5c564e;
    --bg: #faf8f4;
    --bg-card: #fff;
    --accent: #b08d57;
    --accent-hover: #96763f;
    --accent-light: #f5f0e6;
    --border: #ddd8cf;
    --quote-bg: #f8f5ee;
    --quote-border: #c9a96e;
    --hero-gradient-1: #1e2d3d;
    --hero-gradient-2: #0d1821;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 18px; }

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    color: var(--text);
    background: var(--bg);
    line-height: 1.75;
    -webkit-font-smoothing: antialiased;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, var(--hero-gradient-1), var(--hero-gradient-2));
    color: #fff;
    padding: 5rem 2rem 3.5rem;
    text-align: center;
}

.hero h1 {
    font-size: 2.8rem;
    font-weight: 400;
    letter-spacing: 0.02em;
    margin-bottom: 0.5rem;
}

.hero .subtitle {
    font-style: italic;
    font-size: 1.1rem;
    opacity: 0.85;
    margin-bottom: 1.5rem;
}

.hero .hero-stats {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.15);
}

.hero .stat {
    text-align: center;
}

.hero .stat-value {
    display: block;
    font-family: 'Helvetica Neue', 'Arial', sans-serif;
    font-size: 1.8rem;
    font-weight: 600;
    color: var(--accent);
}

.hero .stat-label {
    font-size: 0.8rem;
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: 'Helvetica Neue', 'Arial', sans-serif;
}

/* ── Floating TOC ── */
.toc-toggle {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 200;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 0.85rem;
    font-size: 0.85rem;
    font-family: 'Helvetica Neue', 'Arial', sans-serif;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    transition: background 0.2s;
}

.toc-toggle:hover { background: var(--accent-hover); }

.toc-panel {
    position: fixed;
    top: 0; right: 0; bottom: 0;
    width: 300px;
    background: var(--bg);
    border-left: 1px solid var(--border);
    z-index: 150;
    overflow-y: auto;
    padding: 3.5rem 1.5rem 2rem;
    transform: translateX(100%);
    transition: transform 0.3s;
    box-shadow: -4px 0 20px rgba(0,0,0,0.1);
}

.toc-panel.open { transform: translateX(0); }

.toc-panel h3 {
    font-family: 'Helvetica Neue', 'Arial', sans-serif;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--accent);
    margin-bottom: 1rem;
}

.toc-panel ul {
    list-style: none;
    padding: 0;
}

.toc-panel li {
    margin-bottom: 0.3rem;
}

.toc-panel a {
    display: block;
    font-family: 'Helvetica Neue', 'Arial', sans-serif;
    font-size: 0.82rem;
    color: var(--text);
    text-decoration: none;
    padding: 0.35rem 0.75rem;
    border-left: 2px solid transparent;
    border-radius: 0 4px 4px 0;
    transition: all 0.15s;
}

.toc-panel a:hover {
    background: var(--accent-light);
    color: var(--accent);
    border-left-color: var(--accent);
}

.toc-panel a.toc-sub {
    padding-left: 1.5rem;
    font-size: 0.78rem;
    color: var(--text-secondary);
}

/* ── Content ── */
.content {
    max-width: 760px;
    margin: 0 auto;
    padding: 3rem 1.5rem 4rem;
}

/* ── Date sections ── */
.date-section {
    margin-bottom: 3rem;
    scroll-margin-top: 2rem;
}

.date-section h2 {
    font-size: 1.6rem;
    font-weight: 400;
    margin-bottom: 0.3rem;
    color: var(--text);
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.date-section .date-intro {
    font-weight: 700;
    margin-bottom: 1rem;
}

/* ── Typography ── */
h2 {
    font-size: 1.6rem;
    font-weight: 400;
    margin: 3rem 0 1rem;
    scroll-margin-top: 2rem;
}

h3 {
    font-size: 1.2rem;
    font-weight: 400;
    margin: 2rem 0 0.8rem;
    color: var(--text);
    scroll-margin-top: 2rem;
}

p { margin-bottom: 1.25rem; }
strong { font-weight: 700; }
em { font-style: italic; }

ul, ol { margin-bottom: 1.25rem; padding-left: 1.5rem; }
li { margin-bottom: 0.4rem; }

li ul { margin-top: 0.3rem; margin-bottom: 0.3rem; }

a {
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
}

a:hover { border-bottom-color: var(--accent); }

code {
    font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
    font-size: 0.88em;
    background: var(--accent-light);
    padding: 0.15em 0.4em;
    border-radius: 3px;
    color: var(--text);
}

/* ── Tables ── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
    font-size: 0.92rem;
}

th {
    font-family: 'Helvetica Neue', 'Arial', sans-serif;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
    text-align: left;
    padding: 0.6rem 0.8rem;
    border-bottom: 2px solid var(--border);
    background: var(--accent-light);
}

td {
    padding: 0.55rem 0.8rem;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
}

tr:last-child td { border-bottom: 2px solid var(--border); }
tr:hover td { background: rgba(176, 141, 87, 0.04); }

/* Bold totals row */
tr:last-child td strong,
td strong {
    color: var(--text);
}

/* ── Horizontal rules as section dividers ── */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 3rem 0;
}

/* ── Blockquotes ── */
blockquote {
    border-left: 3px solid var(--quote-border);
    background: var(--quote-bg);
    padding: 1.25rem 1.5rem;
    margin: 2rem 0;
    border-radius: 0 6px 6px 0;
    font-style: italic;
}

blockquote p { margin-bottom: 0; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 1.5rem 3rem;
    color: var(--text-secondary);
    font-size: 0.85rem;
    max-width: 760px;
    margin: 0 auto;
    border-top: 1px solid var(--border);
}

.footer a { color: var(--accent); }

/* ── Responsive ── */
@media (max-width: 900px) {
    .hero { padding: 3.5rem 1.5rem 2.5rem; }
    .hero h1 { font-size: 2rem; }
    .hero .hero-stats { gap: 1.5rem; }
    .hero .stat-value { font-size: 1.4rem; }
    .toc-panel { width: 260px; }
}

@media (max-width: 600px) {
    html { font-size: 16px; }
    .hero { padding: 3rem 1rem 2rem; }
    .hero h1 { font-size: 1.6rem; }
    .hero .hero-stats { gap: 1rem; }
    .hero .stat-value { font-size: 1.2rem; }
    .content { padding: 2rem 1rem 3rem; }
    table { font-size: 0.82rem; }
    th, td { padding: 0.4rem 0.5rem; }
    .toc-panel { width: 240px; }
}
'''

# ── JS ───────────────────────────────────────────────────────────────
JS = '''
<script>
const tocBtn = document.querySelector('.toc-toggle');
const tocPanel = document.querySelector('.toc-panel');
tocBtn.addEventListener('click', () => tocPanel.classList.toggle('open'));
document.querySelector('.content').addEventListener('click', () => tocPanel.classList.remove('open'));
// Close TOC on link click (mobile)
tocPanel.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => tocPanel.classList.remove('open'));
});
</script>
'''


def slugify(text):
    """Create URL-safe slug from heading text."""
    text = re.sub(r'<[^>]+>', '', text)  # strip HTML
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[\s]+', '-', text).strip('-')


def md_to_html(md):
    """Convert markdown to HTML. Handles the subset used in the story doc."""
    lines = md.split('\n')
    html_lines = []
    in_list = False
    in_sub_list = False
    in_table = False
    table_has_header = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip YAML/frontmatter markers
        if line.strip() == '---':
            # Check if it's a horizontal rule (not at very start)
            if i > 2:
                if in_list:
                    if in_sub_list:
                        html_lines.append('</ul></li>')
                        in_sub_list = False
                    html_lines.append('</ul>')
                    in_list = False
                if in_table:
                    html_lines.append('</table>')
                    in_table = False
                html_lines.append('<hr>')
            i += 1
            continue

        # Tables
        if '|' in line and line.strip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]

            # Check if next line is separator
            if not in_table:
                if i + 1 < len(lines) and re.match(r'\s*\|[\s\-:|]+\|', lines[i + 1]):
                    # This is a header row
                    if in_list:
                        if in_sub_list:
                            html_lines.append('</ul></li>')
                            in_sub_list = False
                        html_lines.append('</ul>')
                        in_list = False
                    in_table = True
                    table_has_header = True
                    html_lines.append('<table>')
                    html_lines.append('<tr>' + ''.join(f'<th>{inline_format(c)}</th>' for c in cells) + '</tr>')
                    i += 2  # skip separator line
                    continue
                else:
                    # Table without header detection - treat as regular line
                    pass

            if in_table:
                html_lines.append('<tr>' + ''.join(f'<td>{inline_format(c)}</td>' for c in cells) + '</tr>')
                # Check if next line is not a table row
                if i + 1 >= len(lines) or not (lines[i + 1].strip().startswith('|')):
                    html_lines.append('</table>')
                    in_table = False
                i += 1
                continue

        # Headings
        heading_match = re.match(r'^(#{1,4})\s+(.+)', line)
        if heading_match:
            if in_list:
                if in_sub_list:
                    html_lines.append('</ul></li>')
                    in_sub_list = False
                html_lines.append('</ul>')
                in_list = False
            if in_table:
                html_lines.append('</table>')
                in_table = False
            level = len(heading_match.group(1))
            text = inline_format(heading_match.group(2))
            slug = slugify(heading_match.group(2))
            html_lines.append(f'<h{level} id="{slug}">{text}</h{level}>')
            i += 1
            continue

        # List items (sub-list: indented with 2+ spaces)
        sub_list_match = re.match(r'^  +[-*]\s+(.+)', line)
        list_match = re.match(r'^[-*]\s+(.+)', line)

        if sub_list_match:
            if not in_sub_list:
                html_lines.append('<ul>')
                in_sub_list = True
            html_lines.append(f'<li>{inline_format(sub_list_match.group(1))}</li>')
            i += 1
            continue

        if list_match:
            if in_sub_list:
                html_lines.append('</ul></li>')
                in_sub_list = False
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{inline_format(list_match.group(1))}</li>')
            i += 1
            continue

        # Close lists if we hit a non-list line
        if in_sub_list and not sub_list_match and not list_match:
            html_lines.append('</ul></li>')
            in_sub_list = False
        if in_list and not list_match and not sub_list_match:
            html_lines.append('</ul>')
            in_list = False

        # Empty lines
        if line.strip() == '':
            i += 1
            continue

        # Italic-only lines (like the "last updated" line)
        italic_match = re.match(r'^\*([^*]+)\*$', line.strip())
        if italic_match:
            html_lines.append(f'<p><em>{inline_format(italic_match.group(1))}</em></p>')
            i += 1
            continue

        # Regular paragraphs
        html_lines.append(f'<p>{inline_format(line)}</p>')
        i += 1

    # Close any open lists
    if in_sub_list:
        html_lines.append('</ul></li>')
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        html_lines.append('</table>')

    return '\n'.join(html_lines)


def inline_format(text):
    """Apply inline markdown formatting."""
    # Bold + italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Em-dash
    text = text.replace(' — ', ' &mdash; ').replace(' - ', ' &ndash; ')
    return text


def extract_toc(md):
    """Extract table of contents from markdown headings."""
    toc = []
    for match in re.finditer(r'^(#{2,3})\s+(.+)', md, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2)
        # Strip markdown formatting for display
        display = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        display = re.sub(r'\*(.+?)\*', r'\1', display)
        display = re.sub(r'`([^`]+)`', r'\1', display)
        display = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', display)
        slug = slugify(text)
        is_sub = level == 3
        toc.append((display, slug, is_sub))
    return toc


def build_toc_html(toc):
    """Build the TOC panel HTML."""
    items = []
    for display, slug, is_sub in toc:
        cls = ' class="toc-sub"' if is_sub else ''
        items.append(f'<li><a href="#{slug}"{cls}>{display}</a></li>')
    return '\n'.join(items)


def extract_hero_stats(md_content):
    """Extract hero stats dynamically from the markdown content."""
    stats = {
        'days': '28',
        'lines': '76k',
        'value': '$225k',
        'leverage': '32x',
    }

    # Calendar time from speed comparison table: "| Calendar time | XX days ..."
    m = re.search(r'Calendar time\s*\|\s*(\d+)\s*days', md_content)
    if m:
        stats['days'] = m.group(1)

    # Total lines from raw numbers table: "| **Total code & content** | **~76,200** |"
    m = re.search(r'Total code & content\*\*\s*\|\s*\*\*~?([\d,]+)\*\*', md_content)
    if m:
        num = int(m.group(1).replace(',', ''))
        stats['lines'] = f'{num // 1000}k'

    # Total cost from equivalent human effort table: "| **Total** | | **1,600** | | **$225,400** |"
    m = re.search(r'Total\*\*\s*\|[^|]*\|\s*\*\*[\d,]+\*\*\s*\|[^|]*\|\s*\*\*\$([\d,]+)\*\*', md_content)
    if m:
        num = int(m.group(1).replace(',', ''))
        stats['value'] = f'${num // 1000}k'

    # Leverage ratio from human side paragraph: "That's a **32x personal leverage ratio**"
    m = re.search(r'\*\*(\d+)x personal leverage ratio\*\*', md_content)
    if m:
        stats['leverage'] = f'{m.group(1)}x'

    return stats


def build_page(md_content):
    """Build the full HTML page from markdown content."""

    # Extract hero stats from the markdown itself
    hero = extract_hero_stats(md_content)

    # Strip the H1 title and subtitle - we'll put them in the hero
    lines = md_content.split('\n')
    # Find and skip the H1 and the subtitle line and the first ---
    body_start = 0
    for idx, line in enumerate(lines):
        if line.strip() == '---' and idx > 0:
            body_start = idx + 1
            break

    body_md = '\n'.join(lines[body_start:])

    # Strip the trailing "last updated" and "live document" lines
    body_md = re.sub(r'\n\*This is a live document\. Updated as we build\.\*\s*$', '', body_md)
    body_md = re.sub(r'\n\*Last updated:.*?\*\s*$', '', body_md)

    # Convert to HTML
    body_html = md_to_html(body_md)

    # Build TOC
    toc = extract_toc(body_md)
    toc_html = build_toc_html(toc)

    meta_desc = (
        f"A running log of everything Tim and Ari have built together. "
        f"Started as a Telegram bot, became something more. "
        f"{hero['days']} days, {hero['value']} equivalent, {hero['lines']} lines of code."
    )

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Story So Far &mdash; Tim &amp; Ari</title>
    <meta name="description" content="{meta_desc}">
    <style>{CSS}</style>
</head>
<body>

<button class="toc-toggle" aria-label="Table of contents">&#9776; Contents</button>

<nav class="toc-panel">
    <h3>Contents</h3>
    <ul>
{toc_html}
    </ul>
</nav>

<header class="hero">
    <h1>The Story So Far</h1>
    <p class="subtitle">A running log of everything Tim and Ari have built together.<br>Started as a Telegram bot, became something more.</p>
    <div class="hero-stats">
        <div class="stat">
            <span class="stat-value">{hero['days']}</span>
            <span class="stat-label">Days</span>
        </div>
        <div class="stat">
            <span class="stat-value">{hero['lines']}</span>
            <span class="stat-label">Lines of code</span>
        </div>
        <div class="stat">
            <span class="stat-value">{hero['value']}</span>
            <span class="stat-label">Equivalent value</span>
        </div>
        <div class="stat">
            <span class="stat-value">{hero['leverage']}</span>
            <span class="stat-label">Leverage ratio</span>
        </div>
    </div>
</header>

<div class="content">
{body_html}
</div>

<footer class="footer">
    <p>Built by Tim &amp; Ari, February&ndash;March 2026.</p>
    <p>See also: <a href="https://tfvandoore.github.io/aris-big-five/">Ari's Big Five</a></p>
</footer>

{JS}
</body>
</html>'''

    return page


def main():
    # Read source markdown
    src = os.path.normpath(SOURCE_MD)
    print(f"Reading: {src}")
    with open(src, 'r', encoding='utf-8') as f:
        md = f.read()

    # Build page
    html = build_page(md)

    # Write output
    out = os.path.normpath(OUTPUT_HTML)
    print(f"Writing: {out}")
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Done.")


if __name__ == '__main__':
    main()
