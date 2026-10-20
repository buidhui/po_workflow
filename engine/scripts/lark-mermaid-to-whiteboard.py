#!/usr/bin/env python3
"""Đổi code block mermaid trong một docx Lark thành bảng trắng.

Chạy SAU khi import Markdown lên Lark. Lark không tự dựng ```mermaid — nó ra
code block `Plaintext`, nên phải thay từng cái một.

Dùng:  lark-mermaid-to-whiteboard.py <doc_token> [--dry-run]

Cần `lark-cli` trong PATH và đã `lark-cli auth login --domain docs`.
Nhận diện bằng dòng đầu của code block: flowchart / graph / sequenceDiagram /
classDiagram / erDiagram / gantt / pie / mindmap / journey / gitGraph.
"""
import json, re, subprocess, sys

MERMAID_MO_DAU = re.compile(
    r'^\s*(flowchart|graph|sequenceDiagram|classDiagram|stateDiagram(-v2)?|'
    r'erDiagram|gantt|pie|mindmap|journey|gitGraph|quadrantChart|timeline)\b')


def cli(*args):
    r = subprocess.run(['lark-cli', *args], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(f'lark-cli không trả JSON:\n{r.stdout[:300]}{r.stderr[:300]}')
    if not d.get('ok'):
        sys.exit('lark-cli lỗi: ' + json.dumps(d.get('error', {}), ensure_ascii=False)[:300])
    return d['data']


def go_tag(s):
    """Bỏ thẻ HTML, đổi <br/> thành xuống dòng, giải mã thực thể."""
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    for a, b in (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'),
                 ('&#39;', "'"), ('&amp;', '&')):
        s = s.replace(a, b)
    return s


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    doc = sys.argv[1]
    thu = '--dry-run' in sys.argv

    noi_dung = cli('docs', '+fetch', '--doc', doc,
                   '--detail', 'with-ids', '--as', 'user')['document']['content']

    # <pre id="..." lang="..."><code>…</code></pre>
    khoi = re.findall(r'<pre\s+id="([^"]+)"[^>]*>\s*<code>(.*?)</code>\s*</pre>',
                      noi_dung, re.S)
    can_doi = [(bid, go_tag(code).strip())
               for bid, code in khoi if MERMAID_MO_DAU.match(go_tag(code).strip())]

    print(f'{len(khoi)} code block, {len(can_doi)} cái là mermaid.')
    if not can_doi:
        return

    for i, (bid, code) in enumerate(can_doi, 1):
        dong_dau = code.splitlines()[0][:50]
        if thu:
            print(f'  [thử] {i}. {bid} · {dong_dau}')
            continue
        cli('docs', '+update', '--doc', doc, '--command', 'block_replace',
            '--block-id', bid, '--as', 'user',
            '--content', f'<whiteboard type="mermaid">\n{code}\n</whiteboard>')
        print(f'  ✅ {i}. {dong_dau}')

    if not thu:
        # đọc lại để xác nhận, đừng tin mã 200
        lai = cli('docs', '+fetch', '--doc', doc,
                  '--detail', 'with-ids', '--as', 'user')['document']['content']
        con = len([1 for _, c in re.findall(
            r'<pre\s+id="([^"]+)"[^>]*>\s*<code>(.*?)</code>\s*</pre>', lai, re.S)
            if MERMAID_MO_DAU.match(go_tag(c).strip())])
        bang = len(re.findall(r'<whiteboard[ >]', lai))
        print(f'\nĐối chiếu: {bang} bảng trắng · còn {con} code block mermaid chưa đổi')
        if con:
            sys.exit(1)


if __name__ == '__main__':
    main()
