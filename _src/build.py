"""Builds site/ for LearnSQL.

The .sql files in the topic folders are the source. The build runs every one
of them in SQLite against _src/data/seed.sql, prints what came back, and
stops if a figure the pages claim (EXPECT) drifts or an internal link breaks.
Run: python3 _src/build.py
"""
import html, pathlib, re, sqlite3, sys, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'site'
SEED = (ROOT / '_src/data/seed.sql').read_text(encoding='utf-8')
SITE_URL = 'https://learnsql.shadw.app/'
REPO_URL = 'https://github.com/SolutionsAsService/LearnSQL'

TOPICS = [
    ('basic_operations', 'basic', 'Change the table', 'INSERT, UPDATE and DELETE, run one after another on the same table.'),
    ('aggregate_functions', 'aggregates', 'Squash many rows into one', 'COUNT, SUM, AVG and GROUP BY.'),
    ('joins', 'joins', 'Put two tables side by side', 'INNER, LEFT, RIGHT and FULL OUTER JOIN on the same pair of tables.'),
]
ORDER = {  # reading order inside each topic
    'basic_operations': ['insert_example', 'update_example', 'delete_example'],
    'aggregate_functions': ['count_example', 'sum_example', 'avg_example', 'group_by_example'],
    'joins': ['inner_join_example', 'left_join_example', 'right_join_example', 'full_outer_join_example'],
}
# Every figure the pages print, pinned. The build fails if a run disagrees.
EXPECT = {
    'insert_example': {'rows': 8, 'delta': +1},
    'update_example': {'rows': 8, 'changed': 1},
    'delete_example': {'rows': 5, 'delta': -3},
    'count_example': {'value': 7},
    'sum_example': {'value': 550.75},
    'avg_example': {'value': 25.8571},
    'group_by_example': {'rows': 5},
    'inner_join_example': {'rows': 6},
    'left_join_example': {'rows': 9},
    'right_join_example': {'rows': 7},
    'full_outer_join_example': {'rows': 10},
}
KW = r'\b(SELECT|FROM|WHERE|GROUP BY|INSERT INTO|VALUES|UPDATE|SET|DELETE FROM|FULL OUTER JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN|ON|AS|AND|COUNT|SUM|AVG)\b'


def parse(path):
    text = path.read_text(encoding='utf-8')
    head, _, expl = text.partition('-- Explanation:')
    lines = head.strip().splitlines()
    intro = lines[0].lstrip('- ').strip()
    sql = '\n'.join(l for l in lines[1:]).strip()
    notes = [l.lstrip('- ').strip() for l in expl.strip().splitlines() if l.strip()]
    return intro, sql, notes


def fmt(v):
    if v is None:
        return None
    if isinstance(v, float):
        s = f'{v:.4f}'.rstrip('0').rstrip('.')
        return s if '.' in s or v == int(v) else s
    return str(v)


def table(cols, rows, cls='', marks=None, caption=''):
    """marks: per-row css class (matched / only-left / only-right / changed / new / gone)."""
    h = ''.join(f'<th scope="col">{html.escape(c)}</th>' for c in cols)
    body = []
    for i, r in enumerate(rows):
        m = (marks[i] if marks else '')
        tds = ''.join('<td class="null">NULL</td>' if v is None else f'<td>{html.escape(fmt(v))}</td>' for v in r)
        tag = {'matched': 'both', 'only-left': 'LEFT only', 'only-right': 'RIGHT only',
               'changed': 'changed', 'new': 'new', 'gone': 'removed'}.get(m, '')
        tds += f'<td class="tag">{tag}</td>' if marks else ''
        body.append(f'<tr class="{m}">{tds}</tr>')
    th_extra = '<th scope="col" class="tag"><span class="sr">row</span></th>' if marks else ''
    cap = f'<caption>{html.escape(caption)}</caption>' if caption else ''
    return (f'<div class="tw" tabindex="0" role="region" aria-label="{html.escape(caption or "result")}">'
            f'<table class="{cls}">{cap}<thead><tr>{h}{th_extra}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def code(sql):
    esc = html.escape(sql)
    return '<pre class="sql"><code>' + re.sub(KW, r'<b>\1</b>', esc) + '</code></pre>'


def ticks(s):
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', html.escape(s, quote=False))


def venn(kind, size=120):
    both = '<clipPath id="c-{k}"><circle cx="82" cy="50" r="38"/></clipPath>'.format(k=kind)
    L = kind in ('left', 'full'); R = kind in ('right', 'full')
    parts = [both]
    if L: parts.append('<circle cx="46" cy="50" r="38" class="fl"/>')
    if R: parts.append('<circle cx="82" cy="50" r="38" class="fr"/>')
    parts.append(f'<circle cx="46" cy="50" r="38" clip-path="url(#c-{kind})" class="fb"/>')
    parts.append('<circle cx="46" cy="50" r="38" class="ol"/><circle cx="82" cy="50" r="38" class="ol"/>')
    parts.append('<text x="26" y="54" class="vt">users</text><text x="102" y="54" class="vt">orders</text>')
    label = {'inner': 'only the overlap', 'left': 'all of users', 'right': 'all of orders', 'full': 'everything'}[kind]
    return (f'<svg class="venn" viewBox="0 0 128 100" role="img" aria-label="Venn diagram: {label}">'
            + ''.join(parts) + '</svg>')


def run_all():
    """Execute every example. Returns {stem: result dict} and the seed tables."""
    results, stems = {}, {}
    con = sqlite3.connect(':memory:')
    con.executescript(SEED)
    seed_users = con.execute('SELECT * FROM users ORDER BY user_id').fetchall()
    seed_orders = con.execute('SELECT * FROM orders ORDER BY order_id').fetchall()
    for folder, _, _, _ in TOPICS:
        for stem in ORDER[folder]:
            cand = [p for p in (ROOT / folder).glob('*.sql') if p.stem.replace('-', '_') == stem]
            assert cand, f'missing {folder}/{stem}'
            stems[stem] = cand[0]
    for stem, path in stems.items():
        intro, sql, notes = parse(path)
        r = dict(stem=stem, path=path.relative_to(ROOT).as_posix(), intro=intro, sql=sql, notes=notes)
        head = sql.split()[0].upper()
        if head in ('INSERT', 'UPDATE', 'DELETE'):
            before = con.execute('SELECT * FROM users ORDER BY user_id').fetchall()
            con.execute(sql)
            after = con.execute('SELECT * FROM users ORDER BY user_id').fetchall()
            r.update(kind='dml', before=before, after=after)
        else:
            # a fresh copy of the pristine data for every read-only query
            fresh = sqlite3.connect(':memory:'); fresh.executescript(SEED)
            cur = fresh.execute(sql)
            r.update(kind='select', cols=[d[0] for d in cur.description], rows=cur.fetchall())
        results[stem] = r
    return results, seed_users, seed_orders


def check(results):
    for stem, exp in EXPECT.items():
        r = results[stem]
        if r['kind'] == 'dml':
            n = len(r['after']); d = n - len(r['before'])
            changed = sum(1 for a in r['after'] if a not in r['before'] and a[0] in {b[0] for b in r['before']})
            got = {'rows': n, 'delta': d, 'changed': changed}
            for k, v in exp.items():
                assert got[k] == v, f'{stem}: {k} is {got[k]}, page says {v}'
        else:
            for k, v in exp.items():
                got = len(r['rows']) if k == 'rows' else r['rows'][0][0]
                if isinstance(v, float): got = round(got, 4)
                assert got == v, f'{stem}: {k} is {got}, page says {v}'


def dml_view(r):
    b, a = r['before'], r['after']
    bid = {x[0]: x for x in b}; aid = {x[0]: x for x in a}
    cols = ['user_id', 'first_name', 'last_name', 'age']
    brow = [x for x in b]; bm = ['gone' if x[0] not in aid else ('changed' if aid[x[0]] != x else '') for x in b]
    arow = [x for x in a]; am = ['new' if x[0] not in bid else ('changed' if bid[x[0]] != x else '') for x in a]
    return (table(cols, brow, 'ba', bm, f'users before ({len(b)} rows)'),
            table(cols, arow, 'ba', am, f'users after ({len(a)} rows)'))


def figure(r):
    """The one number that stands for an example: on the poster and on its page."""
    s = r['stem']
    if r['kind'] == 'dml':
        d = len(r['after']) - len(r['before'])
        if s == 'update_example': return ('1', 'row changed: age 30 → 31')
        return (f'{d:+d}'.replace('-', '−'), 'rows' if abs(d) != 1 else 'row')
    if s == 'group_by_example': return (str(len(r['rows'])), 'groups')
    if s.endswith('join_example'): return (str(len(r['rows'])), 'rows')
    return (fmt(r['rows'][0][0]), r['cols'][0].replace('_', ' '))


def example_section(r, ix):
    title = r['stem'].replace('_example', '').replace('_', ' ').upper()
    fig, unit = figure(r)
    notes = ''.join(f'<li>{ticks(n)}</li>' for n in r['notes'])
    out = [f'<section class="ex" id="{r["stem"]}"><header><h2>{html.escape(title)}</h2>'
           f'<p class="fig"><b>{html.escape(fig)}</b> <span>{html.escape(unit)}</span></p></header>',
           f'<p class="intro">{html.escape(r["intro"])}</p>', code(r['sql']),
           f'<p class="src">Source: <a href="{REPO_URL}/blob/main/{r["path"]}">{r["path"]}</a></p>']
    if r['kind'] == 'dml':
        b, a = dml_view(r)
        out.append(f'<div class="ba2"><div><h3>Before</h3>{b}</div><div><h3>After</h3>{a}</div></div>')
    else:
        marks = None
        if r['stem'].endswith('join_example'):
            marks = []
            for row in r['rows']:
                marks.append('only-left' if row[2] is None else ('only-right' if row[0] is None else 'matched'))
            kind = r['stem'].split('_join')[0].replace('full_outer', 'full')
            out.insert(2, venn(kind))
        out.append(f'<h3>Result: {len(r["rows"])} row{"" if len(r["rows"]) == 1 else "s"}</h3>'
                   + table(r['cols'], r['rows'], 'res', marks, 'result'))
    out.append(f'<h3>Reading it</h3><ul class="notes">{notes}</ul></section>')
    return ''.join(out)


NAV = [('index.html', 'Home')] + [(f'{slug}.html', label) for _, slug, label, _ in TOPICS] + [('about.html', 'About')]
NAV_SHORT = {'index.html': 'Home', 'basic.html': 'Change', 'aggregates.html': 'Squash', 'joins.html': 'Join', 'about.html': 'About'}


def page(name, title, desc, body, extra=''):
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if h == name else ""}>{NAV_SHORT[h]}</a>' for h, _ in NAV)
    canon = SITE_URL + ('' if name == 'index.html' else name.replace('.html', ''))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}"><link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website"><meta property="og:url" content="{canon}">
<link rel="stylesheet" href="style.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><a class="brand" href="index.html">Learn<b>SQL</b></a><nav aria-label="Pages">{nav}</nav></header>
<main id="main">{body}</main>
<footer><p>Every result on this site was produced by running the query in SQLite {sqlite3.sqlite_version}, on invented data. Source on <a href="{REPO_URL}">GitHub</a>. By SolutionsAsService.</p></footer>
</body></html>'''


def index(results, users, orders):
    tiles = []
    for folder, slug, label, _ in TOPICS:
        for stem in ORDER[folder]:
            r = results[stem]; fig, unit = figure(r)
            nm = stem.replace('_example', '').replace('_', ' ').upper()
            tiles.append(f'<a class="tile t-{slug}{" long" if len(fig) > 4 else ""}" href="{slug}.html#{stem}"><span class="nm">{nm}</span>'
                         f'<span class="big">{html.escape(fig)}</span><span class="un">{html.escape(unit)}</span></a>')
    tiles.append('<a class="tile t-about" href="about.html"><span class="nm">HOW</span><span class="big">?</span><span class="un">How these numbers were made</span></a>')
    topics = ''.join(f'<li><a href="{s}.html"><b>{l}</b><span>{d}</span></a></li>' for _, s, l, d in TOPICS)
    body = f'''<section class="hero"><h1>Eleven queries.<br>Every one <em>run</em>.</h1>
<p class="lede">Learn SQL from queries that were executed, not described. Each tile is the number its query returned on a
{len(users)}-row users table and a {len(orders)}-row orders table. Click one to see the query and the rows.</p></section>
<section aria-label="All eleven queries" class="poster">{"".join(tiles)}</section>
<section class="start"><h2>Three lessons, in order</h2><ol class="topics">{topics}</ol></section>'''
    return page('index.html', 'LearnSQL: eleven queries, every one run',
                'Learn SQL by reading queries that were actually executed: INSERT, UPDATE, DELETE, aggregates and joins, with the real result rows.', body)


def tables_block(users, orders):
    return ('<div class="ba2"><div><h3>users</h3>' + table(['user_id', 'first_name', 'last_name', 'age'], users, '', None, 'users table') +
            '</div><div><h3>orders</h3>' + table(['order_id', 'user_id', 'order_amount'], orders, '', None, 'orders table') + '</div></div>')


def topic_page(folder, slug, label, blurb, results, users, orders):
    secs = ''.join(example_section(results[s], i) for i, s in enumerate(ORDER[folder]))
    intro = {
        'basic': '<p>These three change the table, so they run in order on one copy of <code>users</code>: the insert adds John, the update ages him a year, the delete removes everyone under twenty. Rows are marked <b>new</b>, <b>changed</b> or <b>removed</b>.</p>',
        'aggregates': '<p>Each query below reads the original, unchanged tables. An aggregate function collapses many rows into one value; <code>GROUP BY</code> gives you one value per group.</p>',
        'joins': '<p>Same two tables, four joins. <b>both</b> rows matched on <code>user_id</code>. <b>LEFT only</b> rows are users with no order. <b>RIGHT only</b> is order 107, whose user_id 99 matches nobody. <code>NULL</code> fills the side that has no match.</p>',
    }[slug]
    start = tables_block(users, orders) if slug != 'basic' else ''
    body = f'<h1>{label}</h1><p class="lede">{blurb}</p>{intro}<details class="data"{" open" if slug=="joins" else ""}><summary>The two tables these run on</summary>{tables_block(users, orders)}</details>{secs}'
    idx = [t[1] for t in TOPICS].index(slug)
    nxt = TOPICS[idx + 1] if idx + 1 < len(TOPICS) else None
    if nxt: body += f'<p class="next"><a href="{nxt[1]}.html">Next: {nxt[2]} →</a></p>'
    return page(f'{slug}.html', f'{label}: LearnSQL', blurb + ' Every result is the real output of the query.', body)


def about(results):
    body = f'''<h1>About</h1>
<p class="lede">A small, honest SQL primer. The only claims it makes are ones the build checks.</p>
<h2>How the numbers get here</h2>
<p><code>python3 _src/build.py</code> reads the eleven <code>.sql</code> files in the repository folders, runs each in SQLite against <a href="{REPO_URL}/blob/main/_src/data/seed.sql">_src/data/seed.sql</a>, and writes every table and figure on this site from what came back. The build stops if a printed figure changes or a link breaks.</p>
<h2>What is not covered</h2>
<p>SQLite is not every database. <code>RIGHT JOIN</code> and <code>FULL OUTER JOIN</code> need SQLite 3.39 or newer, and MySQL has no <code>FULL OUTER JOIN</code>. The data is invented: nobody in it is real.</p>
<h2>Contribute</h2><p>Add a <code>.sql</code> file with a leading comment and an <code>-- Explanation:</code> block, list it in <code>_src/build.py</code>, and rebuild. See <a href="{REPO_URL}/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a>.</p>'''
    return page('about.html', 'About: LearnSQL', 'How the LearnSQL numbers are produced and what the site does not cover.', body)


def main():
    results, users, orders = run_all()
    check(results)
    if OUT.exists():
        for p in OUT.iterdir():
            if p.name not in ('style.css',): p.unlink() if p.is_file() else shutil.rmtree(p)
    OUT.mkdir(exist_ok=True)
    shutil.copy(ROOT / '_src/style.css', OUT / 'style.css')
    pages = {'index.html': index(results, users, orders), 'about.html': about(results)}
    for folder, slug, label, blurb in TOPICS:
        pages[f'{slug}.html'] = topic_page(folder, slug, label, blurb, results, users, orders)
    for n, h in pages.items(): (OUT / n).write_text(h, encoding='utf-8')
    (OUT / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#111"/>'
        '<circle cx="13" cy="16" r="8" fill="#f2c230"/><circle cx="19" cy="16" r="8" fill="#1f3fbf" fill-opacity=".85"/></svg>')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n')
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + ''.join(f'<url><loc>{SITE_URL}{"" if n=="index.html" else n[:-5]}</loc></url>' for n in pages) + '</urlset>')
    # links: every href inside the site must land on a file and, if it has one, an id that exists
    bad = []
    for n, h in pages.items():
        for href in re.findall(r'href="([^"#]*)(#[^"]*)?"', h):
            f, frag = href
            if f.startswith(('http', 'mailto')) or not f: 
                if f == '' : continue
                continue
            if not (OUT / f).exists(): bad.append((n, f))
            elif frag and f'id="{frag[1:]}"' not in (OUT / f).read_text(encoding='utf-8'): bad.append((n, f + frag))
    for n, h in pages.items():
        for frag in re.findall(r'href="#([^"]+)"', h):
            if f'id="{frag}"' not in h: bad.append((n, '#' + frag))
    if bad: sys.exit(f'broken links: {bad}')
    print('built', len(pages), 'pages;', len(results), 'queries run; all figures match EXPECT')


if __name__ == '__main__':
    main()
