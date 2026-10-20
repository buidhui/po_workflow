#!/usr/bin/env python3
"""Chèn ảnh design vào mục `Design` của một docx Lark.

Chạy SAU khi publish lại tài liệu. Ảnh là file nhị phân nên **không nằm được
trong file `.md`** — mỗi lần import tạo doc mới là mất hết, phải chèn lại.

Dùng:  lark-insert-design-images.py <doc_token> <thư mục ảnh> [--dry-run]

Thứ tự ảnh lấy theo file `order.txt` trong chính thư mục đó: mỗi dòng là
`<tên file>|<chú thích>`. Thiếu file đó thì xếp theo tên.

Cần `lark-cli` trong PATH, đã đăng nhập, và tài liệu phải có heading `Design`.
"""
import json, re, subprocess, sys
from pathlib import Path


def cli(*args):
    r = subprocess.run(['lark-cli', *args], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(f'lark-cli không trả JSON:\n{r.stdout[:300]}{r.stderr[:300]}')
    if not d.get('ok'):
        sys.exit('lark-cli lỗi: ' + json.dumps(d.get('error', {}), ensure_ascii=False)[:300])
    return d['data']


def doc_cuoi_muc(doc, ten_muc='Design'):
    """block_id của block cuối cùng trong một mục heading 1."""
    c = cli('docs', '+fetch', '--doc', doc, '--scope', 'outline',
            '--max-depth', '1', '--as', 'user')['document']['content']
    m = re.search(r'<h1 id="([^"]+)">' + re.escape(ten_muc) + r'</h1>', c)
    if not m:
        sys.exit(f'Không tìm thấy heading "{ten_muc}" trong tài liệu.')
    sec = cli('docs', '+fetch', '--doc', doc, '--scope', 'section',
              '--start-block-id', m.group(1), '--detail', 'with-ids',
              '--as', 'user')['document']['content']
    ids = re.findall(r'<\w+\s+id="([^"]+)"', sec)
    if not ids:
        sys.exit(f'Mục "{ten_muc}" rỗng.')
    return ids[-1]


def danh_sach(thu_muc: Path):
    f = thu_muc / 'order.txt'
    if f.exists():
        ra = []
        for d in f.read_text(encoding='utf-8').splitlines():
            d = d.strip()
            if not d or d.startswith('#'):
                continue
            ten, _, chu = d.partition('|')
            ra.append((thu_muc / ten.strip(), chu.strip()))
        return ra
    return [(p, p.stem) for p in sorted(thu_muc.glob('*.png'))]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    doc, thu_muc = sys.argv[1], Path(sys.argv[2])
    thu = '--dry-run' in sys.argv

    anh = danh_sach(thu_muc)
    thieu = [p for p, _ in anh if not p.exists()]
    if thieu:
        sys.exit('Không có file: ' + ', '.join(str(x) for x in thieu))

    neo = doc_cuoi_muc(doc)
    print(f'{len(anh)} ảnh · chèn sau block {neo}\n')

    blocks = []
    for p, chu in anh:
        if thu:
            print(f'  [thử] {p.name} · {chu[:60]}')
            continue
        d = cli('docs', '+media-insert', '--doc', doc, '--file', str(p),
                '--type', 'image', '--caption', chu, '--align', 'center',
                '--as', 'user')
        blocks.append(d['block_id'])
        print(f'  ✅ {p.name}')

    if thu or not blocks:
        return

    # media-insert luôn ghi vào cuối tài liệu, nên phải kéo cả cụm về đúng mục
    cli('docs', '+update', '--doc', doc, '--command', 'block_move_after',
        '--block-id', neo, '--src-block-ids', ','.join(blocks), '--as', 'user')

    c = cli('docs', '+fetch', '--doc', doc, '--detail', 'with-ids',
            '--as', 'user')['document']['content']
    i_d, i_s = c.find('>Design<'), c.find('>Solution<')
    vi_tri = [m.start() for m in re.finditer(r'<img[ >]', c)]
    trong = sum(1 for v in vi_tri if i_d < v < i_s)
    print(f'\nĐối chiếu: {len(vi_tri)} ảnh trong tài liệu, {trong} nằm đúng mục Design')
    if trong != len(anh):
        sys.exit(1)


if __name__ == '__main__':
    main()
