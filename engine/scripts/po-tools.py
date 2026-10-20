#!/usr/bin/env python3
"""Công cụ dòng lệnh của PO-Workflow (theo AWS AI-DLC). Chỉ dùng thư viện chuẩn, chạy được với Python 3.9.

<intent> là đường dẫn thư mục intent, hoặc chỉ tên thư mục trong intents/.
Danh sách stage, thư mục, template và checklist đọc từ bảng metadata của engine/stages/*.md;
thứ tự và mã stage đọc từ engine/protocol/profiles.md. Quy ước mã ở engine/standards/id-conventions.md,
quy tắc bàn giao liên team ở engine/standards/handoff-rules.md.

Theo dõi và kiểm:
  po-tools.py status  [intents-root]
      Bảng trạng thái mọi intent và mười kiểm tra lệch giữa state.md và đĩa, gồm mã tính năng
      trùng giữa hai intent, cộng độ tươi của nguồn sống trong domain.md mục 2.
      Mặc định intents-root là <repo>/intents.
  po-tools.py next    <intent>
      Stage cần làm tiếp, dòng tiến độ, số câu hỏi còn trống và số câu chặn còn trống.
  po-tools.py check   <intent> <stage-slug> [--strict]
      Kiểm máy artifact của stage: heading bắt buộc, thẻ nguồn, [Qn] và [DECn] có thật,
      chữ mẫu còn sót, thẻ US đủ chín mục, mục cấm trong PRD; ở 2.43 thêm giới hạn từ và chữ ký của
      Decision Brief, độ phủ của ba file thiết kế so với PRD,
      cột ưu tiên của FR. Với PRD còn kiểm: mã AC trùng, BR chưa có AC trỏ tới, frontmatter
      thiếu feature; AC không có chữ "Khi" chỉ là gợi ý. Mã thoát 0; --strict trả 1 khi có cảnh báo.
  po-tools.py trace   <intent> [--write]
      Truy vết FR, US, BR, AC từ requirements.md, stories.md và prd.md: mỗi BR có AC cùng US trỏ tới,
      mã AC không trùng, AC thuộc US có trong PRD. Mã thoát 0 là đạt, 1 là có GAP hoặc ORPHAN,
      2 là không đọc được. --write ghi inception/prd/traceability.md và
      verification/phase-check-inception.md.
  po-tools.py dor     <intent> [--story US-<feature>-<NN>]
      Điều kiện giao Dev của từng US trong prd.md: PRD đã duyệt, US có AC, mọi BR có AC trỏ tới, không còn
      ❓PO, không còn câu chặn trong Open Issues. Mã thoát 0 khi mọi story đạt, 1 khi có story chưa đạt,
      2 khi chưa có PRD hoặc mã tính năng.
  po-tools.py replay  <intent>
      In bản bàn giao intent cho PO khác: tóm tắt, dòng thời gian, quyết định, CR, review,
      số story theo trạng thái, câu chặn còn mở, nơi đăng bản đọc nếu có. Không ghi gì.

Ghi chép:
  po-tools.py feature-id [--next] [--assign <intent>] [--dry-run]
      Mã tính năng <code>-F<NNN>, code lấy từ frontmatter domain/domain.md. --next (mặc định) in mã
      kế tiếp: số lớn nhất trong feature của intents/*/intent.md cùng code, cộng một. --assign ghi
      feature vào frontmatter intent.md, ngay sau khoá intent, rồi in mã; intent đã có mã thì từ chối.
      --dry-run chỉ in.
  po-tools.py stories <intent> [--write] [--us US3]
      Lập Story List cho Jira từ các khối ## US<n> của prd.md: mỗi US một dòng, 12 cột theo mẫu import
      CSV của Jira (Project key, Project name, Project type, Issue Type, Summary, Description, Epic Link,
      3 cột Labels, Comment). Project lấy từ jira_project_key, jira_project_name ở frontmatter domain.md;
      Epic từ dòng Jira Epic của intent.md, ghi "U2: KEY" để gán Epic theo Unit. Description theo cú pháp
      Jira, mã đầy đủ. Labels: mã tính năng, mã story, Unit. So với bản CSV trước thì in story đổi và mới.
      --write ghi intents/<intent>/stories/story-list-prd-v<version>.csv, chỉ khi PRD đã duyệt.
  po-tools.py review-start <intent> <stage-slug>
      Trước khi gọi AI Reviewer: ghi dấu artifact vào reviews/review-<slug>-NN.digest. approve so dấu này để biết
      review còn ứng với bản hiện tại không.
  po-tools.py approve <intent> <stage-slug> --words "<lời PO>" [--who <tên>] [--version X.Y] [--dry-run]
                      [--accept-warnings "<lời PO>"] [--accept-review-gap "<lời PO>"]
      Ghi một lần duyệt: version, status, approved_at ở frontmatter; chụp archive; thêm DEC;
      cập nhật state.md; in dòng tiến độ. Chỉ chạy khi stage đang [?], và khi:
      - lời PO có nguyên văn trong sổ lượt người .po/turns.jsonl, ghi sau lần sửa artifact cuối;
        PO tự gõ lệnh trong terminal thì không cần sổ;
      - kiểm máy không còn cảnh báo, hoặc PO chấp nhận bằng --accept-warnings;
      - stage bật AI Reviewer thì lần review mới nhất ứng với đúng bản hiện tại, hoặc PO chấp nhận
        bằng --accept-review-gap. Lời chấp nhận cũng phải có trong sổ và được ghi vào DEC.
      --dry-run kiểm như thật, chỉ in, không ghi.
  po-tools.py archive <intent> <stage-slug> <artifact> [--label <nhãn>]
      Chép artifact vào archive/<slug>/<tên>-v<version>-<YYYYMMDD>.md, hoặc
      <tên>-<nhãn>-<YYYYMMDD>.md khi có --label. Từ chối ghi đè.
  po-tools.py index   [--write]
      Bảng spec cho Dev, mỗi intent có PRD một dòng, có mã tính năng, số story và số story
      đạt điều kiện giao Dev. --write ghi intents/INDEX.md.

Engine:
  po-tools.py doctor
      Kiểm môi trường và repo, gồm mã tính năng trùng và intent có PRD chưa có mã.
      Mã thoát 1 khi có Lỗi.
  po-tools.py manifest [--write]
      sha256 của mọi file engine. --write ghi engine/MANIFEST.txt.
  po-tools.py engine-check [--strict]
      So file engine hiện tại với engine/MANIFEST.txt. Mã thoát 1 khi có file bị sửa hoặc mất;
      --strict coi cả file mới chưa ghi vào manifest là lỗi, dùng trong CI.
  po-tools.py selftest
      Chạy các ca trong engine/tests/fixtures/*/expected.txt, mỗi fixture trên một gốc dữ liệu tạm gồm
      domain mẫu ở engine/tests/root và ngày cố định. Kiểm thêm: cấu trúc file stage, mọi lệnh đều có ca
      (trừ UNTESTED), tài liệu chỉ nhắc lệnh và đường dẫn có thật, VERSION khớp CHANGELOG và MANIFEST.
  po-tools.py migrate <intent-dir> [--feature <mã>] [--words "<lời PO>"] [--write]
      Chuyển dữ liệu intent cũ lên engine hiện tại: đường dẫn, Unit, PIC, AI Reviewer, mã tính năng,
      file câu hỏi luồng v1 sang dạng ## Q<n>, chụp lại bản duyệt kèm DEC. Không đụng archive, reviews.
"""
import datetime
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parents[2]
# Gốc dữ liệu: domain/, intents/, memory/, .po/. Mặc định là repo; selftest đặt PO_TOOLS_ROOT sang thư mục tạm
# để mỗi fixture chạy trên domain riêng, không phụ thuộc domain đang cài.
ROOT = Path(os.environ["PO_TOOLS_ROOT"]).resolve() if os.environ.get("PO_TOOLS_ROOT") else REPO
DATA_DIRS = ("domain/", "intents/", "memory/", ".po/")
INTENTS = ROOT / "intents"
STAGES_DIR = REPO / "engine" / "stages"
PROFILES_MD = REPO / "engine" / "protocol" / "profiles.md"
DOMAIN_MD = ROOT / "domain" / "domain.md"
TURNS = ROOT / ".po" / "turns.jsonl"
TESTS = REPO / "engine" / "tests"
FIXTURES = TESTS / "fixtures"
TEST_ROOT = TESTS / "root"
TEST_TODAY = "2026-10-20"
MANIFEST = REPO / "engine" / "MANIFEST.txt"



def data_path(t):
    """Đường dẫn trong file engine: domain/, intents/, memory/ tính từ gốc dữ liệu, còn lại tính từ repo."""
    return (ROOT if str(t).startswith(DATA_DIRS) else REPO) / t


def show(p):
    """Đường dẫn để in: tương đối với gốc dữ liệu nếu nằm trong đó, không thì với repo."""
    p = Path(p)
    for base in (ROOT, REPO):
        try:
            return p.resolve().relative_to(base.resolve()).as_posix()
        except ValueError:
            continue
    return str(p)


def today():
    """Ngày hiện tại; PO_TOOLS_TODAY=YYYY-MM-DD cố định ngày khi kiểm thử."""
    v = os.environ.get("PO_TOOLS_TODAY", "")
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", v.strip())
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else datetime.date.today()


def now():
    if os.environ.get("PO_TOOLS_TODAY"):
        return datetime.datetime.combine(today(), datetime.time(9, 0))
    return datetime.datetime.now()


# Dự phòng, chỉ dùng khi không đọc được engine/stages/*.md.
# (mã, slug, tên, phase, thư mục, artifact chính, file câu hỏi)
FALLBACK_STAGES = [
    ("1.1", "intent-capture", "Intent Capture & Framing", "ideation", "ideation/intent-capture", "intent-statement.md", "intent-capture-questions.md"),
    ("1.2", "market-research", "Market Research", "ideation", "ideation/market-research", "competitive-analysis.md", "market-research-questions.md"),
    ("1.4", "scope-definition", "Scope Definition", "ideation", "ideation/scope-definition", "scope-document.md", "scope-definition-questions.md"),
    ("1.7", "approval-handoff", "Approval & Handoff", "ideation", "ideation/approval-handoff", "initiative-brief.md", "approval-handoff-questions.md"),
    ("2.3", "requirements-analysis", "Requirements Analysis", "inception", "inception/requirements-analysis", "requirements.md", "requirements-analysis-questions.md"),
    ("2.31", "impact-analysis", "Impact Analysis", "inception", "inception/impact-analysis", "impact-matrix.md", "impact-analysis-questions.md"),
    ("2.32", "solution-options", "Solution Options", "inception", "inception/solution-options", "solution-options.md", "solution-options-questions.md"),
    ("2.4", "user-stories", "User Stories", "inception", "inception/user-stories", "stories.md", "user-stories-questions.md"),
    ("2.42", "prd-generation", "PRD Generation", "inception", "inception/prd", "prd.md", "field-intake-questions.md"),
    ("2.43", "design-alignment", "Design Alignment", "inception", "inception/decision-brief", "decision-brief.md", "design-alignment-questions.md"),
]

INTERNAL = ("intent-statement", "scope-document", "requirements", "impact-matrix", "solution-options",
            "stories", "competitive-analysis", "related-features-map")
HANDOFF = ("initiative-brief", "decision-brief", "prd")
US_CARD_LABELS = ("Vai và mục tiêu", "Bối cảnh", "Luồng chính", "Nhánh đáng kể", "Rule đã biết",
                  "Dữ liệu và vùng chạm", "Ngoài phạm vi", "Phụ thuộc", "Chưa rõ")
BRIEF_AI_SECTIONS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
BRIEF_WORD_LIMIT = 1500
# Ba file thiết kế các team viết ở 2.43, từ PRD đã duyệt: (tên, đường dẫn trong intent, người viết)
TEAM_DESIGNS = (("ux-design", "inception/ux-design/ux-design.md", "Design PIC"),
                ("tech-design", "inception/tech-design/tech-design.md", "Tech PIC"),
                ("test-design", "inception/test-design/test-design.md", "QA PIC"))
SIGNERS = ("Design PIC", "Tech PIC", "QA PIC")
SIGNED = ("đồng ý", "có ý kiến")
STALE_DAYS = 30

FR_RE = re.compile(r"\bN?FR\d+(?:\.\d+)?\b")
ID_FR = re.compile(r"N?FR\d+(?:\.\d+)?")
ID_US = re.compile(r"US\d+")
BR_RE = re.compile(r"\bBR-?(\d+)\.(\d+)([a-z]?)\b")
STAGE_LINE = re.compile(r"^- \[(.)\] (\S+) (\S+)(.*)$")
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
SEP_CELL = re.compile(r"^\s*:?-{2,}:?\s*$")
TAG_RE = re.compile(r"\[(desc|Q\d+|\d+\.\d+\s+Q\d+|\d+\.\d+|KB-[^\]\n]+|DEC\d+|assumption|suy ra|scope|N?FR\d+(?:\.\d+)?)\]", re.I)
PLACEHOLDER_RE = re.compile(r"<([^\s<>][^<>\n]{1,79})>")
HTML_TAGS = {"a", "abbr", "b", "blockquote", "br", "center", "code", "del", "details", "div", "em", "figcaption",
             "figure", "font", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "iframe", "img", "ins", "kbd", "li",
             "mark", "ol", "p", "picture", "pre", "s", "small", "source", "span", "strong", "sub", "summary", "sup",
             "table", "tbody", "td", "th", "thead", "tr", "u", "ul", "video"}
EMPTY = ("", "-", "—", "–", "none")
NONE_VALUES = ("không có", "không", "none", "chưa có", "-", "—", "n/a", "không áp dụng")
WORD_STATE = {"-": "đang làm", "?": "chờ duyệt", "R": "đang sửa", " ": "chưa bắt đầu", "x": "đã duyệt", "S": "bỏ qua"}


# ================================================================ tiện ích chung
def read(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError, IsADirectoryError, UnicodeDecodeError, PermissionError):
        return None


def write(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")


def rel(p, base):
    try:
        return Path(p).resolve().relative_to(Path(base).resolve()).as_posix()
    except ValueError:
        return str(p)


def clean(s):
    s = (s or "").replace("\\|", "|")
    s = re.sub(r"[`*~]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def snippet(text, n=70):
    t = clean(text)
    return '"%s"' % (t[:n] + ("..." if len(t) > n else ""))


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def fm_bounds(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return (0, i)
    return None


def body_start(lines):
    b = fm_bounds(lines)
    return b[1] + 1 if b else 0


def frontmatter(text):
    fm = {}
    if not text:
        return fm
    lines = text.splitlines()
    b = fm_bounds(lines)
    if not b:
        return fm
    for ln in lines[1:b[1]]:
        if ":" in ln:
            k, v = ln.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def set_frontmatter(text, updates):
    """Đặt các khoá ở frontmatter, giữ khoá khác và thứ tự; thêm khoá thiếu vào cuối."""
    lines = text.splitlines()
    b = fm_bounds(lines)
    if not b:
        lines = ["---"] + ["%s: %s" % kv for kv in updates] + ["---"] + lines
    else:
        done = set()
        for i in range(1, b[1]):
            if ":" not in lines[i]:
                continue
            k = lines[i].split(":", 1)[0].strip()
            for uk, uv in updates:
                if k == uk and uk not in done:
                    lines[i] = "%s: %s" % (uk, uv)
                    done.add(uk)
        add = ["%s: %s" % (k, v) for k, v in updates if k not in done]
        lines = lines[:b[1]] + add + lines[b[1]:]
    return "\n".join(lines) + "\n"


def norm_body(text):
    lines = (text or "").splitlines()
    return "\n".join(ln.rstrip() for ln in lines[body_start(lines):]).strip()


def ver_tuple(v):
    v = (v or "").strip().lstrip("vV")
    m = re.match(r"(\d+(?:\.\d+)*)", v)
    return tuple(int(x) for x in m.group(1).split(".")) if m else None


def fmt_ver(t):
    return ".".join(str(x) for x in t)


def code_key(code):
    a, _, b = (code or "").partition(".")
    try:
        return (int(a), b)
    except ValueError:
        return (999, code)


def parse_date(txt):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", txt or "")
    try:
        if m:
            return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", txt or "")
        if m:
            return datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None
    return None


def git(*args):
    try:
        r = subprocess.run(["git", "-c", "core.quotepath=false"] + list(args), cwd=str(REPO),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return r.returncode, r.stdout.decode("utf-8", "replace")
    except OSError:
        return 127, ""


def git_user():
    rc, out = git("config", "--get", "user.name")
    return out.strip() if rc == 0 else ""


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(esc(str(c)) for c in r) + " |")
    return "\n".join(out)


def parse_opts(args, flags=(), opts=()):
    pos, kv = [], {}
    i = 0
    while i < len(args):
        a = args[i]
        if "=" in a and a.split("=", 1)[0] in opts:
            k, v = a.split("=", 1)
            kv[k] = v
        elif a in opts:
            if i + 1 >= len(args):
                raise ValueError("thiếu giá trị sau %s" % a)
            kv[a] = args[i + 1]
            i += 1
        elif a in flags:
            kv[a] = True
        else:
            pos.append(a)
        i += 1
    return pos, kv


# ================================================================ bảng và heading
def split_cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def is_sep_row(cells):
    return bool(cells) and any(SEP_CELL.match(c) for c in cells) and all(SEP_CELL.match(c) or c == "" for c in cells)


def table_rows(text):
    rows = []
    for ln in (text or "").splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = split_cells(s)
        if all(SEP_CELL.match(c) or c == "" for c in cells):
            continue
        rows.append(cells)
    return rows


def parse_tables(lines, start=0, end=None):
    end = len(lines) if end is None else min(end, len(lines))
    out, i, fence = [], start, False
    while i < end:
        s = lines[i].strip()
        if s.startswith("```") or s.startswith("~~~"):
            fence = not fence
            i += 1
            continue
        if fence or not s.startswith("|"):
            i += 1
            continue
        j = i
        while j < end and lines[j].strip().startswith("|"):
            j += 1
        group = [(k, split_cells(lines[k])) for k in range(i, j)]
        if len(group) >= 2 and is_sep_row(group[1][1]):
            header, hline, data = group[0][1], group[0][0], group[2:]
        else:
            header, hline, data = [], None, group
        rows = [(c, k) for k, c in data if not is_sep_row(c)]
        out.append({"header": header, "hline": hline, "rows": rows, "start": i, "end": j})
        i = j
    return out


def col(header, *keys):
    for idx, h in enumerate(header):
        hl = clean(h).lower()
        if any(k.lower() in hl for k in keys):
            return idx
    return None


def cell(cells, idx):
    return cells[idx].strip() if idx is not None and 0 <= idx < len(cells) else ""


def headings(lines, start=0):
    out, fence = [], False
    for i in range(start, len(lines)):
        st = lines[i].strip()
        if st.startswith("```") or st.startswith("~~~"):
            fence = not fence
            continue
        if fence:
            continue
        m = HEAD_RE.match(lines[i])
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip()))
    return out


def section_lines(lines, pred, start=0):
    """(đầu, cuối) của mục đầu tiên có heading thoả pred, tới heading cùng cấp hoặc cao hơn."""
    hs = headings(lines, start)
    for k, (i, lvl, txt) in enumerate(hs):
        if pred(clean(txt)):
            end = len(lines)
            for (j, l2, _) in hs[k + 1:]:
                if l2 <= lvl:
                    end = j
                    break
            return (i, end)
    return None


def section(text, heading):
    """Phần văn bản dưới heading (khớp đầu dòng, không phân biệt cấp) tới heading kế."""
    if text is None:
        return ""
    m = re.search(r"^#+\s*" + re.escape(heading) + r"\b.*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^#+\s", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def first_id(text, rx):
    n = clean(text)
    if not n:
        return None
    tok = n.split()[0].strip(":,;()[]").rstrip(".")
    return tok if rx.fullmatch(tok) else None


def backticks(s):
    return [t.strip() for t in re.findall(r"`([^`]+)`", s or "")]


def strip_inline_code(s):
    return re.sub(r"`[^`]*`", "", s)


# ================================================================ danh sách stage
class Stage(object):
    def __init__(self):
        self.code = ""
        self.name = ""
        self.slug = ""
        self.phase = ""
        self.dir = ""
        self.artifacts = []
        self.main = ""
        self.questions = ""
        self.templates = []
        self.checklist = []
        self.knowledge = []
        self.reviewer = ""
        self.profiles = ""
        self.aws_diff = None
        self.has_dir_row = False
        self.file = None
        self.meta = {}
        self.problems = []


class StageSet(object):
    def __init__(self, items, warnings, notes, reviewers, source):
        self.list = items
        self.by_slug = dict((s.slug, s) for s in items)
        self.by_code = dict((s.code, s) for s in items)
        self.warnings = warnings
        self.notes = notes
        self.reviewers = reviewers
        self.source = source

    def artifact_map(self):
        m = {}
        for s in self.list:
            for a in s.artifacts:
                m.setdefault(Path(a).stem, (s, "%s/%s" % (s.dir, a)))
        return m

    def name(self, slug):
        s = self.by_slug.get(slug)
        return s.name if s else slug


def parse_stage_file(path):
    text = read(path) or ""
    lines = text.splitlines()
    st = Stage()
    st.file = path
    h1 = next((l for l in lines if l.startswith("# ")), "")
    m = re.match(r"#\s+(\d+(?:\.\d+)?)\s+(.+)$", h1)
    if m:
        st.code, st.name = m.group(1), m.group(2).strip()
    stop = next((i for i, l in enumerate(lines) if l.startswith("## ")), len(lines))
    meta = {}
    for t in parse_tables(lines, 0, stop)[:1]:
        for cells, _ in [(t["header"], None)] + t["rows"]:
            if len(cells) >= 2 and clean(cells[0]):
                meta[clean(cells[0])] = cells[1].strip()
    st.meta = meta
    if not meta:
        st.problems.append("không có bảng metadata ngay dưới tiêu đề")
    m = re.match(r"(\d+(?:\.\d+)?)\s+(.+)$", clean(meta.get("Stage", "")))
    if m:
        st.code, st.name = m.group(1), m.group(2).strip()
    if not st.code:
        st.problems.append("không đọc được mã stage")
    st.slug = clean(meta.get("Slug", "")) or path.stem
    if st.slug != path.stem:
        st.problems.append("Slug '%s' khác tên file" % st.slug)
    st.phase = clean(meta.get("Phase", "")).lower()
    tokens = backticks(meta.get("Produces", ""))
    if "Thư mục" in meta:
        mm = re.search(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", clean(meta["Thư mục"]))
        if mm:
            st.dir = mm.group(0).strip("/")
            st.has_dir_row = True
    if not st.dir:
        first = next((t for t in tokens if "/" in t), None)
        if first:
            st.dir = first.rsplit("/", 1)[0]
        else:
            st.problems.append("không suy được thư mục: thiếu dòng Thư mục và Produces không có đường dẫn")
    for tok in tokens:
        name = tok
        if "/" in tok:
            parent, name = tok.rsplit("/", 1)
            if parent != st.dir:
                continue
        if name.endswith("questions.md"):
            st.questions = st.questions or name
        elif name.endswith(".md") and name not in st.artifacts:
            st.artifacts.append(name)
    override = clean(meta.get("Artifact chính", ""))
    if override:
        st.main = override.split()[0]
        if st.main not in st.artifacts:
            st.artifacts.append(st.main)
    else:
        cands = [a for a in st.artifacts if a != "traceability.md"] or st.artifacts
        st.main = cands[-1] if cands else ""
    if not st.main:
        st.problems.append("không đọc được artifact chính từ Produces")
    st.questions = st.questions or (st.slug + "-questions.md")
    st.templates = backticks(meta.get("Template", ""))
    st.checklist = backticks(meta.get("Checklist", ""))
    st.knowledge = backticks(meta.get("Knowledge", ""))
    st.reviewer = clean(meta.get("Reviewer", ""))
    st.profiles = clean(meta.get("Profiles", ""))
    st.aws_diff = meta.get("Lệch so với AWS")
    return st


def parse_profiles():
    lines = (read(PROFILES_MD) or "").splitlines()
    order, reviewers = [], {}
    rng = section_lines(lines, lambda t: t.lower().startswith("danh sách stage"))
    if rng:
        for t in parse_tables(lines, rng[0], rng[1]):
            for cells, _ in t["rows"]:
                c = clean(cell(cells, 0))
                if re.fullmatch(r"\d+(?:\.\d+)?", c) and c not in order:
                    order.append(c)
    for t in parse_tables(lines):
        pc, rc = col(t["header"], "Profile"), col(t["header"], "Reviewer")
        if pc is None or rc is None:
            continue
        for cells, _ in t["rows"]:
            p = clean(cell(cells, pc))
            if p:
                reviewers[p] = re.findall(r"\d+\.\d+", cell(cells, rc))
    return order, reviewers


def fallback_stage(row):
    code, slug, name, phase, d, main, q = row
    s = Stage()
    s.code, s.slug, s.name, s.phase, s.dir, s.main, s.questions = code, slug, name, phase, d, main, q
    s.artifacts = [main]
    return s


def load_stages():
    warnings, notes, parsed = [], [], []
    order, reviewers = parse_profiles()
    if not order:
        notes.append("Không đọc được bảng 'Danh sách stage' trong profiles.md, xếp stage theo mã.")
    for f in sorted(STAGES_DIR.glob("*.md")):
        try:
            st = parse_stage_file(f)
        except Exception as e:  # file hỏng không được làm sập công cụ
            warnings.append("%s: lỗi khi đọc (%s)" % (f.name, e))
            continue
        if not st.has_dir_row and st.dir:
            notes.append("%s chưa có dòng Thư mục, suy từ Produces: %s" % (f.name, st.dir))
        if st.code and st.slug and st.dir and st.main:
            if st.problems:
                notes.append("%s: %s" % (f.name, "; ".join(st.problems)))
            parsed.append(st)
        else:
            warnings.append("%s: %s" % (f.name, "; ".join(st.problems) or "thiếu thông tin"))
    fb = [fallback_stage(r) for r in FALLBACK_STAGES]
    if not parsed:
        warnings.append("Không đọc được file stage nào trong engine/stages, dùng danh sách dự phòng trong script.")
        return StageSet(fb, warnings, notes, reviewers, "fallback")
    have = set(s.slug for s in parsed)
    for s in fb:
        if s.slug not in have and (STAGES_DIR / (s.slug + ".md")).exists():
            warnings.append("Dùng thông tin dự phòng cho %s vì file stage không đọc được." % s.slug)
            parsed.append(s)
    parsed.sort(key=lambda s: (order.index(s.code) if s.code in order else 1000, code_key(s.code)))
    return StageSet(parsed, warnings, notes, reviewers, "stages")


_STAGES = []


def stages():
    if not _STAGES:
        S = load_stages()
        for w in S.warnings:
            sys.stderr.write("Cảnh báo: %s\n" % w)
        _STAGES.append(S)
    return _STAGES[0]


# ================================================================ intent, state, câu hỏi
def resolve_intent(arg):
    p = Path(arg)
    if p.exists():
        return p
    q = INTENTS / arg
    return q if q.exists() else p


class State(object):
    pass


def load_state(intent):
    path = Path(intent) / "state.md"
    text = read(path)
    if text is None:
        return None
    s = State()
    s.path, s.text, s.lines, s.fm = path, text, text.splitlines(), frontmatter(text)
    s.stages, phase = [], ""
    for i, ln in enumerate(s.lines):
        h = re.match(r"^###\s+(\w+)", ln)
        if h:
            phase = h.group(1).lower()
        m = STAGE_LINE.match(ln)
        if m:
            s.stages.append({"mark": m.group(1), "code": m.group(2), "slug": m.group(3), "rest": m.group(4),
                             "line": i, "phase": phase})
    s.current = {}
    rng = section_lines(s.lines, lambda t: t.lower() == "current")
    if rng:
        for t in parse_tables(s.lines, rng[0], rng[1]):
            for cells, k in [(t["header"], t["hline"])] + t["rows"]:
                if len(cells) >= 2 and clean(cells[0]):
                    s.current[clean(cells[0])] = (cells[1], k)
    s.versions, s.versions_header = {}, []
    rng = section_lines(s.lines, lambda t: t.lower() == "versions")
    if rng:
        for t in parse_tables(s.lines, rng[0], rng[1])[:1]:
            s.versions_header = t["header"]
            for cells, k in t["rows"]:
                if cells and clean(cells[0]) and clean(cells[0]) != "Artifact":
                    s.versions[clean(cells[0])] = (cells, k)
    s.log = []
    rng = section_lines(s.lines, lambda t: t.lower() == "log")
    if rng:
        s.log = [(k, s.lines[k][2:].strip()) for k in range(rng[0] + 1, rng[1]) if s.lines[k].startswith("- ")]
    return s


def entry_phase(e):
    st = stages().by_slug.get(e["slug"])
    return (st.phase if st and st.phase else e["phase"]) or "?"


def entry_label(e):
    return "%s %s" % (e["code"], stages().name(e["slug"]))


def progress_line(entries, focus, nxt):
    active = [e for e in entries if e["mark"] != "S"]
    done = sum(1 for e in active if e["mark"] == "x")
    ph = entry_phase(focus) if focus else ""
    in_ph = [e for e in active if entry_phase(e) == ph]
    dph = sum(1 for e in in_ph if e["mark"] == "x")
    return "Progress: %d/%d | %s %d/%d · Next: %s" % (done, len(active), ph.upper(), dph, len(in_ph),
                                                      entry_label(nxt) if nxt else "không còn stage nào")


def legacy_pointer(intent, rest):
    m = re.search(r"v1:\s*([^\s·,]+)", rest or "")
    return (Path(intent) / m.group(1)) if m else None


def parse_questions(text):
    """(danh sách câu, theo_định_dạng_mới). Mỗi câu: id, dòng, chặn, đã trả lời, tiêu đề."""
    if text is None:
        return [], True
    lines = text.splitlines()
    qs, cur = [], None
    for i, ln in enumerate(lines):
        if ln.startswith("## "):
            cur = None
            m = re.match(r"^##\s+(Q\d+)\b", ln)
            if m:
                cur = {"id": m.group(1), "line": i + 1, "blocking": False, "answered": False,
                       "has_answer": False, "title": ln[3:].strip()}
                qs.append(cur)
            continue
        if cur is None:
            continue
        s = ln.strip()
        if re.match(r"^Chặn:\s*có\b", s, re.I):
            cur["blocking"] = True
        a = re.match(r"^\[Answer\]:(.*)$", s)
        if a:
            cur["has_answer"] = True
            if a.group(1).strip():
                cur["answered"] = True
            else:
                for nx in lines[i + 1:]:
                    if nx.startswith("## "):
                        break
                    if nx.strip() and nx.strip() not in ("---", "***", "___"):
                        cur["answered"] = not nx.strip().lower().startswith("hiểu là")
                        break
    return qs, bool(qs) or not text.strip()


def decision_ids(intent):
    ids = set()
    for t in parse_tables((read(Path(intent) / "decisions.md") or "").splitlines()):
        for cells, _ in t["rows"]:
            c = clean(cell(cells, 0))
            if re.fullmatch(r"DEC\d+", c):
                ids.add(c)
    return ids


def latest_archive(intent, slug, stem):
    d = Path(intent) / "archive" / slug
    best = None
    if d.is_dir():
        for f in d.iterdir():
            m = re.match(re.escape(stem) + r"-v(\d+(?:\.\d+)*)-(\d{8})\.md$", f.name)
            if m:
                key = (ver_tuple(m.group(1)), m.group(2))
                if best is None or key > best[0]:
                    best = (key, f)
    return (best[1], fmt_ver(best[0][0])) if best else (None, None)


def approved_versions(intent, slug, stem):
    d = Path(intent) / "archive" / slug
    out = []
    if d.is_dir():
        for f in d.iterdir():
            m = re.match(re.escape(stem) + r"-v(\d+(?:\.\d+)*)-\d{8}\.md$", f.name)
            if m:
                out.append(ver_tuple(m.group(1)))
    return sorted(out)


def open_crs(intent, so):
    out = []
    if so is not None:
        v = clean(so.current.get("Open CR", ("", None))[0]).lower()
        if v and not v.startswith(("none", "không", "-", "—")):
            out.append("state.md: Open CR = %s" % so.current["Open CR"][0])
    for t in parse_tables((read(Path(intent) / "decisions.md") or "").splitlines()):
        sc = col(t["header"], "Trạng thái")
        if not t["header"] or clean(cell(t["header"], 0)).upper() != "CR" or sc is None:
            continue
        for cells, _ in t["rows"]:
            st = clean(cell(cells, sc)).lower()
            if clean(cell(cells, 0)) and not st.startswith(("đóng", "closed", "huỷ", "hủy", "bác", "rejected", "done", "xong")):
                out.append("decisions.md: %s %s" % (clean(cell(cells, 0)), clean(cell(cells, sc))))
    return out


def live_sources():
    lines = (read(DOMAIN_MD) or "").splitlines()
    rng = section_lines(lines, lambda t: re.match(r"2\.", t) is not None)
    out = []
    if not rng:
        return out
    for t in parse_tables(lines, rng[0], rng[1]):
        h = t["header"]
        lc, dc, vc = col(h, "Loại"), col(h, "Đối chiếu"), col(h, "Phiên bản")
        if lc is None or dc is None:
            continue
        for cells, _ in t["rows"]:
            dtxt = clean(cell(cells, dc))
            out.append({"name": clean(cell(cells, 0)), "kind": clean(cell(cells, lc)).lower(), "date_txt": dtxt,
                        "date": parse_date(dtxt), "version": clean(cell(cells, vc)) if vc is not None else ""})
    return out


def stale_sources(days=STALE_DAYS):
    day0 = today()
    return [s for s in live_sources() if s["kind"] == "sống" and s["date"] and (day0 - s["date"]).days > days]


# ================================================================ trace
def stage_file(intent, slug, which="main"):
    S = stages()
    st = S.by_slug.get(slug)
    if st is None:
        row = next(r for r in FALLBACK_STAGES if r[1] == slug)
        st = fallback_stage(row)
    return Path(intent) / st.dir / (st.main if which == "main" else which)


def us_key(us):
    return int(us[2:])


def trace(intent, write_out=False):
    intent = resolve_intent(intent)
    req_p, sto_p, prd_p = stage_file(intent, "requirements-analysis"), stage_file(intent, "user-stories"), stage_file(intent, "prd-generation")
    req, sto, prd = read(req_p), read(sto_p), read(prd_p)
    missing = [rel(p, intent) for p, t in ((req_p, req), (sto_p, sto)) if t is None]
    if missing:
        print("Không truy vết được %s: thiếu %s." % (intent.name, " và ".join(missing)))
        if sto is None and prd is not None:
            print("Intent chưa có stories.md. Nếu đây là intent chuyển từ luồng cũ, danh sách US nằm trong prd.md; truy vết tay hoặc tách stories.md trước.")
        if prd is not None:
            rows, g, o = ac_layer(prd, re.findall(r"^##\s+`?(US\d+)\b", prd, re.M))
            print("\nKiểm riêng lớp AC của %s, chưa kết luận Đạt:\n" % rel(prd_p, intent))
            print("## AC sang BR")
            print(md_table(["AC", "US", "BR", "Trạng thái"], rows) if rows else "_prd.md chưa có dòng AC nào_")
            print("")
            for x in g:
                print("- GAP: " + x)
            for x in o:
                print("- ORPHAN: " + x)
            print("Lớp AC: GAP %d, ORPHAN %d." % (len(g), len(o)))
        return 2

    frs = []
    for t in parse_tables(req.splitlines()):
        for cells, _ in t["rows"]:
            fid = first_id(cell(cells, 0), ID_FR)
            if fid and fid not in frs:
                frs.append(fid)
    if not frs:
        print("Không đọc được mã FR nào trong %s: cột đầu các bảng không có mã dạng FR1, FR1.1, NFR1. Không kết luận Đạt." % rel(req_p, intent))
        legacy = sorted(set(re.findall(r"\bRC-?\d+\b", req)))
        if legacy:
            print("Thấy %d mã họ cũ (%s...). Script chưa truy vết họ mã này; truy vết tay." % (len(legacy), ", ".join(legacy[:3])))
        return 2

    sto_lines = sto.splitlines()
    rng = section_lines(sto_lines, lambda t: t.lower().startswith("danh sách"))
    us_fr, us_round = {}, {}
    for t in (parse_tables(sto_lines, rng[0], rng[1]) if rng else parse_tables(sto_lines)):
        fc, rc = col(t["header"], "FR"), col(t["header"], "Đợt")
        for cells, _ in t["rows"]:
            us = first_id(cell(cells, 0), ID_US)
            if not us:
                continue
            src = cell(cells, fc) if fc not in (None, 0) else " ".join(cells[1:])
            us_fr[us] = set(FR_RE.findall(clean(src)))
            last = (cell(cells, rc) if rc is not None else cells[-1]).lower()
            us_round[us] = not ("không" in last or "chưa" in last)
    if not us_fr:
        print("Không đọc được mã US nào trong mục Danh sách của %s. Không kết luận Đạt." % rel(sto_p, intent))
        return 2

    explicit = {}
    rng = section_lines(sto_lines, lambda t: t.lower().startswith("fr sang us"))
    if rng:
        for t in parse_tables(sto_lines, rng[0], rng[1]):
            sc, nc = col(t["header"], "Trạng thái"), col(t["header"], "Ghi chú")
            sc = 2 if sc is None else sc
            for cells, _ in t["rows"]:
                fid = first_id(cell(cells, 0), ID_FR)
                if not fid:
                    continue
                note = cell(cells, nc) if nc is not None else " ".join(cells[sc + 1:])
                explicit[fid] = {"us": cell(cells, 1), "status": clean(cell(cells, sc)), "note": clean(note)}

    def deferral(fid):
        e = explicit.get(fid)
        if not e:
            return None
        s, low = e["status"], e["status"].lower()
        for kw, label in (("deferred", "Deferred"), ("n/a", "N/A")):
            if low.startswith(kw):
                reason = s[len(kw):].strip(" \t,:;.-–—()")
                note = "" if e["note"].lower() in EMPTY else e["note"]
                return label, " · ".join(x for x in (reason, note) if x)
        return None

    status, target, gap_of = {}, {}, {}
    good = ("OK", "OK qua FR con", "Deferred", "N/A")
    for fid in sorted(frs, key=lambda f: -f.count(".")):
        uss = sorted([u for u, s in us_fr.items() if fid in s], key=us_key)
        d = deferral(fid)
        if uss:
            status[fid], target[fid] = "OK", ", ".join(uss)
        elif d and d[1]:
            status[fid], target[fid] = d[0], d[1]
        elif d:
            status[fid], target[fid] = "GAP", "-"
            gap_of[fid] = "%s %s chưa có lý do (ghi ở cột Ghi chú hoặc sau chữ %s)" % (fid, d[0], d[0])
        else:
            kids = [k for k in frs if k.startswith(fid + ".")]
            if kids and all(status.get(k) in good for k in kids):
                status[fid], target[fid] = "OK qua FR con", "qua " + ", ".join(kids)
            else:
                status[fid], target[fid] = "GAP", "-"
                bad = [k for k in kids if status.get(k) not in good]
                gap_of[fid] = ("%s chưa có US, FR con chưa phủ hết: %s" % (fid, ", ".join(bad))) if kids else ("%s chưa có US" % fid)
    gaps = [gap_of[f] for f in frs if f in gap_of]
    orphans = []
    fr_rows = [(f, target[f], status[f]) for f in frs]

    us_rows = []
    for us in sorted(us_fr, key=us_key):
        if us_fr[us]:
            us_rows.append((us, ", ".join(sorted(us_fr[us])), "OK"))
        else:
            us_rows.append((us, "-", "ORPHAN"))
            orphans.append("%s không truy về FR nào" % us)
        for fr in sorted(us_fr[us]):
            if fr not in frs:
                us_rows.append((us, fr, "ORPHAN"))
                orphans.append("%s trỏ tới %s không có trong requirements.md" % (us, fr))

    br_rows, prd_note = [], "chưa có prd.md, bỏ kiểm US sang PRD và BR"
    ac_rows, ac_note = [], "chưa có prd.md, bỏ kiểm AC"
    if prd is not None:
        prd_us = re.findall(r"^##\s+`?(US\d+)\b", prd, re.M)
        for us in sorted(us_fr, key=us_key):
            if us_round.get(us) and us not in prd_us:
                gaps.append("%s làm đợt này nhưng chưa có trong prd.md" % us)
        for us in prd_us:
            if us not in us_fr:
                orphans.append("%s có trong prd.md nhưng không có trong stories.md" % us)
        brs = sorted(set(BR_RE.findall(prd)), key=lambda t: (int(t[0]), int(t[1]), t[2]))
        for a, b, c in brs:
            us = "US%s" % a
            ok = us in prd_us or int(a) == 0  # BR0.<n> là rule dùng chung ở PRD mục 4
            br_rows.append(("BR%s.%s%s" % (a, b, c), "dùng chung" if int(a) == 0 else us, "OK" if ok else "ORPHAN"))
            if not ok:
                orphans.append("BR%s.%s%s thuộc %s không có trong prd.md" % (a, b, c, us))
        prd_note = "%d US trong prd.md, %d BR" % (len(prd_us), len(brs))
        ac_rows, ac_gaps, ac_orph = ac_layer(prd, prd_us)
        gaps += ac_gaps
        orphans += ac_orph
        ac_note = "prd.md chưa có dòng AC nào"

    day0 = today().isoformat()
    result = "Đạt" if not gaps and not orphans else "Không đạt"
    body = [
        "# Traceability: %s" % intent.name,
        "",
        "Kiểm ngày %s bằng po-tools.py. Trạng thái: OK có đích · OK qua FR con khi mọi FR con đã phủ · GAP chưa có · ORPHAN không truy về đâu · TRÙNG mã AC lặp · Deferred, N/A ghi ở stories.md kèm lý do." % day0,
        "",
        "## FR sang US",
        md_table(["FR", "US", "Trạng thái"], fr_rows),
        "",
        "## US sang FR",
        md_table(["US", "FR", "Trạng thái"], us_rows),
        "",
        "## BR sang US",
        md_table(["BR", "US", "Trạng thái"], br_rows) if br_rows else "_%s_" % prd_note,
        "",
        "## AC sang BR",
        md_table(["AC", "US", "BR", "Trạng thái"], ac_rows) if ac_rows else "_%s_" % ac_note,
        "",
        "## Kết luận",
        "%s. GAP: %d. ORPHAN: %d." % (result, len(gaps), len(orphans)),
    ]
    body += ["- GAP: " + p for p in gaps] + ["- ORPHAN: " + p for p in orphans]
    text = "\n".join(body) + "\n"
    print(text)

    if write_out:
        out = prd_p.parent / "traceability.md"
        write(out, "---\nintent: %s\nartifact: traceability\nchecked: %s\n---\n" % (intent.name, day0) + text)
        pc = intent / "verification/phase-check-inception.md"
        fr_gap = any(s == "GAP" for s in status.values())
        pc_rows = [
            ("1", "Mọi FR có US, hoặc Deferred, N/A có lý do", "Không đạt" if fr_gap else "Đạt"),
            ("2", "Mọi US truy về FR có thật", "Đạt" if not [o for o in orphans if "FR" in o] else "Không đạt"),
            ("3", "Mọi US làm đợt này có trong PRD", "Chưa kiểm" if prd is None else ("Không đạt" if [g for g in gaps if "prd.md" in g] else "Đạt")),
            ("4", "Mọi BR thuộc một US có trong PRD", "Chưa kiểm" if prd is None else ("Không đạt" if [o for o in orphans if o.startswith("BR")] else "Đạt")),
            ("5", "Mọi BR có AC trỏ tới", "Chưa kiểm" if prd is None else ("Không đạt" if [g for g in gaps if g.endswith("chưa có AC")] else "Đạt")),
        ]
        write(pc, "---\nintent: %s\nphase: inception\ndate: %s\nresult: %s\n---\n# Phase check: INCEPTION · %s\n\nSinh bởi po-tools.py trace. Điều kiện ngữ nghĩa (OQ chặn đã đóng; với profile M, L thì Decision Brief đủ chữ ký ở 2.43) AI kiểm thêm theo template phase-check.md.\n\n%s\n\n## Kết luận\n%s. GAP: %d. ORPHAN: %d. Chi tiết trong %s.\n"
              % (intent.name, day0, result, intent.name, md_table(["#", "Điều kiện", "Kết quả"], pc_rows), result, len(gaps), len(orphans), rel(out, intent)))
        print("Đã ghi:", out, "và", pc)
    return 0 if result == "Đạt" else 1


# ================================================================ check
class Warns(object):
    KINDS = [("heading", "Mục bắt buộc"), ("tag", "Thẻ nguồn"), ("ref", "Thẻ trỏ sai"),
             ("handoff", "Artifact bàn giao"), ("card", "Thẻ US"), ("split", "Cỡ story"), ("words", "Giới hạn từ"),
             ("prd", "PRD"), ("fr", "Cột của FR"), ("design", "Thiết kế của các team"), ("sign", "Chữ ký"), ("diagram", "Sơ đồ")]

    def __init__(self):
        self.items, self.info, self.seen = [], [], set()

    def add(self, kind, f, line, msg, once=False):
        if once:
            if (kind, f, msg) in self.seen:
                return
            self.seen.add((kind, f, msg))
        self.items.append((kind, f, line, msg))


def norm_heading(t):
    t = re.sub(r"<!--.*?-->", "", t or "")
    t = re.sub(r"<[^<>]*>", "", t)
    t = re.sub(r"[\s:]+$", "", clean(unicodedata.normalize("NFC", t))).lower()
    t = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", t)
    return re.sub(r"\s+", " ", t).strip()


def is_optional_heading(t):
    t = unicodedata.normalize("NFC", t or "")
    return bool(re.search(r"<!--\s*(tuỳ|tùy|tuy)\s+chọn\s*-->\s*$", t.strip(), re.I))


def is_assumption_heading(t):
    t = clean(t).lower()
    return "assumptions & open questions" in t or "assumptions and open questions" in t or t.endswith("assumptions")


def is_exempt_heading(t):
    t = clean(t).lower()
    return any(k in t for k in ("sources read", "nguồn đã đọc", "nguồn đã tra", "phụ lục nguồn", "document version", "change log"))


def is_none_value(text):
    t = re.sub(r"^\**[^:*]{1,60}\**:\s*\**", "", clean(text)).strip().strip(".;").lower()
    return t in NONE_VALUES


def is_html_tag(inner):
    s = inner.strip()
    if s.startswith("!--") or "://" in s or s.lower().startswith("mailto:"):
        return True
    m = re.match(r"^/?([A-Za-z][A-Za-z0-9]*)(\s[^<>]*)?/?$", s)
    return bool(m and m.group(1).lower() in HTML_TAGS)


def iter_blocks(lines, start):
    out, stack, cur = [], [], []
    state = {"fence": False, "comment": False}

    def flush():
        if cur:
            out.append({"line": cur[0], "kind": cur[1], "text": " ".join(cur[2]), "stack": [t for _, t in stack]})
            del cur[:]

    i = start
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if state["comment"]:
            if "-->" in s:
                state["comment"] = False
            i += 1
            continue
        if s.startswith("```") or s.startswith("~~~"):
            flush()
            state["fence"] = not state["fence"]
            i += 1
            continue
        if state["fence"]:
            i += 1
            continue
        if s.startswith("<!--"):
            flush()
            state["comment"] = "-->" not in s
            i += 1
            continue
        m = HEAD_RE.match(ln)
        if m:
            flush()
            lvl = len(m.group(1))
            while stack and stack[-1][0] >= lvl:
                stack.pop()
            stack.append((lvl, m.group(2).strip()))
            i += 1
            continue
        if not s or re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s):
            flush()
            i += 1
            continue
        if s.startswith("|"):
            flush()
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            group = [(k, split_cells(lines[k])) for k in range(i, j)]
            has_header = len(group) >= 2 and is_sep_row(group[1][1])
            header = group[0][1] if has_header else []
            for k, cells in (group[2:] if has_header else group):
                if not is_sep_row(cells):
                    out.append({"line": k, "kind": "row", "cells": cells, "header": header,
                                "text": " ".join(cells), "stack": [t for _, t in stack]})
            i = j
            continue
        lm = re.match(r"^\s*([-*+]|\d+[.)])\s+(.*)$", ln)
        if lm:
            flush()
            cur.extend([i, "item", [lm.group(2)]])
        elif cur:
            cur[2].append(s)
        else:
            cur.extend([i, "para", [s.lstrip("> ")]])
        i += 1
    flush()
    return out


def line_flags(lines, start, pred):
    """Cờ cho từng dòng: dòng có nằm dưới heading thoả pred không."""
    flags, stack, fence = [False] * len(lines), [], False
    for i in range(start, len(lines)):
        st = lines[i].strip()
        if st.startswith("```") or st.startswith("~~~"):
            fence = not fence
        m = None if fence else HEAD_RE.match(lines[i])
        if m:
            lvl = len(m.group(1))
            while stack and stack[-1][0] >= lvl:
                stack.pop()
            stack.append((lvl, m.group(2)))
        flags[i] = any(pred(t) for _, t in stack)
    return flags


class CheckCtx(object):
    def __init__(self, intent, stage):
        self.intent, self.stage = intent, stage
        self.decs = decision_ids(intent)
        self.qcache = {}

    def questions(self, st):
        p = Path(self.intent) / st.dir / st.questions
        if p not in self.qcache:
            text = read(p)
            qs, v2 = parse_questions(text)
            self.qcache[p] = (p, text is not None, dict((q["id"], q) for q in qs), v2)
        return self.qcache[p]


def template_lines(path):
    return (read(path) or "").splitlines()

# ================================================================ sơ đồ, theo engine/standards/diagrams.md
NODE_DEF = re.compile(r'\b([A-Za-z][A-Za-z0-9_]*)\s*(\(\(|\(\[|\[\[|\[\(|\(|\[|\{)\s*"?([^"()\[\]{}]*?)"?\s*(\)\)|\]\)|\]\]|\)\]|\)|\]|\})')
EDGE_RE = re.compile(r'([A-Za-z][A-Za-z0-9_]*)\s*(?:--\s*([^-|>][^|>]*?)\s*-->|-->|==>|-\.->)\s*(?:\|([^|]*)\|\s*)?([A-Za-z][A-Za-z0-9_]*)')


def mermaid_blocks(lines, start=0, end=None):
    """[(dòng mở khối, [dòng trong khối])] của mọi khối ```mermaid."""
    end = len(lines) if end is None else end
    out, i = [], start
    while i < end:
        if re.match(r"^\s*```\s*mermaid\b", lines[i]):
            j = i + 1
            while j < end and not lines[j].strip().startswith("```"):
                j += 1
            out.append((i, lines[i + 1:j]))
            i = j + 1
        else:
            i += 1
    return out


def norm_state(t):
    t = clean(re.sub(r"<[^<>]*>", " ", t or "")).strip().strip("*_`\"'")
    return re.sub(r"\s+", " ", t).lower()


STATE_DEF = re.compile(r'^\s*state\s+"([^"]+)"\s+as\s+([A-Za-z][A-Za-z0-9_]*)')
STATE_EDGE = re.compile(r'^\s*(\[\*\]|[A-Za-z][A-Za-z0-9_]*)\s*-->\s*(\[\*\]|[A-Za-z][A-Za-z0-9_]*)\s*(?::\s*(.*\S))?\s*$')


def parse_state(block):
    """(nhãn nút {mã: (nhãn, là [*]?)}, mũi tên [(mã đầu, sự kiện, mã cuối)]) của một sơ đồ stateDiagram-v2.
    [*] ở đầu mũi tên là trạng thái bắt đầu, ở cuối là trạng thái kết thúc."""
    nodes, edges = {"[*]": ("[*]", True)}, []
    for ln in block:
        m = STATE_DEF.match(ln)
        if m:
            nodes[m.group(2)] = (m.group(1).strip(), False)
            continue
        m = STATE_EDGE.match(ln)
        if m:
            edges.append((m.group(1), (m.group(3) or "").strip(), m.group(2)))
    for a, _, b in edges:
        for x in (a, b):
            nodes.setdefault(x, (x, False))
    return nodes, edges


def parse_flow(block):
    """(nhãn nút {mã: (nhãn, tròn?)}, mũi tên [(mã đầu, nhãn mũi tên, mã cuối)]) của một sơ đồ flowchart."""
    nodes, edges = {}, []
    for ln in block:
        if re.match(r"^\s*(%%|style|classDef|class|linkStyle|click|flowchart|graph|subgraph|end\b|direction)", ln.strip()):
            continue
        for m in NODE_DEF.finditer(ln):
            nodes.setdefault(m.group(1), (m.group(3).strip(), m.group(2) in ("((",)))
        bare = NODE_DEF.sub(lambda m: m.group(1), ln)
        pos = 0
        while True:
            m = EDGE_RE.search(bare, pos)
            if not m:
                break
            lab = (m.group(2) or m.group(3) or "").strip()
            edges.append((m.group(1), lab, m.group(4)))
            pos = m.start(4)
    for a, _, b in edges:
        for x in (a, b):
            nodes.setdefault(x, (x, False))
    return nodes, edges


def check_lifecycle(W, f, lines, b0):
    """Vòng đời trạng thái: bảng là nguồn, sơ đồ khớp từng chuyển trạng thái; mọi trạng thái tới được và không cụt."""
    rng = section_lines(lines, lambda t: "vòng đời trạng thái" in t.lower(), b0)
    if not rng:
        return
    lo, hi = rng
    table, tline = set(), {}
    for t in parse_tables(lines, lo, hi):
        h = [clean(x).lower() for x in t["header"]]
        if not any("sự kiện" in x for x in h) or not any(x.endswith("sau") for x in h):
            continue
        fi = next((k for k, x in enumerate(h) if "hiện tại" in x), 0)
        ei = next(k for k, x in enumerate(h) if "sự kiện" in x)
        ti = next(k for k, x in enumerate(h) if x.endswith("sau"))
        for cells, k in t["rows"]:
            a, e, b = (norm_state(cell(cells, x)) for x in (fi, ei, ti))
            if not a or not b or "<" in cell(cells, fi) or clean(cell(cells, fi)).startswith("*"):
                continue
            table.add((a, e, b))
            tline.setdefault((a, e, b), k + 1)
    blocks = mermaid_blocks(lines, lo, hi)
    if table and not blocks:
        W.add("diagram", f, lo + 1, "Vòng đời trạng thái có bảng nhưng chưa có sơ đồ: vẽ stateDiagram-v2 từ bảng, theo engine/standards/diagrams.md mục 3")
        return
    if not blocks:
        return
    diag, starts, ends, states, dline = set(), set(), set(), set(), {}
    for bl, block in blocks:
        head = next((x.strip() for x in block if x.strip()), "")
        nodes, edges = parse_state(block) if head.startswith("stateDiagram") else parse_flow(block)
        for a, lab, b in edges:
            la, ca = nodes[a]
            lb, cb = nodes[b]
            if ca and not cb:
                starts.add(norm_state(lb))
            elif cb and not ca:
                ends.add(norm_state(la))
            elif not ca and not cb:
                key = (norm_state(la), norm_state(lab), norm_state(lb))
                diag.add(key)
                dline.setdefault(key, bl + 1)
        states |= {norm_state(l) for l, c in nodes.values() if not c and "<" not in l}
    if not table:
        W.add("diagram", f, lo + 1, "Vòng đời trạng thái có sơ đồ nhưng chưa có bảng chuyển trạng thái; bảng là nguồn chính")
        return
    for k in sorted(table - diag):
        W.add("diagram", f, tline[k], "Vòng đời trạng thái: chuyển '%s' sang '%s' bằng '%s' có trong bảng, không có trong sơ đồ" % (k[0], k[2], k[1]))
    for k in sorted(diag - table):
        W.add("diagram", f, dline[k], "Vòng đời trạng thái: chuyển '%s' sang '%s' bằng '%s' có trong sơ đồ, không có trong bảng" % (k[0], k[2], k[1]))
    states |= {x for a, _, b in table for x in (a, b)}
    if not starts:
        W.add("diagram", f, lo + 1, "Vòng đời trạng thái: sơ đồ chưa có [*] --> <trạng thái đầu>")
    else:
        seen, todo = set(starts), list(starts)
        while todo:
            x = todo.pop()
            for a, _, b in diag | table:
                if a == x and b not in seen:
                    seen.add(b)
                    todo.append(b)
        for x in sorted(states - seen):
            W.add("diagram", f, lo + 1, "Vòng đời trạng thái: trạng thái '%s' không đi tới được từ trạng thái bắt đầu" % x)
    outs = {a for a, _, _ in diag | table}
    for x in sorted(states - outs - ends):
        W.add("diagram", f, lo + 1, "Vòng đời trạng thái: trạng thái '%s' không có đường ra; nếu là trạng thái cuối thì thêm '%s --> [*]'" % (x, x))


def check_artifact(ctx, W, st, path):
    intent = ctx.intent
    text = read(path) or ""
    lines = text.splitlines()
    b0 = body_start(lines)
    f = rel(path, intent)
    stem = path.stem
    tpls = [data_path(t) for t in st.templates if Path(t).stem == stem]
    if not tpls and (REPO / "engine/templates" / (stem + ".md")).exists():
        tpls = [REPO / "engine/templates" / (stem + ".md")]
    if stem == "prd" and prd_is_legacy(lines):
        tpls = [t for t in tpls if "engine/templates" not in t.as_posix()]
        W.info.append("%s: PRD theo template công ty cũ (có mục Specific Requirement), không kiểm heading của template chuẩn" % f)
    eng = [t for t in tpls if t.exists() and "engine/templates" in t.as_posix()]
    fm = frontmatter(text)
    W.info.append("%s: version %s, status %s" % (f, fm.get("version", "?"), fm.get("status", "?")))

    # 1. heading bắt buộc của template engine
    if eng:
        tl = template_lines(eng[0])
        have = set(norm_heading(t) for _, _, t in headings(lines, b0))
        for _, lvl, t in headings(tl, body_start(tl)):
            if lvl == 2 and not is_optional_heading(t) and norm_heading(t) not in have:
                W.add("heading", f, None, "Thiếu mục bắt buộc của template %s: '## %s'" % (rel(eng[0], REPO), clean(re.sub(r"<!--.*?-->", "", t))))
    elif tpls:
        W.info.append("%s: template là của công ty (%s), không kiểm heading" % (f, ", ".join(show(t) for t in tpls)))

    # sơ đồ: vòng đời trạng thái khớp bảng, theo engine/standards/diagrams.md
    check_lifecycle(W, f, lines, b0)
    # BABOK 7.2: từ khó kiểm ở dòng yêu cầu, chỉ gợi ý
    if stem in ("requirements", "prd"):
        for i in range(b0, len(lines)):
            m = REQ_LINE.match(lines[i])
            v = VAGUE_RE.search(lines[i]) if m else None
            if v:
                W.info.append("Gợi ý, %s:%d %s có từ khó kiểm chứng '%s': thay bằng điều đo được, theo BABOK 7.2" % (f, i + 1, m.group(1), v.group(1)))

    # 2. artifact nội bộ: Assumptions & Open Questions và thẻ nguồn
    if stem in INTERNAL:
        if not any(is_assumption_heading(t) for _, _, t in headings(lines, b0)):
            W.add("heading", f, None, "Thiếu mục 'Assumptions & Open Questions' (bắt buộc với artifact nội bộ, không có gì thì ghi None)")
        stories_exempt = ("danh sách", "fr sang us", "proto-unit", "units")
        for b in iter_blocks(lines, b0):
            hs = [clean(t).lower() for t in b["stack"]]
            if any(is_assumption_heading(t) or is_exempt_heading(t) for t in hs):
                continue
            if stem == "stories" and any(t.startswith(stories_exempt) for t in hs):
                continue
            if b["kind"] == "row":
                if all(clean(c).lower() in EMPTY for c in b["cells"][1:]):
                    continue
            elif is_none_value(b["text"]) or re.fullmatch(r"!\[[^\]]*\]\([^)]*\)", clean(b["text"])):
                continue
            elif b["kind"] == "para" and clean(b["text"]).endswith(":") and len(clean(b["text"])) <= 80:
                continue  # câu dẫn vào danh sách ngay dưới, thẻ nằm ở các mục của danh sách
            if not TAG_RE.search(b["text"]):
                W.add("tag", f, b["line"] + 1, "Khối khẳng định chưa có thẻ nguồn: %s" % snippet(b["text"]))
        in_assump = line_flags(lines, b0, is_assumption_heading)
        fence = False
        for i in range(b0, len(lines)):
            s = lines[i].strip()
            if s.startswith("```") or s.startswith("~~~"):
                fence = not fence
            if fence:
                continue
            for m in TAG_RE.finditer(lines[i]):
                tag = m.group(1)
                q = re.fullmatch(r"(?:(\d+\.\d+)\s+)?(Q\d+)", tag, re.I)
                if q:
                    tst = st if not q.group(1) else stages().by_code.get(q.group(1))
                    if tst is None:
                        W.add("ref", f, i + 1, "[%s] trỏ tới stage %s không có trong engine/stages" % (tag, q.group(1)))
                        continue
                    p, exists, qmap, v2 = ctx.questions(tst)
                    qf = rel(p, intent)
                    qid = q.group(2).upper()
                    if not exists:
                        W.add("ref", f, None, "Có thẻ [Qn] của %s nhưng chưa có %s" % (tst.code, qf), once=True)
                    elif not v2:
                        W.add("ref", f, None, "%s theo định dạng cũ (không có khối ## Q<n>), không kiểm được thẻ [Qn]" % qf, once=True)
                    elif qid not in qmap:
                        W.add("ref", f, i + 1, "[%s] không có câu %s trong %s" % (tag, qid, qf))
                    elif not qmap[qid]["answered"]:
                        W.add("ref", f, i + 1, "[%s] trỏ tới câu chưa có [Answer] trong %s" % (tag, qf))
                elif re.fullmatch(r"DEC\d+", tag, re.I):
                    if tag.upper() not in ctx.decs:
                        W.add("ref", f, i + 1, "[%s] không có trong decisions.md" % tag)
                elif tag.lower() == "assumption" and not in_assump[i]:
                    W.add("ref", f, i + 1, "[assumption] nằm ngoài mục Assumptions & Open Questions: chưa xác nhận thì đưa vào mục đó")

    # 3. artifact bàn giao: không thẻ nguồn, không chữ mẫu
    if stem in HANDOFF:
        guide = set()
        for t in tpls:
            for ln in template_lines(t):
                s = ln.strip()
                if re.fullmatch(r"<[^<>]+>", s) or re.fullmatch(r"\*[^*\s][^*]*[^*\s]\*", s):
                    guide.add(s)
        fence = comment = False
        for i in range(b0, len(lines)):
            raw = lines[i]
            s = raw.strip()
            if comment:
                comment = "-->" not in s
                continue
            if s.startswith("```") or s.startswith("~~~"):
                fence = not fence
                continue
            if fence:
                continue
            if s.startswith("<!--"):
                comment = "-->" not in s
                continue
            plain = strip_inline_code(raw)
            for m in TAG_RE.finditer(plain):
                W.add("handoff", f, i + 1, "Artifact bàn giao không ghi thẻ nguồn: [%s]" % m.group(1))
            for m in PLACEHOLDER_RE.finditer(re.sub(r"<!--.*?-->", "", plain)):
                if not is_html_tag(m.group(1)):
                    W.add("handoff", f, i + 1, "Chữ mẫu của template còn sót: <%s>" % m.group(1))
            if s in guide:
                W.add("handoff", f, i + 1, "Dòng hướng dẫn của template còn nguyên: %s" % snippet(s))

    # 4. riêng từng artifact
    if stem == "stories":
        hs = headings(lines, b0)
        cards = [(k, i, lvl, t) for k, (i, lvl, t) in enumerate(hs) if lvl >= 3 and re.match(r"US\d+\b", clean(t))]
        if not cards:
            W.add("card", f, None, "Chưa có thẻ ### US<n> nào")
        for k, i, lvl, t in cards:
            end = next((j for j, l2, _ in hs[k + 1:] if l2 <= lvl), len(lines))
            items = [clean(re.sub(r"^\s*[-*+]\s+", "", l)).lower() for l in lines[i + 1:end] if re.match(r"^\s*[-*+]\s+", l)]
            miss = [lab for lab in US_CARD_LABELS if not any(it.startswith(lab.lower()) for it in items)]
            if miss:
                W.add("card", f, i + 1, "Thẻ %s thiếu mục: %s" % (clean(t).split(":")[0], ", ".join(miss)))
            name = clean(t).split(":", 1)[1] if ":" in clean(t) else ""
            if re.search(r"(?<!\w)và(?!\w)", name):
                W.add("split", f, i + 1, "Tên %s có chữ 'và': xem có phải hai việc người dùng làm riêng được không, theo engine/standards/story-splitting.md mục 4" % clean(t).split(":")[0])
    if stem == "decision-brief":
        h2 = [(i, t) for i, lvl, t in headings(lines, b0) if lvl == 2]
        total, parts = 0, []
        for k, (i, t) in enumerate(h2):
            m = re.match(r"(\d+)\.", clean(t))
            if not m or int(m.group(1)) not in BRIEF_AI_SECTIONS:
                continue
            end = h2[k + 1][0] if k + 1 < len(h2) else len(lines)
            n = count_words(lines[i + 1:end])
            total += n
            parts.append("%s: %d" % (m.group(1), n))
        W.info.append("%s: mục 1 đến 9 có %d từ, giới hạn %d (%s)" % (f, total, BRIEF_WORD_LIMIT, ", ".join(parts)))
        if total > BRIEF_WORD_LIMIT:
            W.add("words", f, None, "Phần AI viết (mục 1 đến 9) có %d từ, quá giới hạn %d" % (total, BRIEF_WORD_LIMIT))
        signs = sign_status(lines)
        for who in SIGNERS:
            st_ = signs.get(who)
            if st_ is None:
                W.add("sign", f, None, "Bảng Ký thiếu dòng %s" % who)
            elif st_.lower() not in SIGNED:
                W.add("sign", f, None, "%s chưa ký, đang ghi '%s'%s" % (who, st_ or "trống", ": gate là Request Changes" if st_.lower() == "yêu cầu sửa" else ""))
    if stem == "prd":
        legacy = prd_is_legacy(lines)
        per_us = {}
        for a in prd_acs(lines, b0):
            per_us.setdefault(a["us"], []).append(a)
        for u, al in sorted(per_us.items()):
            if len(al) > STORY_AC_MAX:
                W.add("split", f, al[0]["line"], "US%d có %d AC, quá %d: story có thể quá lớn, xem engine/standards/story-splitting.md mục 4" % (u, len(al), STORY_AC_MAX))
            if not any(SAD_RE.search(clean(a["text"])) for a in al):
                W.add("prd", f, al[0]["line"], "US%d chưa thấy AC cho nhánh lỗi hoặc bị từ chối; mỗi US cần ít nhất một, ngưỡng số cần AC ở giá trị biên" % u)
        for b in prd_us_blocks(lines):
            blines = lines[b["start"]:b["end"]]
            if "chưa làm" in clean(b["title"]).lower():
                continue
            if not us_priority("\n".join(blines))[0]:
                W.add("prd", f, b["start"] + 1, "US%d chưa có dòng Ưu tiên (Must, Should, Could): Story List sẽ để trống cột Priority" % b["num"])
            if not legacy and not split_us_block(lines, b["start"], b["end"])["corner"]:
                W.add("prd", f, b["start"] + 1, "US%d chưa ghi Trường hợp ngoại lệ: ghi góc từ Impact Matrix mục Coverage Gaps, hoặc ghi 'Không có góc nào từ Impact Matrix chạm US này'" % b["num"])
        qpo = sum(len(re.findall(r"❓\s*`?PO", ln)) for ln in lines[b0:])
        if not legacy and qpo > PRD_QPO_MAX:
            W.add("prd", f, None, "PRD còn %d chỗ ❓PO, quá %d khi trình duyệt: trả lời bớt hoặc chuyển thành câu hỏi mở có người trả lời" % (qpo, PRD_QPO_MAX))
        for i, lvl, t in headings(lines, b0):
            if re.search(r"\b(database|api)\b", clean(t), re.I):
                W.add("prd", f, i + 1, "PRD không có mục thiết kế kỹ thuật như Database, API: '%s'" % clean(t))
        defs = {}
        skip = line_flags(lines, b0, lambda t: any(k in clean(t).lower() for k in ("traceability", "truy vết")))
        fence = False
        for i in range(b0, len(lines)):
            s = lines[i].strip()
            if s.startswith("```") or s.startswith("~~~"):
                fence = not fence
            if fence or skip[i]:
                continue
            code = None
            m = re.match(r"^\s*(?:(?:[-*+]|\d+[.)])\s+)?[`*_]*(BR-?\d+\.\d+[a-z]?)(?![\w.])", lines[i])
            if m:
                code = m.group(1)
            elif s.startswith("|"):
                code = first_id(cell(split_cells(s), 0), re.compile(r"BR-?\d+\.\d+[a-z]?"))
            if code:
                key = code.replace("-", "")
                if key in defs:
                    W.add("prd", f, i + 1, "%s định nghĩa lần nữa, lần đầu ở dòng %d" % (code, defs[key]))
                else:
                    defs[key] = i + 1
        W.info.append("%s: %d mã BR được định nghĩa" % (f, len(defs)))
        acs, seen_ac = prd_acs(lines, b0), {}
        for a in acs:
            if a["id"] in seen_ac:
                W.add("prd", f, a["line"], "%s định nghĩa lần nữa, lần đầu ở dòng %d" % (a["id"], seen_ac[a["id"]]))
            else:
                seen_ac[a["id"]] = a["line"]
            miss = [k for k in ("Given", "When", "Then") if not re.search(r"\b%s\b" % k, a["text"], re.I)]
            if miss:
                msg = "%s chưa theo cấu trúc Given/When/Then, thiếu %s" % (a["id"], ", ".join(miss))
                if legacy:
                    W.info.append("Gợi ý, %s:%d %s" % (f, a["line"], msg))
                else:
                    W.add("prd", f, a["line"], msg)
        W.info.append("%s: %d mã AC" % (f, len(seen_ac)))
        refd = set(br_label(t) for a in acs for t in a["brs"])
        if defs and not acs:
            W.add("prd", f, None, "PRD chưa có dòng AC nào, %d BR chưa có AC trỏ tới. Viết khối Tiêu chí chấp nhận trong mục 4/ của mỗi US" % len(defs))
        elif defs:
            for key, ln in sorted(defs.items(), key=lambda kv: kv[1]):
                if key not in refd:
                    W.add("prd", f, ln, "%s chưa có AC nào trỏ tới" % key)
        pf = clean(fm.get("feature", ""))
        if not pf:
            W.add("prd", f, None, "Frontmatter thiếu feature: ghi mã tính năng của intent.md, chưa có thì cấp bằng po-tools.py feature-id --assign")
        elif not valid_feature(pf):
            W.add("prd", f, None, "feature '%s' ở frontmatter sai dạng <mã sản phẩm>-F<NNN>" % pf)
        elif intent_feature(intent) and intent_feature(intent) != pf:
            W.add("prd", f, None, "feature ở frontmatter là %s, intent.md ghi %s" % (pf, intent_feature(intent)))
    if stem == "requirements":
        had_fr, found = False, False
        for t in parse_tables(lines, b0):
            rows = [(c, k) for c, k in t["rows"] if first_id(cell(c, 0), ID_FR)]
            if not rows:
                continue
            had_fr = True
            pc, ec = col(t["header"], "Ưu tiên", "Priority"), col(t["header"], "Existing")
            if pc is None or ec is None:
                continue
            found = True
            for cells, k in rows:
                fid = first_id(cell(cells, 0), ID_FR)
                if clean(cell(cells, pc)).lower() in EMPTY:
                    W.add("fr", f, k + 1, "%s chưa ghi Ưu tiên" % fid)
                if clean(cell(cells, ec)).lower() in EMPTY:
                    W.add("fr", f, k + 1, "%s chưa ghi Existing, New hay Changed" % fid)
        if not had_fr:
            W.add("fr", f, None, "Không đọc được dòng FR nào (cột đầu bảng phải là mã FR1, FR1.1)")
        elif not found:
            W.add("fr", f, None, "Không tìm thấy bảng FR có cột Ưu tiên và cột Existing, New, Changed")


def count_words(lines):
    n, fence = 0, False
    for ln in lines:
        s = ln.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fence = not fence
            continue
        if fence or HEAD_RE.match(ln) or s.startswith("<!--"):
            continue
        if s.startswith("|") and is_sep_row(split_cells(s)):
            continue
        n += sum(1 for tok in s.split() if re.search(r"\w", tok))
    return n


def sign_status(lines):
    """{vai: trạng thái} từ bảng Ký của Decision Brief: cột Vai và cột Trạng thái."""
    out = {}
    for t in parse_tables(lines):
        vc, sc = col(t["header"], "Vai"), col(t["header"], "Trạng thái")
        if vc is None or sc is None:
            continue
        for cells, _ in t["rows"]:
            who = clean(cell(cells, vc))
            if who in SIGNERS:
                out[who] = clean(cell(cells, sc))
    return out


def exact_col(header, name):
    for idx, h in enumerate(header):
        if clean(h).strip().lower() == name.lower():
            return idx
    return None


def ux_screen_map(text):
    """{số US: [(mã SCR ngắn, tên màn)]} từ bảng Danh sách màn của ux-design.md: cột SCR, cột US, cột Tên màn."""
    out = {}
    for t in parse_tables((text or "").splitlines()):
        sc, uc, nc = exact_col(t["header"], "SCR"), exact_col(t["header"], "US"), col(t["header"], "Tên màn")
        if sc is None or uc is None:
            continue
        for cells, _ in t["rows"]:
            m = re.search(r"SCR(?:-[A-Z][A-Z0-9]*-F\d{3,}-)?(\d+)", clean(cell(cells, sc)))
            if not m:
                continue
            name = clean(cell(cells, nc)) if nc is not None else ""
            for u in re.findall(r"(?<![\w-])US(?:-[A-Z][A-Z0-9]*-F\d{3,}-)?(\d+)\b", cell(cells, uc)):
                out.setdefault(int(u), []).append(("SCR%d" % int(m.group(1)), name))
    return out


def design_coverage(intent, W):
    """Đối chiếu ba file thiết kế ở 2.43 với PRD: file có chưa, dựng từ bản PRD nào, còn chữ mẫu không,
    US có giao diện có màn chưa, AC có trong kế hoạch test chưa, US có trong tech-design chưa."""
    intent = Path(intent)
    prd_p = stage_file(intent, "prd-generation")
    prd = read(prd_p)
    if prd is None:
        W.add("design", rel(prd_p, intent), None, "Chưa có PRD; 2.43 chạy sau khi PRD được duyệt")
        return
    pl = prd.splitlines()
    pver = clean(frontmatter(prd).get("version", ""))
    blocks = [b for b in prd_us_blocks(pl) if "chưa làm" not in clean(b["title"]).lower()]
    texts = {}
    for name, rp, who in TEAM_DESIGNS:
        t = read(intent / rp)
        texts[name] = t
        if t is None:
            W.add("design", rp, None, "Chưa có file thiết kế của %s" % who)
            continue
        m = re.search(r"prd@v?(\d+(?:\.\d+)*)", frontmatter(t).get("inputs", ""))
        if not m:
            W.add("design", rp, None, "Frontmatter chưa ghi inputs: prd@<version> mà %s đã đọc" % who)
        elif pver and ver_tuple(m.group(1)) != ver_tuple(pver):
            W.add("design", rp, None, "Dựng từ prd@%s, PRD hiện là %s: %s xem lại theo bản mới" % (m.group(1), pver, who))
        tl = t.splitlines()
        left = [k for k in range(body_start(tl), len(tl)) if PLACEHOLDER_RE.search(re.sub(r"`[^`]*`", "", tl[k]))]
        if left:
            W.add("design", rp, left[0] + 1, "Còn %d dòng chữ mẫu của template: %s chưa viết xong" % (len(left), who))
    if texts.get("ux-design") is not None:
        smap = ux_screen_map(texts["ux-design"])
        for b in blocks:
            if us_has_ui(split_us_block(pl, b["start"], b["end"])["ui"]) and b["num"] not in smap:
                W.add("design", TEAM_DESIGNS[0][1], None, "US%d có giao diện trong PRD nhưng ux-design chưa có màn" % b["num"])
    if texts.get("test-design") is not None:
        have = set("AC%d.%s" % (int(a), c) for a, c in re.findall(r"AC-?(?:[A-Z][A-Z0-9]*-F\d{3,}-)?(\d+)\.(\d+)", texts["test-design"]))
        for a in prd_acs(pl):
            if a["id"] not in have:
                W.add("design", TEAM_DESIGNS[2][1], None, "%s chưa có trong kế hoạch test" % a["id"])
    if texts.get("tech-design") is not None:
        have = set(int(u) for u in re.findall(r"(?<![\w-])US(?:-[A-Z][A-Z0-9]*-F\d{3,}-)?(\d+)\b", texts["tech-design"]))
        for b in blocks:
            if b["num"] not in have:
                W.add("design", TEAM_DESIGNS[1][1], None, "US%d chưa có trong tech-design" % b["num"])


def check(intent, slug, strict=False):
    intent = resolve_intent(intent)
    S = stages()
    st = S.by_slug.get(slug)
    if st is None:
        print("Không có stage '%s'. Stage hợp lệ: %s" % (slug, ", ".join(s.slug for s in S.list)))
        return 2
    if not intent.is_dir():
        print("Không thấy thư mục intent:", intent)
        return 2
    d = intent / st.dir
    files = [d / a for a in st.artifacts if (d / a).exists()]
    if not files and slug != "design-alignment":
        print("Chưa có artifact của %s %s trong %s, chưa có gì để kiểm." % (st.code, st.name, rel(d, intent)))
        so = load_state(intent)
        e = next((x for x in (so.stages if so else []) if x["slug"] == slug), None)
        lp = legacy_pointer(intent, e["rest"]) if e else None
        if lp:
            print("state.md trỏ stage này tới artifact của luồng cũ: %s. Lệnh check chỉ kiểm artifact theo template mới." % rel(lp, intent))
        return 2
    ctx = CheckCtx(intent, st)
    W = Warns()
    for p in files:
        check_artifact(ctx, W, st, p)
    if slug == "design-alignment":
        design_coverage(intent, W)
    print("# Kiểm máy: %s · %s %s\n" % (intent.name, st.code, st.name))
    for x in W.info:
        print("- " + x)
    print("")
    if not W.items:
        print("Không có cảnh báo.")
        return 0
    cap = 40
    for kind, title in Warns.KINDS:
        its = [w for w in W.items if w[0] == kind]
        if not its:
            continue
        print("## %s (%d)" % (title, len(its)))
        for _, fpath, line, msg in its[:cap]:
            print("- %s%s %s" % (fpath, (":%d" % line) if line else "", msg))
        if len(its) > cap:
            print("- ... còn %d cảnh báo loại này" % (len(its) - cap))
        print("")
    print("Kết luận: %d cảnh báo." % len(W.items))
    return 1 if strict else 0


# ================================================================ archive
def archive_dst(intent, slug, src, tag, day=None):
    day = day or today().strftime("%Y%m%d")
    return Path(intent) / "archive" / slug / ("%s-%s-%s.md" % (Path(src).stem, tag, day))


def archive(intent, slug, artifact, label=None):
    intent = resolve_intent(intent)
    src = Path(artifact)
    if not src.is_absolute() and not src.exists():
        src = intent / artifact
    st = stages().by_slug.get(slug)
    if not src.exists() and st and (intent / st.dir / artifact).exists():
        src = intent / st.dir / artifact
    if not src.exists():
        print("Không thấy artifact:", src)
        return 2
    fm = frontmatter(read(src))
    dst = archive_dst(intent, slug, src, label or ("v" + fm.get("version", "0")))
    if dst.exists():
        print("Đã có, không ghi đè: %s. Dùng --label để đặt tên khác." % dst)
        return 2
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(dst))
    print("Đã chụp:", dst)
    return 0


# ================================================================ approve
def table_line(cells):
    return "| " + " | ".join(esc(c) for c in cells) + " |"


def next_entry(entries, idx):
    """Stage kế theo thứ tự: stage đầu tiên sau idx chưa duyệt và không bỏ qua, kể cả stage đang làm dở."""
    e = next((x for x in entries[idx + 1:] if x["mark"] not in "xS"), None)
    return e or next((x for x in entries if x["mark"] not in "xS"), None)


def set_current(lines, key, value):
    rng = section_lines(lines, lambda t: t.lower() == "current")
    if not rng:
        return False
    for t in parse_tables(lines, rng[0], rng[1]):
        for cells, k in [(t["header"], t["hline"])] + t["rows"]:
            if k is not None and len(cells) >= 2 and clean(cells[0]) == key:
                lines[k] = table_line([cells[0], value] + cells[2:])
                return True
        lines.insert(t["end"], table_line([key, value]))
        return True
    return False


def published_ref(fm):
    """Nơi đăng bản đọc ngoài repo, nếu domain có đăng: khoá published, nhận cả khoá lark của bản cũ."""
    return (fm.get("published") or fm.get("lark") or "").strip()


def upsert_version(lines, stem, ver, day):
    rng = section_lines(lines, lambda t: t.lower() == "versions")
    if not rng:
        at = next((i for i, l in enumerate(lines) if re.match(r"^##\s+Log\b", l)), len(lines))
        lines[at:at] = ["## Versions", "| Artifact | Version | Status | Approved | Bản đăng |", "|---|---|---|---|---|",
                        table_line([stem, "v" + ver, "approved", day, "-"]), ""]
        return "thêm mục Versions"
    tabs = parse_tables(lines, rng[0], rng[1])
    if not tabs:
        lines.insert(rng[0] + 1, table_line([stem, "v" + ver, "approved", day, "-"]))
        return "thêm dòng"
    t = tabs[0]
    h = t["header"] or ["Artifact", "Version", "Status", "Approved", "Bản đăng"]
    vc, sc, ac = col(h, "Version"), col(h, "Status"), col(h, "Approved")
    vc, sc, ac = 1 if vc is None else vc, 2 if sc is None else sc, 3 if ac is None else ac
    for cells, k in t["rows"]:
        if clean(cell(cells, 0)) == stem:
            cells = cells + [""] * (len(h) - len(cells))
            old = clean(cells[ac])
            cells[vc], cells[sc] = "v" + ver, "approved"
            cells[ac] = ("v%s: %s · %s" % (ver, day, cells[ac].strip())) if re.search(r"v\d", old) else day
            lines[k] = table_line(cells)
            return "sửa dòng"
    row = [""] * len(h)
    row[0], row[vc], row[sc], row[ac] = stem, "v" + ver, "approved", day
    if len(h) > 4:
        row[col(h, "Bản đăng", "Lark") or 4] = "-"
    lines.insert(t["end"], table_line(row))
    return "thêm dòng"


def append_log(lines, entry):
    rng = section_lines(lines, lambda t: t.lower() == "log")
    if not rng:
        lines.extend(["", "## Log", entry])
        return
    last = rng[0]
    for k in range(rng[0] + 1, rng[1]):
        if lines[k].strip():
            last = k
    lines.insert(last + 1, entry)


def add_decision(text, row_vals):
    lines = (text or "").splitlines()
    target = None
    for t in parse_tables(lines):
        if t["header"] and clean(t["header"][0]).upper() == "DEC" and col(t["header"], "Quyết định") is not None:
            target = t
            break
    if target is None:
        hdr = ["DEC", "Ngày", "Stage", "Quyết định", "Nguyên văn", "Người quyết", "Read when"]
        lines += ["", table_line(hdr), "|" + "---|" * len(hdr), table_line([row_vals.get(k, "") for k in hdr])]
        return "\n".join(lines) + "\n", table_line([row_vals.get(k, "") for k in hdr])
    h = target["header"]
    row = []
    for name in h:
        key = clean(name)
        row.append(next((v for k, v in row_vals.items() if k.lower() == key.lower()), ""))
    line = table_line(row)
    lines.insert(target["end"], line)
    return "\n".join(lines) + "\n", line


def next_dec(text):
    nums = [int(m) for t in parse_tables((text or "").splitlines()) for cells, _ in t["rows"]
            for m in re.findall(r"^DEC(\d+)$", clean(cell(cells, 0)))]
    return "DEC%d" % ((max(nums) if nums else 0) + 1)


def norm_words(t):
    t = unicodedata.normalize("NFC", t or "").casefold()
    t = re.sub(r"[\"“”'‘’`]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def human_turns():
    """Lượt người thật do engine/scripts/po-hook.py ghi vào .po/turns.jsonl: [(thời điểm, nội dung)]. None khi chưa có sổ."""
    text = read(TURNS)
    if text is None:
        return None
    out = []
    for ln in text.splitlines():
        try:
            d = json.loads(ln)
            ts = datetime.datetime.strptime(str(d["ts"])[:19], "%Y-%m-%dT%H:%M:%S")
        except (ValueError, KeyError, TypeError):
            continue
        out.append((ts, str(d.get("text") or "")))
    return out


NEGATION = ("chưa", "không", "ko", "đừng", "khoan", "chẳng", "chớ", "no", "not", "dont", "don't", "never")


def said(w, t):
    """Lời w có trong lượt t: khớp nguyên từ, và ba từ ngay trước không có từ phủ định như "chưa duyệt", "không ok"."""
    for m in re.finditer(r"(?<!\w)%s(?!\w)" % re.escape(w), t):
        before = re.findall(r"\w+(?:'\w+)?", t[:m.start()])[-3:]
        if not any(x in NEGATION for x in before):
            return True
    return False


def presence(words, since, label):
    """Lời PO phải có nguyên văn trong một lượt người ghi sau mốc since, như HUMAN_TURN của AWS AI-DLC.
    Trả None khi đạt, câu lý do khi không. PO tự gõ lệnh trong terminal thì coi là có mặt."""
    if sys.stdin.isatty() and sys.stdout.isatty():
        return None
    turns = human_turns()
    if turns is None:
        return ("không thấy sổ lượt người %s. Lời %s phải do PO nói: mở phiên Claude Code ở gốc repo để hook trong "
                ".claude/settings.json ghi sổ, hoặc PO tự chạy lệnh này trong terminal." % (show(TURNS), label))
    w = norm_words(words)
    if len(w) < 2:
        return "lời %s quá ngắn để đối chiếu với lời PO." % label
    for ts, text in turns:
        if ts >= since and said(w, norm_words(text)):
            return None
    return ("không thấy lời %s \"%s\" trong lượt nào của PO từ %s, lúc artifact được sửa lần cuối. Trình gate, chờ PO trả lời, "
            "sau đó chép đúng lời PO vào tham số." % (label, (words or "").strip(), since.strftime("%H:%M %d/%m/%Y")))


def stage_artifacts(intent, st, fallback=None):
    d = Path(intent) / st.dir
    arts = [d / a for a in st.artifacts if (d / a).exists()]
    return arts or ([fallback] if fallback is not None and Path(fallback).exists() else [])


def machine_warnings(intent, st):
    """Số cảnh báo của po-tools.py check cho stage; 0 khi stage chưa có artifact theo template mới."""
    files = [p for p in stage_artifacts(intent, st)]
    if not files:
        return 0
    ctx, W = CheckCtx(intent, st), Warns()
    for p in files:
        check_artifact(ctx, W, st, p)
    if st.slug == "design-alignment":
        design_coverage(intent, W)
    return len(W.items)


def art_digest(intent, arts):
    h = hashlib.sha256()
    for p in sorted(arts):
        h.update(rel(p, intent).encode("utf-8") + b"\0" + norm_body(read(p)).encode("utf-8") + b"\0")
    return h.hexdigest()


def review_files(intent, slug):
    d = Path(intent) / "reviews"
    out = []
    if d.is_dir():
        for p in d.glob("review-%s-*.md" % slug):
            m = re.fullmatch(r"review-%s-(\d+)\.md" % re.escape(slug), p.name)
            if m:
                out.append((int(m.group(1)), p))
    return sorted(out)


def reviewer_needed(so, st):
    """Stage có bật AI Reviewer với profile của intent, và state.md không tắt reviewer."""
    if re.search(r"reviewer:\s*off", so.text or "", re.I):
        return False
    prof = clean(so.fm.get("profile", "")).upper()[:1]
    return st.code in stages().reviewers.get(prof, [])


def review_gap(intent, st, arts):
    """None khi lần review mới nhất có Verdict và ứng với đúng bản artifact hiện tại; không thì câu lý do."""
    revs = review_files(intent, st.slug)
    if not revs:
        return "%s %s bật AI Reviewer nhưng reviews/ chưa có file review nào của stage này." % (st.code, st.name)
    n, rp = revs[-1]
    if not re.search(r"Verdict\W*\s*(READY|NOT-READY)", read(rp) or ""):
        return "%s chưa có dòng Verdict." % rel(rp, intent)
    dg = read(rp.with_suffix(".digest"))
    m = re.search(r"sha256 ([0-9a-f]{64})", dg or "")
    if not m:
        return ("%s không có bản ghi artifact lúc review, nên không biết review ứng với bản nào. Trước khi gọi reviewer, chạy "
                "po-tools.py review-start." % rel(rp, intent))
    if m.group(1) != art_digest(intent, arts):
        return "artifact đã đổi sau review lần %02d; theo review-protocol phải review lại trước khi trình gate." % n
    return None


def review_start(intent, slug):
    """Ghi dấu artifact trước khi gọi AI Reviewer: reviews/review-<slug>-NN.digest, để approve biết review ứng với bản nào."""
    intent = resolve_intent(intent)
    st = stages().by_slug.get(slug)
    if st is None:
        print("Không có stage '%s'." % slug)
        return 2
    arts = stage_artifacts(intent, st)
    if not arts:
        print("Chưa có artifact của %s %s trong %s, chưa có gì để review." % (st.code, st.name, rel(intent / st.dir, intent)))
        return 2
    revs = review_files(intent, slug)
    n = (revs[-1][0] + 1) if revs else 1
    dst = intent / "reviews" / ("review-%s-%02d.digest" % (slug, n))
    dst.parent.mkdir(parents=True, exist_ok=True)
    write(dst, "sha256 %s\nartifacts: %s\ncreated: %s\n" % (art_digest(intent, arts), ", ".join(rel(a, intent) for a in arts),
                                                         now().strftime("%Y-%m-%d %H:%M")))
    print("Review lần %02d của %s %s. Đã ghi %s." % (n, st.code, st.name, rel(dst, intent)))
    print("Reviewer ghi kết quả vào reviews/review-%s-%02d.md. Artifact đổi sau mốc này thì approve đòi review lại." % (slug, n))
    return 0


def approve(intent, slug, words, who=None, version=None, dry=False, accept_warnings=None, accept_review_gap=None):
    intent = resolve_intent(intent)
    S = stages()
    st = S.by_slug.get(slug)
    if st is None:
        print("Không có stage '%s'. Stage hợp lệ: %s" % (slug, ", ".join(s.slug for s in S.list)))
        return 2
    so = load_state(intent)
    if so is None:
        print("Không thấy state.md trong", intent)
        return 2
    idx = next((k for k, e in enumerate(so.stages) if e["slug"] == slug), None)
    if idx is None:
        print("state.md không có dòng của stage %s. Thêm stage vào state.md trước khi duyệt." % slug)
        return 2
    e = so.stages[idx]
    if e["mark"] != "?":
        why = {" ": "chưa làm", "-": "đang làm, chưa trình gate", "R": "đang sửa sau Request Changes, phải trình lại gate trước",
               "x": "đã duyệt rồi", "S": "đang bỏ qua"}.get(e["mark"], "không ở trạng thái chờ duyệt")
        print("Không ghi duyệt: %s %s đang [%s], %s. Chỉ duyệt được stage đang [?] chờ duyệt." % (e["code"], st.name, e["mark"], why))
        return 2
    if not (words or "").strip():
        print("Thiếu --words: cần lời duyệt nguyên văn của PO.")
        return 2
    lp = legacy_pointer(intent, e["rest"])
    path = lp if lp is not None and lp.exists() else intent / st.dir / st.main
    text = read(path)
    if text is None:
        print("Không thấy artifact để duyệt:", rel(path, intent))
        return 2
    arts = stage_artifacts(intent, st, path)
    since = datetime.datetime.fromtimestamp(max(p.stat().st_mtime for p in arts))
    msg = presence(words, since, "duyệt")
    if msg:
        print("Không ghi duyệt: " + msg)
        return 2
    notes, said = [], [words.strip()]
    nwarn = machine_warnings(intent, st)
    if nwarn:
        if not (accept_warnings or "").strip():
            print("Không ghi duyệt: kiểm máy còn %d cảnh báo. Xem bằng python3 engine/scripts/po-tools.py check intents/%s %s. "
                  "Sửa, hoặc trình cho PO; PO chấp nhận thì thêm --accept-warnings \"<lời PO>\"." % (nwarn, intent.name, slug))
            return 2
        msg = presence(accept_warnings, since, "chấp nhận cảnh báo")
        if msg:
            print("Không ghi duyệt: " + msg)
            return 2
        notes.append("chấp nhận %d cảnh báo kiểm máy" % nwarn)
        said.append(accept_warnings.strip())
    if reviewer_needed(so, st):
        gap = review_gap(intent, st, arts)
        if gap:
            if not (accept_review_gap or "").strip():
                print("Không ghi duyệt: %s PO quyết duyệt không review lại thì thêm --accept-review-gap \"<lời PO>\"." % gap)
                return 2
            msg = presence(accept_review_gap, since, "duyệt không review lại")
            if msg:
                print("Không ghi duyệt: " + msg)
                return 2
            notes.append("duyệt khi review không ứng với bản hiện tại")
            said.append(accept_review_gap.strip())
    stem = path.stem
    cur = frontmatter(text).get("version", "")
    if version:
        if not re.fullmatch(r"\d+\.\d+", version):
            print("--version phải có dạng X.Y, ví dụ 1.0")
            return 2
        newv = version
    else:
        prev = approved_versions(intent, slug, stem)
        if not prev:
            newv = "1.0"
        else:
            last, c = prev[-1], ver_tuple(cur)
            newv = fmt_ver(c) if c and c > last else "%d.%d" % (last[0], (last[1] if len(last) > 1 else 0) + 1)
    t_now = now()
    stamp, day = t_now.strftime("%Y-%m-%d %H:%M"), t_now.strftime("%Y-%m-%d")
    approved_at = t_now.strftime("%Y-%m-%dT%H:%M")
    dst = archive_dst(intent, slug, path, "v" + newv, t_now.strftime("%Y%m%d"))
    if dst.exists():
        print("Không ghi duyệt: bản chụp %s đã có, script không ghi đè. Kiểm lại version, hoặc dùng --version." % rel(dst, intent))
        return 2
    who = (who or git_user() or "PO").strip()
    new_art = set_frontmatter(text, [("version", newv), ("status", "approved"), ("approved_at", approved_at)])

    dec_text = read(intent / "decisions.md") or "# Decisions: %s\n" % intent.name
    dec_id = next_dec(dec_text)
    quoted = " · ".join(w if (w[:1] in "\"“" and w[-1:] in "\"”" and len(w) > 1) else '"%s"' % w for w in said)
    new_dec, dec_line = add_decision(dec_text, {"DEC": dec_id, "Ngày": stamp, "Stage": e["code"],
                                                "Quyết định": "Approve %s, %s v%s%s" % (st.name, path.name, newv, "".join("; " + x for x in notes)),
                                                "Nguyên văn": quoted, "Người quyết": who, "Read when": slug})

    lines = so.text.splitlines()
    lines[e["line"]] = lines[e["line"]].replace("- [?]", "- [x]", 1)
    entries = [dict(x) for x in so.stages]
    entries[idx]["mark"] = "x"
    nxt = next_entry(entries, idx)
    if nxt:
        cur_stage = "%s %s" % (nxt["code"], nxt["slug"])
        action = ("Làm tiếp %s" if nxt["mark"] in "-R" else ("Trình gate %s" if nxt["mark"] == "?" else "Bắt đầu %s")) % entry_label(nxt)
    else:
        cur_stage, action = "Mọi stage của profile đã duyệt", "Không còn stage nào. Publish bản bàn giao nếu chưa"
    set_current(lines, "Stage", cur_stage)
    set_current(lines, "Next action", action)
    vchange = upsert_version(lines, stem, newv, day)
    log = "- %s %s approved v%s bởi %s" % (stamp, e["code"], newv, who)
    append_log(lines, log)
    new_state = "\n".join(lines) + "\n"
    prog = progress_line(entries, entries[idx], nxt)

    print(("Chạy thử, chưa ghi gì. Các thay đổi sẽ là:" if dry else "Đã duyệt %s %s: %s v%s." % (e["code"], st.name, path.name, newv)))
    print("- %s: version %s (trước là %s), status approved, approved_at %s" % (rel(path, intent), newv, cur or "chưa có", approved_at))
    print("- Chụp archive: %s" % rel(dst, intent))
    print("- decisions.md thêm %s:\n  %s" % (dec_id, dec_line))
    print("- state.md: %s [?] thành [x]; Versions %s %s v%s approved %s" % (e["code"], vchange, stem, newv, day))
    print("- state.md Log: %s" % log)
    print("- state.md Current: Stage = %s; Next action = %s" % (cur_stage, action))
    if not dry:
        write(path, new_art)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(path), str(dst))
        write(intent / "decisions.md", new_dec)
        write(so.path, new_state)
    print(prog)
    if slug in ("prd-generation", "design-alignment"):
        tag = "%s/%s-v%s" % (intent.name, stem, newv)
        print("Gợi ý tag git cho bản bàn giao: %s" % tag)
        print('Sau khi commit: git tag -a %s -m "%s v%s đã duyệt" && git push origin %s' % (tag, stem, newv, tag))
    return 0


# ================================================================ next
def next_cmd(intent):
    intent = resolve_intent(intent)
    so = load_state(intent)
    if so is None:
        print("Không thấy state.md trong", intent)
        return 2
    ents = so.stages
    if not ents:
        print("state.md không có dòng stage nào dạng '- [ ] 2.3 requirements-analysis'.")
        return 2
    target = next((e for e in ents if e["mark"] == "?"), None)
    if target:
        action = "Trình lại gate cho PO duyệt, không làm lại artifact."
    else:
        target = next((e for e in ents if e["mark"] in "-R"), None)
        if target:
            action = "Làm tiếp: đọc file câu hỏi, tiếp từ câu còn trống hoặc bước đang dở." if target["mark"] == "-" else "Sửa theo phản hồi của PO rồi trình lại gate."
        else:
            target = next((e for e in ents if e["mark"] == " "), None)
            action = "Bắt đầu stage này."
    print("# Việc kế tiếp: %s\n" % intent.name)
    if target is None:
        print("Mọi stage của profile đã duyệt hoặc bỏ qua.")
        print(progress_line(ents, ents[-1], None))
        nx = so.current.get("Next action")
        if nx:
            print("state.md ghi Next action: %s" % clean(nx[0]))
        return 0
    st = stages().by_slug.get(target["slug"])
    print("Stage: %s (%s), đang [%s] %s." % (entry_label(target), target["slug"], target["mark"], WORD_STATE.get(target["mark"], "")))
    print("Việc: %s" % action)
    print(progress_line(ents, target, target))
    if st is None:
        print("Slug %s không có trong engine/stages, không tìm được file câu hỏi." % target["slug"])
        return 0
    qp = intent / st.dir / st.questions
    text = read(qp)
    if text is None:
        print("Câu hỏi: chưa có %s." % rel(qp, intent))
        return 0
    qs, v2 = parse_questions(text)
    if not v2:
        bq = clean(so.current.get("Blocking questions open", ("?", None))[0])
        print("Câu hỏi: %s theo định dạng cũ (không có khối ## Q<n> và [Answer]:), script không đếm được. state.md ghi Blocking questions open: %s." % (rel(qp, intent), bq))
        return 0
    open_q = [q for q in qs if not q["answered"]]
    open_b = [q for q in open_q if q["blocking"]]
    print("Câu hỏi (%s): %d/%d câu còn trống, %d câu chặn còn trống%s." % (
        rel(qp, intent), len(open_q), len(qs), len(open_b), (": " + ", ".join(q["id"] for q in open_b)) if open_b else ""))
    return 0


# ================================================================ status
def status(root):
    root = Path(root)
    if not root.exists():
        print("Không thấy thư mục", root)
        return 2
    S = stages()
    amap = S.artifact_map()
    if "design-alignment" in S.by_slug:
        for name, rp, _ in TEAM_DESIGNS:
            amap.setdefault(name, (S.by_slug["design-alignment"], rp))
    intents = sorted(p for p in root.iterdir() if p.is_dir() and (p / "state.md").exists())
    day0 = today()
    rows, findings = [], []
    for it in intents:
        so = load_state(it)
        fm = so.fm
        ents = so.stages
        cur = dict((k, v[0]) for k, v in so.current.items())
        vers = dict((k, v[0]) for k, v in so.versions.items())
        active = next((e for e in ents if e["mark"] in "-?R"), None) or next((e for e in ents if e["mark"] == " "), None)
        if active is None:
            stage_txt, state_txt = "-", "xong"
        else:
            stage_txt, state_txt = "%s %s" % (active["code"], active["slug"]), WORD_STATE.get(active["mark"], active["mark"])
        if fm.get("status", "").lower() in ("archived", "rejected", "parked"):
            state_txt = fm["status"]
        pub = " · ".join("%s %s" % (k, v[4]) for k, v in vers.items() if len(v) > 4 and clean(v[4]) not in EMPTY)
        rows.append((it.name, fm.get("profile", "?"), stage_txt, state_txt, cur.get("Next action", ""),
                     cur.get("Blocking questions open", ""), cur.get("Open CR", ""), pub or "-"))

        dec = read(it / "decisions.md") or ""
        dec_stages = [c[2] for c in table_rows(dec) if len(c) > 2 and re.fullmatch(r"DEC\d+", clean(c[0]))]
        crs = open_crs(it, so)
        for k, e in enumerate(ents):
            m, n, slug, rest = e["mark"], e["code"], e["slug"], e["rest"]
            stg = S.by_slug.get(slug)
            if stg is None:
                findings.append((it.name, "1. %s %s: slug không có trong engine/stages" % (n, slug), "Sửa state.md theo tên file stage, hoặc chạy po-tools.py migrate"))
                continue
            d = it / stg.dir
            main = d / stg.main
            approved_file = main
            lp = legacy_pointer(it, rest)
            if lp is not None:
                # artifact kế thừa từ luồng v1: kiểm file được trỏ tới, không đòi archive theo slug
                if not lp.exists():
                    findings.append((it.name, "1. %s %s trỏ v1: %s nhưng file không có" % (n, slug, rel(lp, it)), "Sửa đường dẫn trong state.md"))
                approved_file = lp if lp.exists() else None
                main = None
            if m == "x" and main is not None:
                if not main.exists():
                    findings.append((it.name, "1. %s %s đã [x] nhưng thiếu %s" % (n, slug, rel(main, it)), "Kiểm lại state hoặc artifact"))
                arch = it / "archive" / slug
                if not arch.exists() or not any(arch.glob("*.md")):
                    findings.append((it.name, "1. %s %s đã [x] nhưng archive/%s/ trống" % (n, slug, slug), "Chụp bản duyệt: po-tools.py archive"))
            if m == "x" and not any((clean(ds).split() or [""])[0] == n or slug in ds for ds in dec_stages):
                findings.append((it.name, "4. %s %s đã [x] nhưng decisions.md không có DEC của stage" % (n, slug), "Ghi DEC nguyên văn lời duyệt"))
            if m == " " and main is not None and main.exists():
                findings.append((it.name, "2. %s có trên đĩa nhưng %s %s còn [ ]" % (rel(main, it), n, slug), "Cập nhật state.md"))
            if m in "?xR":
                qs, v2 = parse_questions(read(d / stg.questions))
                for q in qs:
                    if q["blocking"] and q["has_answer"] and not q["answered"]:
                        findings.append((it.name, "5. %s %s: %s chặn chưa trả lời nhưng stage đã [%s]" % (n, slug, q["id"], m), "Trả lời hoặc hạ cờ chặn"))
            if m in "?-":
                age = (day0 - datetime.date.fromtimestamp((it / "state.md").stat().st_mtime)).days
                if age > 7:
                    findings.append((it.name, "6. %s %s ở [%s] đã %d ngày không đổi" % (n, slug, m, age), "Nhắc PO, hoặc park"))
            if m == "x" and approved_file is not None and approved_file.exists():
                arch, av = latest_archive(it, slug, approved_file.stem)
                if arch is not None and not crs and norm_body(read(approved_file)) != norm_body(read(arch)):
                    findings.append((it.name, "9. %s %s: %s khác bản đã duyệt %s, không có CR mở" % (n, slug, rel(approved_file, it), rel(arch, it)),
                                     "Artifact đã duyệt bị sửa ngoài CR: mở CR, hoặc trả về đúng bản archive"))
        for name, cells in vers.items():
            if name not in amap:
                continue
            f = it / amap[name][1]
            if not f.exists():
                continue
            ffm = frontmatter(read(f))
            v_state, v_file = cell(cells, 1).lstrip("v"), ffm.get("version", "")
            if ver_tuple(v_state) and ver_tuple(v_file) and ver_tuple(v_state) != ver_tuple(v_file):
                findings.append((it.name, "3. %s: state ghi v%s, file ghi v%s" % (name, v_state, v_file), "Đồng bộ state.md"))
            pub_cell = cell(cells, 4)
            mv = re.search(r"v(\d+\.\d+)", pub_cell)
            if mv and ver_tuple(v_file) and ver_tuple(mv.group(1)) != ver_tuple(v_file):
                findings.append((it.name, "7. %s: bản đăng đang v%s, file đang v%s" % (name, mv.group(1), v_file), "Đăng lại, hoặc ghi chú vì sao chưa"))
            tok_state = re.search(r"\b[A-Za-z0-9]{20,}\b", pub_cell)
            tok_file = published_ref(ffm)
            if tok_state and re.fullmatch(r"[A-Za-z0-9]{20,}", tok_file) and tok_state.group(0) != tok_file:
                findings.append((it.name, "7. %s: state.md ghi bản đăng %s, frontmatter ghi %s" % (name, tok_state.group(0), tok_file), "Sửa khoá published ở frontmatter theo bản đang dùng"))
        order = [e["slug"] for e in ents]
        for stem, (stg, relp) in amap.items():
            f = it / relp
            if not f.exists():
                continue
            for nm, ver in re.findall(r"([A-Za-z0-9_.-]+)@v?(\d+(?:\.\d+)*)", frontmatter(read(f)).get("inputs", "")):
                if nm not in amap:
                    continue
                cur_v = frontmatter(read(it / amap[nm][1])).get("version", "")
                if ver_tuple(cur_v) and ver_tuple(cur_v) > ver_tuple(ver):
                    pos = order.index(stg.slug) if stg.slug in order else 0
                    hit = [x for x in ents[pos:] if x["mark"] in "x?-R"] if stg.slug in order else []
                    names = ", ".join("%s %s" % (x["code"], x["slug"]) for x in hit) or "%s %s" % (stg.code, stg.slug)
                    findings.append((it.name, "9. %s dựng từ %s@%s, nay %s đã v%s. Stage bị ảnh hưởng: %s" % (f.name, nm, ver, nm, cur_v, names),
                                     "Xem lại các stage này qua CR, hoặc ghi DEC giữ nguyên"))
        im = read(it / "intent.md") or ""
        for c in table_rows(section(im, "Related intents")):
            ref = c[0].strip("`").strip()
            if not ref or ref.startswith("<") or ref.lower().startswith("intent"):
                continue
            if not (root / ref).exists():
                findings.append((it.name, "8. Related intents trỏ tới '%s' không tồn tại" % ref, "Sửa intent.md"))
    for fid, its in duplicate_features([root]):
        findings.append((", ".join(i.name for i in its), "10. Mã tính năng %s trùng ở %d intent" % (fid, len(its)),
                         "PO đến sau đổi số bằng feature-id --next, sửa feature trong intent.md và prd.md"))
    for s in stale_sources():
        findings.append(("domain.md", "Nguồn sống '%s' đối chiếu lần cuối %s, đã %d ngày" % (s["name"], s["date_txt"], (day0 - s["date"]).days),
                         "Đọc lại nguồn, sửa KB và ngày đối chiếu"))

    print("## Intent\n")
    if rows:
        print(md_table(["Intent", "Profile", "Stage", "Trạng thái", "Việc kế tiếp", "Câu chặn", "CR mở", "Bản đăng"], rows))
    else:
        print("_Chưa có intent nào trong %s_" % root)
    print("\n## Kiểm tra lệch\n")
    if findings:
        print(md_table(["Intent", "Lệch", "Gợi ý xử lý"], findings))
    else:
        print("state khớp với đĩa")
    return 1 if findings else 0


# ================================================================ replay
def replay(intent):
    intent = resolve_intent(intent)
    so = load_state(intent)
    if so is None:
        print("Không thấy state.md trong", intent)
        return 2
    imd = read(intent / "intent.md") or ""
    ifm = frontmatter(imd)
    h1 = next((l[2:].strip() for l in imd.splitlines() if l.startswith("# ")), "")
    title = ifm.get("title") or h1 or intent.name
    cur = dict((k, clean(v[0])) for k, v in so.current.items())
    out = ["# Bàn giao intent: %s" % title, "",
           "In bởi po-tools.py replay ngày %s, chỉ đọc, không sửa gì." % today().isoformat(), "",
           md_table(["", ""], [("Intent", intent.name), ("Profile", so.fm.get("profile", "?")), ("Trạng thái", so.fm.get("status", "?")),
                               ("Stage hiện tại", cur.get("Stage", "-")), ("Việc kế tiếp", cur.get("Next action", "-")),
                               ("Câu chặn", cur.get("Blocking questions open", "-")), ("CR mở", cur.get("Open CR", "-"))]),
           "", "## Stage"]
    for e in so.stages:
        note = clean(e["rest"]).lstrip("· ").strip()
        out.append("- [%s] %s%s" % (e["mark"], entry_label(e), (": " + note[:160] + ("..." if len(note) > 160 else "")) if note else ""))
    nxt = next((e for e in so.stages if e["mark"] in "?-R"), None) or next((e for e in so.stages if e["mark"] == " "), None)
    out += ["", progress_line(so.stages, nxt or (so.stages[-1] if so.stages else None), nxt) if so.stages else "", "", "## Dòng thời gian"]
    out += ["- " + t for _, t in so.log] or ["_state.md chưa có Log_"]
    dec_lines = (read(intent / "decisions.md") or "").splitlines()
    drows, crs = [], []
    for t in parse_tables(dec_lines):
        h = t["header"]
        if h and clean(h[0]).upper() == "DEC" and col(h, "Quyết định") is not None:
            dc, sc, qc, wc = col(h, "Ngày"), col(h, "Stage"), col(h, "Quyết định"), col(h, "Người quyết")
            for cells, _ in t["rows"]:
                q = clean(cell(cells, qc))
                drows.append((clean(cell(cells, 0)), clean(cell(cells, dc)), clean(cell(cells, sc)), q[:160] + ("..." if len(q) > 160 else ""), clean(cell(cells, wc))))
        elif h and clean(h[0]).upper() == "CR":
            sc = col(h, "Trạng thái")
            nc = col(h, "Nội dung")
            for cells, _ in t["rows"]:
                stx = clean(cell(cells, sc))
                crs.append((clean(cell(cells, 0)), clean(cell(cells, nc))[:120], stx[:120] + ("..." if len(stx) > 120 else "")))
    out += ["", "## Quyết định (%d)" % len(drows)]
    out.append(md_table(["DEC", "Ngày", "Stage", "Quyết định", "Người quyết"], drows) if drows else "_Chưa có DEC_")
    out += ["", "## Change request"]
    out.append(md_table(["CR", "Nội dung", "Trạng thái"], crs) if crs else "_Không có CR trong decisions.md_")
    oc = open_crs(intent, so)
    out.append("CR đang mở: %s" % ("; ".join(oc) if oc else "không có"))
    out += ["", "## Review"]
    revs = sorted((intent / "reviews").glob("*.md")) if (intent / "reviews").is_dir() else []
    rrows = []
    for r in revs:
        rl = (read(r) or "").splitlines()
        verdict = next((clean(l) for l in rl if "verdict" in l.lower()), "-")
        who = next((clean(l) for l in rl if "reviewer" in l.lower() and "verdict" not in l.lower()), "")
        rrows.append((rel(r, intent), verdict, who))
    out.append(md_table(["File", "Verdict", "Reviewer, ngày"], rrows) if rrows else "_Chưa có review_")
    if stage_file(intent, "prd-generation").exists():
        meta, sts = us_handoff(intent)
        if meta is not None:
            out += ["", "## Story giao Dev"]
            csvs = sorted((intent / "stories").glob("story-list-prd-v*.csv"), key=csv_version) if (intent / "stories").is_dir() else []
            out.append("%d story trong PRD v%s, %d đạt điều kiện giao Dev. Story List: %s. Chi tiết: po-tools.py dor %s"
                       % (len(sts), meta["ver"], sum(1 for x in sts if not x["reasons"]), ", ".join(p.name for p in csvs) or "chưa sinh", intent.name))
    out += ["", "## Câu chặn còn mở"]
    qlines = []
    for e in so.stages:
        st = stages().by_slug.get(e["slug"])
        if st is None:
            continue
        qp = intent / st.dir / st.questions
        text = read(qp)
        if text is None:
            continue
        qs, v2 = parse_questions(text)
        if not v2:
            qlines.append("- %s: %s theo định dạng cũ, script không đọc được câu chặn; mở file để xem" % (entry_label(e), rel(qp, intent)))
            continue
        for q in qs:
            if q["blocking"] and not q["answered"]:
                qlines.append("- %s %s: %s (%s:%d)" % (entry_label(e), q["id"], clean(q["title"]), rel(qp, intent), q["line"]))
    out += qlines or ["Không có câu chặn nào còn trống."]
    out += ["", "## Bản đăng"]
    llines = []
    for k, (cells, _) in so.versions.items():
        if clean(cell(cells, 4)) not in EMPTY:
            llines.append("- state.md Versions, %s: %s" % (k, clean(cell(cells, 4))))
    for stem, (stg, relp) in stages().artifact_map().items():
        fmx = frontmatter(read(intent / relp))
        ref = published_ref(fmx)
        if ref and clean(ref).lower() not in EMPTY:
            llines.append("- %s frontmatter published: %s" % (relp, ref))
    il = imd.splitlines()
    rng = section_lines(il, lambda t: t.lower() in ("bản đăng", "lark"))
    if rng:
        for t in parse_tables(il, rng[0], rng[1]):
            for cells, _ in t["rows"]:
                if clean(cell(cells, 0)) and clean(cell(cells, 1)) not in EMPTY:
                    llines.append("- intent.md, %s: %s" % (clean(cell(cells, 0)), clean(cell(cells, 1))))
    out += llines or ["Chưa đăng ra ngoài repo."]
    print("\n".join(out))
    return 0


# ================================================================ index
def index(write_out=False):
    S = stages()
    prd_st = S.by_slug.get("prd-generation") or fallback_stage(FALLBACK_STAGES[-1])
    dfm = frontmatter(read(DOMAIN_MD))
    code = dfm.get("code", "").strip()
    notes = []
    if not code:
        code = (dfm.get("domain") or "X").upper()
        notes.append("domain.md chưa có khoá code ở frontmatter, tạm dùng %s." % code)
    rows = []
    for it in sorted(p for p in INTENTS.iterdir() if p.is_dir()) if INTENTS.is_dir() else []:
        prd = it / prd_st.dir / prd_st.main
        if not prd.exists():
            continue
        fm = frontmatter(read(prd))
        imd = read(it / "intent.md") or ""
        title = frontmatter(imd).get("title") or next((l[2:].strip() for l in imd.splitlines() if l.startswith("# ")), it.name)
        ver = fm.get("version", "?")
        at = fm.get("approved_at", "")
        if not at and fm.get("approved"):
            d = re.search(r"\d{4}-\d{2}-\d{2}", fm["approved"])
            at = (d.group(0) + " (từ khoá approved)") if d else ""
        arch, av = latest_archive(it, prd_st.slug, prd.stem)
        feat = intent_feature(it) or valid_feature(fm.get("feature", ""))
        hmeta, hst = us_handoff(it)
        scell = "%d, %d đạt" % (len(hst), sum(1 for x in hst if not x["reasons"])) if hmeta is not None else "-"
        rows.append((feat or "%s-%s (chưa cấp mã)" % (code, it.name), title, "v" + ver, fm.get("status", "-") or "-", at or "-",
                     fm.get("services", "") or "-", scell, show(arch) if arch else "-", "%s/prd-v%s" % (it.name, ver),
                     published_ref(fm) or "-"))
    out = ["# Spec index", "",
           "Sinh bởi `python3 engine/scripts/po-tools.py index --write` ngày %s. Không sửa tay, chạy lại lệnh khi PRD đổi." % today().isoformat(),
           "",
           "Repo này là nguồn chuẩn của spec cho agent và Dev: đọc PRD theo đường dẫn archive (bản đã duyệt, không bao giờ sửa) hoặc theo tag git ở bảng dưới. Bản đăng ra ngoài repo, nếu có, chép từ repo, có thể chậm hơn repo.",
           ""]
    out.append(md_table(["Mã tính năng", "Tên", "PRD", "Status", "Approved at", "Services", "Story, đạt điều kiện giao Dev", "Bản duyệt mới nhất", "Tag git gợi ý", "Bản đăng"], rows)
               if rows else "_Chưa có intent nào có PRD._")
    text = "\n".join(out) + "\n"
    for n in notes:
        sys.stderr.write("Lưu ý: %s\n" % n)
    if write_out:
        write(INTENTS / "INDEX.md", text)
        print("Đã ghi:", INTENTS / "INDEX.md")
    else:
        print(text)
    return 0


# ================================================================ mã tính năng
FEATURE_FULL = re.compile(r"[A-Z][A-Z0-9]*-F\d{3,}")


def domain_code():
    return clean(frontmatter(read(DOMAIN_MD)).get("code", ""))


def valid_feature(v):
    v = clean(v)
    return v if FEATURE_FULL.fullmatch(v) else ""


def intent_feature(intent):
    return valid_feature(frontmatter(read(Path(intent) / "intent.md")).get("feature", ""))


def feature_map(roots):
    """{mã tính năng: [thư mục intent]} của mọi thư mục có intent.md ngay dưới các gốc."""
    out, seen = {}, set()
    for root in roots:
        root = Path(root)
        if not root.is_dir():
            continue
        for it in sorted(p for p in root.iterdir() if p.is_dir() and (p / "intent.md").exists()):
            key = it.resolve()
            if key in seen:
                continue
            seen.add(key)
            f = intent_feature(it)
            if f:
                out.setdefault(f, []).append(it)
    return out


def duplicate_features(roots):
    return [(f, its) for f, its in sorted(feature_map(roots).items()) if len(its) > 1]


def next_feature(code, roots):
    nums = []
    for f in feature_map(roots):
        m = re.fullmatch(re.escape(code) + r"-F(\d+)", f)
        if m:
            nums.append(int(m.group(1)))
    return "%s-F%03d" % (code, (max(nums) if nums else 0) + 1)


def insert_feature(text, fid):
    """Ghi feature vào frontmatter: thay giá trị mẫu nếu có khoá, không thì chèn ngay sau khoá intent."""
    lines = text.splitlines()
    b = fm_bounds(lines)
    line = "feature: %s" % fid
    if not b:
        lines = ["---", line, "---"] + lines
    else:
        keys = [(i, lines[i].split(":", 1)[0].strip()) for i in range(1, b[1]) if ":" in lines[i]]
        cur = next((i for i, k in keys if k == "feature"), None)
        if cur is not None:
            lines[cur] = line
        else:
            at = next((i for i, k in keys if k == "intent"), None)
            lines.insert(at + 1 if at is not None else b[1], line)
    return "\n".join(lines) + "\n"


def feature_id(root=None, assign=None, dry=False):
    code = domain_code()
    if not code:
        print("domain/domain.md chưa có khoá code ở frontmatter nên chưa cấp được mã tính năng. Thêm code: <mã sản phẩm> theo DOMAIN-SETUP.md.")
        return 2
    if not assign:
        print(next_feature(code, [root] if root else [INTENTS]))
        return 0
    base = Path(root) if root else None
    it = base / assign if base is not None and (base / assign).exists() else resolve_intent(assign)
    imd = Path(it) / "intent.md"
    text = read(imd)
    if text is None:
        print("Không thấy intent.md trong %s." % it)
        return 2
    raw = clean(frontmatter(text).get("feature", ""))
    if raw and not raw.startswith("<"):
        print("%s đã có feature: %s, không cấp mã mới. Mã đã cấp không đổi. Nếu mã này trùng với intent khác thì PO đến sau đổi số: chạy feature-id --next rồi sửa feature trong intent.md và prd.md." % (show(imd), raw))
        return 2
    fid = next_feature(code, [base] if base is not None else [INTENTS, Path(it).parent])
    print(fid)
    if dry:
        print("Chạy thử, chưa ghi gì. Sẽ ghi feature: %s vào %s." % (fid, show(imd)))
        return 0
    write(imd, insert_feature(text, fid))
    print("Đã ghi feature: %s vào %s. Khi viết PRD, ghi cùng mã này ở khoá feature của prd.md." % (fid, show(imd)))
    return 0


# ================================================================ PRD: khối US, AC
SEC_KEYS = ("us", "pre", "scenario", "ac", "ui", "br", "data", "nfr", "oos", "corner")
LIST_HEAD = r"^\s*(?:(?:[-*+]|\d+[.)])\s+)?[`*_]*"
AC_ITEM = re.compile(LIST_HEAD + r"AC-?(\d+)\.(\d+)\b")
AC_CODE = re.compile(r"AC-?\d+\.\d+")
SHORT_US = re.compile(r"(?<![\w-])US(\d+)\b")
SHORT_AC = re.compile(r"(?<![\w-])AC-?(\d+)\.(\d+)\b")
SHORT_BR = re.compile(r"(?<![\w-])BR-?(\d+)\.(\d+)([a-z]?)\b")
SHORT_SCR = re.compile(r"(?<![\w-])SCR(\d+)\b")
PRIORITY_RE = re.compile(r"Ưu tiên\W{0,8}(Must|Should|Could|Won[’']?t)\b", re.I)
PRIORITY_JIRA = {"must": "Highest", "should": "High", "could": "Medium", "wont": "Low"}
# AC cho nhánh lỗi hoặc bị từ chối: chỉ là gợi ý bằng từ khoá, PO và reviewer quyết.
SAD_RE = re.compile(r"\b(không|lỗi|từ chối|sai|thiếu|quá|vượt|hết hạn|chặn|trống|bị khoá|tối đa|tối thiểu|giới hạn)\b", re.I)


def us_priority(text):
    m = PRIORITY_RE.search(text or "")
    if not m:
        return "", ""
    k = re.sub(r"[’']", "", m.group(1).lower())
    return m.group(1).capitalize().replace("’", "'"), PRIORITY_JIRA.get(k, "")


def us_has_ui(ui_lines):
    """US có bảng giao diện với ít nhất một dòng nội dung thật, không tính dòng hướng dẫn in nghiêng của template."""
    for t in parse_tables(ui_lines):
        for cells, _ in t["rows"]:
            vals = [clean(c) for c in cells if clean(c)]
            if vals and not all(v.startswith("*") or "<" in v for v in vals):
                return True
    return False
FULL_AC = re.compile(r"\bAC-[A-Z][A-Z0-9]*-F\d+-\d+\.\d+\b")
FULL_BR = re.compile(r"\bBR-[A-Z][A-Z0-9]*-F\d+-\d+\.\d+[a-z]?\b")
FULL_AC_ITEM = re.compile(LIST_HEAD + r"(AC-[A-Z][A-Z0-9]*-F\d+-\d+\.\d+)\b")
FULL_BR_ITEM = re.compile(LIST_HEAD + r"(BR-[A-Z][A-Z0-9]*-F\d+-\d+\.\d+[a-z]?)\b")
CONT_RE = re.compile(r"^\s{2,}\S")


def to_full(text, feat):
    """Đổi mã ngắn US1, AC1.1, BR1.1, BR-1.1, SCR2 sang mã đầy đủ; mã KB như BR-EDIT-07 giữ nguyên."""
    text = SHORT_BR.sub(lambda m: "BR-%s-%02d.%s%s" % (feat, int(m.group(1)), m.group(2), m.group(3)), text)
    text = SHORT_AC.sub(lambda m: "AC-%s-%02d.%s" % (feat, int(m.group(1)), m.group(2)), text)
    text = SHORT_SCR.sub(lambda m: "SCR-%s-%02d" % (feat, int(m.group(1))), text)
    return SHORT_US.sub(lambda m: "US-%s-%02d" % (feat, int(m.group(1))), text)


def classify_label(label):
    """Loại của một heading hoặc nhãn in đậm trong khối US: us, pre, scenario, ac, ui, br, data, nfr, oos, corner."""
    t = clean(re.sub(r"<!--.*?-->", "", label or "")).lower()
    t = re.sub(r"^\d+\s*[/.)]\s*", "", t).strip(" :")
    if "conner case" in t or "corner case" in t or "ngoại lệ" in t or "edge case" in t:
        return "corner"
    if "out of scope" in t or "ngoài phạm vi" in t:
        return "oos"
    if t.startswith("user story"):
        return "us"
    if ("pre" in t and "condition" in t) or "điều kiện trước" in t or "tiền điều kiện" in t:
        return "pre"
    if "scenario" in t or "kịch bản" in t or t.startswith("luồng"):
        return "scenario"
    if "acceptance" in t or "tiêu chí chấp nhận" in t:
        return "ac"
    if "business" in t or "rule nghiệp vụ" in t or "luật nghiệp vụ" in t:
        return "br"
    if re.search(r"\b(ui|ux)\b", t) or "giao diện" in t:
        return "ui"
    if "data field" in t or t.startswith("dữ liệu"):
        return "data"
    if re.search(r"\bnfr\b", t) or "phi chức năng" in t:
        return "nfr"
    return None


US_SECTION_NAMES = ("specific requirement", "yêu cầu theo user story")


def is_us_section(t):
    """Heading cấp 1 chứa các khối US: Specific Requirement của template công ty, Yêu cầu theo user story của template chuẩn."""
    return re.sub(r"^\d+\.\s*", "", clean(t)).lower().startswith(US_SECTION_NAMES)


def prd_is_legacy(lines):
    """PRD viết theo template công ty cũ: có heading cấp 1 Specific Requirement."""
    return any(l == 1 and clean(t).lower().startswith("specific requirement") for _, l, t in headings(lines, body_start(lines)))


def prd_us_blocks(lines):
    """Khối ## US<n> của PRD, trong mục Specific Requirement nếu có. Khối hết ở heading cấp 1 hoặc 2 kế tiếp."""
    b0 = body_start(lines)
    hs = headings(lines, b0)
    lo, hi = b0, len(lines)
    sr = next((k for k, (i, l, t) in enumerate(hs) if l == 1 and is_us_section(t)), None)
    if sr is not None:
        lo = hs[sr][0]
        hi = next((i for i, l, _ in hs[sr + 1:] if l == 1), len(lines))
    out, seen = [], set()
    for k, (i, l, t) in enumerate(hs):
        if l != 2 or not lo <= i < hi:
            continue
        m = re.match(r"US(\d+)\b\s*[:.\-–]?\s*(.*)$", clean(t))
        if not m or int(m.group(1)) in seen:
            continue
        seen.add(int(m.group(1)))
        end = next((j for j, l2, _ in hs[k + 1:] if l2 <= 2), len(lines))
        out.append({"num": int(m.group(1)), "title": m.group(2).strip(), "start": i, "end": end})
    return out


def tidy(lines):
    """Bỏ khoảng trắng cuối dòng, gộp dòng trống liền nhau, bỏ dòng trống và đường kẻ ở đầu, cuối."""
    out, fence, blank = [], False, False
    hr = re.compile(r"(-{3,}|\*{3,}|_{3,})")
    for ln in lines:
        s = ln.rstrip()
        if s.strip().startswith(("```", "~~~")):
            fence = not fence
        if not fence and not s.strip():
            if out and not blank:
                out.append("")
            blank = True
            continue
        out.append(s)
        blank = False
    while out and (not out[-1].strip() or hr.fullmatch(out[-1].strip())):
        out.pop()
    while out and (not out[0].strip() or hr.fullmatch(out[0].strip())):
        out.pop(0)
    return out


def split_ac_section(body, secs):
    """Mục 4/ Acceptance criteria: tách danh sách AC, bảng UI, BR, Data Field, NFR theo nhãn in đậm hoặc heading ####."""
    state = {"kind": None}
    pre = []

    def put(ln):
        if state["kind"] is None:
            pre.append(ln)
        elif state["kind"] != "ac":
            secs[state["kind"]].append(ln)

    fence, i = False, 0
    while i < len(body):
        ln = body[i]
        s = ln.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fence = not fence
            put(ln)
            i += 1
            continue
        if fence:
            put(ln)
            i += 1
            continue
        m = HEAD_RE.match(ln)
        lab = m.group(2) if m else None
        if lab is None:
            bm = re.fullmatch(r"\*\*([^*][^*]*)\*\*\s*:?", s)
            lab = bm.group(1) if bm else None
        if lab is not None:
            k = classify_label(lab)
            if k is None:
                # nhãn lạ: giữ nguyên nhãn, gắn vào mục đang đọc, chưa có thì vào UI
                k = state["kind"] if state["kind"] not in (None, "ac") else "ui"
                secs[k].extend(["", "**%s**" % lab.strip(), ""])
            state["kind"] = k
            i += 1
            continue
        if AC_ITEM.match(ln):
            secs["ac"].append(ln)
            i += 1
            while i < len(body) and body[i].strip() and CONT_RE.match(body[i]) and not AC_ITEM.match(body[i]):
                secs["ac"].append(body[i])
                i += 1
            continue
        put(ln)
        i += 1
    if any(x.strip() for x in pre):
        secs["ui"][0:0] = pre + [""]


def split_us_block(lines, start, end):
    secs = dict((k, []) for k in SEC_KEYS)
    hs = [h for h in headings(lines, start + 1) if h[0] < end and h[1] == 3]
    first = hs[0][0] if hs else end
    secs["us"].extend(lines[start + 1:first])
    prev = "us"
    for k, (i, lvl, t) in enumerate(hs):
        stop = hs[k + 1][0] if k + 1 < len(hs) else end
        body = lines[i + 1:stop]
        kind = classify_label(t)
        if kind == "ac":
            split_ac_section(body, secs)
        elif kind:
            secs[kind].extend(body)
        else:
            kind = prev if prev not in (None, "ac") else "ui"
            secs[kind].extend(["", "**%s**" % t.strip(), ""] + body)
        prev = kind
    return dict((k, tidy(v)) for k, v in secs.items())


def prd_acs(lines, b0=None):
    """Mọi dòng AC của PRD (mục danh sách hoặc dòng bảng mở đầu bằng AC<n>.<m>), bỏ mục Traceability."""
    b0 = body_start(lines) if b0 is None else b0
    skip = line_flags(lines, b0, lambda t: any(k in clean(t).lower() for k in ("traceability", "truy vết")))
    out, fence, i = [], False, b0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("```") or s.startswith("~~~"):
            fence = not fence
            i += 1
            continue
        if fence or skip[i]:
            i += 1
            continue
        a = None
        m = AC_ITEM.match(lines[i])
        if m:
            a, b = m.group(1), m.group(2)
        elif s.startswith("|"):
            code = first_id(cell(split_cells(s), 0), AC_CODE)
            if code:
                a, b = re.match(r"AC-?(\d+)\.(\d+)", code).groups()
        if a is None:
            i += 1
            continue
        text, j = lines[i], i + 1
        if not s.startswith("|"):
            while j < len(lines) and lines[j].strip() and CONT_RE.match(lines[j]) and not AC_ITEM.match(lines[j]):
                text += " " + lines[j].strip()
                j += 1
        out.append({"id": "AC%d.%s" % (int(a), b), "us": int(a), "line": i + 1, "text": text, "brs": set(BR_RE.findall(text))})
        i = j
    return out


def br_label(t):
    return "BR%s.%s%s" % t


def ac_layer(prd, prd_us):
    """Lớp AC của trace: bảng AC sang BR, GAP và ORPHAN."""
    acs = prd_acs(prd.splitlines())
    rows, gaps, orphans, first = [], [], [], {}
    for a in acs:
        us = "US%d" % a["us"]
        brs = ", ".join(br_label(t) for t in sorted(a["brs"], key=lambda t: (int(t[0]), int(t[1]), t[2])))
        if a["id"] in first:
            st = "TRÙNG"
            gaps.append("%s trùng mã, dòng %d và dòng %d" % (a["id"], first[a["id"]], a["line"]))
        elif us not in prd_us:
            st = "ORPHAN"
            orphans.append("%s thuộc %s không có trong prd.md" % (a["id"], us))
        else:
            st = "OK"
        first.setdefault(a["id"], a["line"])
        rows.append((a["id"], us, brs or "-", st))
    with_ac = set(a["us"] for a in acs)
    covered = set(t for a in acs for t in a["brs"] if int(t[0]) == a["us"])
    no_ac = []
    for t in sorted(set(BR_RE.findall(prd)), key=lambda t: (int(t[0]), int(t[1]), t[2])):
        u = int(t[0])
        if u == 0 or "US%d" % u not in prd_us:
            continue
        if u not in with_ac:
            if u not in no_ac:
                no_ac.append(u)
        elif t not in covered:
            gaps.append("%s chưa có AC" % br_label(t))
    gaps += ["US%d chưa có AC" % u for u in no_ac]
    any_ref = set(t for a in acs for t in a["brs"])
    for t in sorted(set(BR_RE.findall(prd)), key=lambda t: (int(t[1]), t[2])):
        if int(t[0]) == 0 and t not in any_ref:
            gaps.append("%s chưa có AC" % br_label(t))
    return rows, gaps, orphans


def prd_open_issues(lines):
    rng = section_lines(lines, lambda t: "open issues" in t.lower() or "vấn đề tồn đọng" in t.lower() or "câu hỏi mở" in t.lower())
    out = []
    if not rng:
        return out
    for t in parse_tables(lines, rng[0], rng[1]):
        h = t["header"]
        nc = col(h, "Nội dung", "Câu hỏi", "Vấn đề", "Issue")
        wc = col(h, "Người trả lời", "Owner")
        bc = col(h, "Chặn", "Block")
        for cells, _ in t["rows"]:
            txt = " | ".join(cells)
            if not clean(txt.replace("|", "")):
                continue
            out.append({"no": clean(cell(cells, 0)) if nc != 0 else "", "text": cell(cells, nc) if nc is not None else txt,
                        "who": clean(cell(cells, wc)), "block_txt": cell(cells, bc), "all": txt})
    return out


def issue_blocks(it):
    b = clean(it["block_txt"]).lower()
    if b.startswith(("có", "yes")):
        return True
    if b.startswith(("không", "no")):
        # cột Chặn ghi rõ không chặn thì chữ "chặn" ở nội dung câu hỏi không làm câu đó thành câu chặn
        return False
    t = re.sub(r"không\s+chặn|non-?blocking|not\s+blocking", " ", clean(it["all"]).lower())
    return bool(re.search(r"chặn|blocking", t))


# ================================================================ tiện ích story
def story_section_text(text, n):
    """Nội dung mục '## <n>.' của một file Markdown, dùng cho kiểm 'giữ nguyên mục' của selftest."""
    lines = (text or "").splitlines()
    hs = [(i, l, t) for i, l, t in headings(lines, body_start(lines)) if l <= 2]
    for k, (i, l, t) in enumerate(hs):
        m = re.match(r"(\d+)\.", clean(t))
        if l == 2 and m and m.group(1) == n:
            end = hs[k + 1][0] if k + 1 < len(hs) else len(lines)
            return "\n".join(lines[i:end])
    return None


def us_number(arg):
    a = (arg or "").strip()
    a = a[:-3] if a.endswith(".md") else a
    m = re.fullmatch(r"(?:US-?)?(\d+)", a) or re.fullmatch(r"US-.+-(\d+)", a)
    return int(m.group(1)) if m else None


# ================================================================ Story List cho Jira
JIRA_COLS = ["Project key", "Project name", "Project type", "Issue Type", "Summary", "Priority", "Description",
             "Epic Link", "Labels", "Labels", "Labels", "Comment"]
JIRA_KEY = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")
JIRA_DESC_MAX = 32000
STORY_AC_MAX = 6
KB_MIN = ("00-index.md", "glossary.md", "concept-model.md", "data-model.md", "permissions.md", "product-direction.md", "corner-checklist.md")
PRD_QPO_MAX = 3
# Từ khó kiểm chứng, theo BABOK 7.2 (không mơ hồ, kiểm được) và ISO/IEC/IEEE 29148 mục 5.2.7
VAGUE_RE = re.compile(r"(?<!\w)(nhanh chóng|nhanh|dễ dàng|dễ|thân thiện|linh hoạt|hợp lý|phù hợp|tối ưu|một số|nếu cần|tuỳ trường hợp|và/hoặc|v\.v\.|tương đối|đơn giản)(?!\w)", re.I)
REQ_LINE = re.compile(r"^\s*(?:\|\s*)?(?:[-*+]\s+)?[`*_]*((?:N?FR|BR|AC|SC)-?\d+(?:\.\d+)?)\b")  # Spec Kit giới hạn 3 chỗ chưa rõ trong spec, xem ADR 0004
JIRA_SECTIONS = (("us", "MÔ TẢ"), ("pre", "ĐIỀU KIỆN TRƯỚC"), ("scenario", "KỊCH BẢN"), ("ac", "TIÊU CHÍ CHẤP NHẬN"),
                 ("ui", "GIAO DIỆN VÀ VALIDATE"), ("br", "BUSINESS RULE"), ("data", "DỮ LIỆU"), ("nfr", "NFR"),
                 ("corner", "TRƯỜNG HỢP NGOẠI LỆ"), ("oos", "NGOÀI PHẠM VI"))


def jira_config():
    """(project key, project name, project type) từ frontmatter domain/domain.md."""
    fm = frontmatter(read(DOMAIN_MD) or "")
    return (clean(fm.get("jira_project_key", "")).strip("\"'"), clean(fm.get("jira_project_name", "")).strip("\"'"),
            clean(fm.get("jira_project_type", "")).strip("\"'") or "software")


def intent_row(imd, name):
    """Ô thứ hai của dòng bảng trong intent.md có ô đầu bắt đầu bằng name."""
    for ln in (imd or "").splitlines():
        if ln.strip().startswith("|"):
            cells = split_cells(ln)
            if cells and clean(cells[0]).lower().startswith(name.lower()):
                return cell(cells, 1)
    return ""


def jira_epics(imd):
    """(Epic mặc định, {số Unit: Epic}, mọi Epic) từ dòng Jira Epic của intent.md. Ghi 'U2: KEY' để gán Epic theo Unit."""
    txt = intent_row(imd, "Jira Epic")
    keys = list(dict.fromkeys(JIRA_KEY.findall(txt)))
    by_unit = {int(u): k for u, k in re.findall(r"\bU(\d+)\s*[:=]\s*([A-Z][A-Z0-9]+-\d+)", txt)}
    return (keys[0] if keys else ""), by_unit, keys


def prd_unit_map(lines):
    """{số US: 'U<n>'} từ bảng Units của PRD: ô đầu là U<n>, ô sau liệt kê US."""
    out = {}
    for ln in lines:
        if not ln.strip().startswith("|"):
            continue
        cells = split_cells(ln)
        # ô đầu là U<n>, có thể kèm tên Unit như "U1 — Khung nhóm"
        m = re.match(r"U(\d+)\b", clean(cell(cells, 0)))
        if not m:
            continue
        for u in re.findall(r"(?<![\w-])US(\d+)\b", " ".join(cells[1:])):
            out.setdefault(int(u), "U" + m.group(1))
    return out


def md_to_jira(lines, feat):
    """Đổi một đoạn Markdown của PRD sang các dòng cú pháp Jira: mã đầy đủ, gạch đầu dòng •, bảng thành dòng."""
    out, fence = [], False
    for k, raw in enumerate(lines):
        st = re.sub(r"<br\s*/?>", " \\\\ ", re.sub(r"<!--.*?-->", "", raw)).strip()
        if st.startswith(("```", "~~~")):
            if not fence:
                out.append("(Sơ đồ hoặc khối mã: xem trong PRD)")
            fence = not fence
            continue
        if fence or not st:
            continue
        if st.startswith("|"):
            cells = split_cells(st)
            if is_sep_row(cells):
                continue
            cells = [c for c in (x.strip() for x in cells) if c]
            if not cells:
                continue
            nxt = lines[k + 1].strip() if k + 1 < len(lines) else ""
            head = nxt.startswith("|") and is_sep_row(split_cells(nxt))
            st = ("*%s*" if head else "• %s") % " · ".join(clean(c) for c in cells)
        elif re.match(r"#{1,6}\s", st):
            st = "*%s*" % clean(re.sub(r"^#{1,6}\s*", "", st))
        else:
            st = re.sub(r"^[-*+]\s+", "• ", st)
            st = re.sub(r"\*\*(.+?)\*\*", "\x02\\1\x02", st)
            st = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", st)
            st = st.replace("\x02", "*").replace("`", "")
        st = to_full(st, feat)
        st = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", "\x00\\1|\\2\x01", st)
        st = re.sub(r"([\[\]{}])", r"\\\1", st)
        out.append(st.replace("\x00", "[").replace("\x01", "]"))
    return out


def jira_description(secs, feat, ref):
    parts = []
    for key, title in JIRA_SECTIONS:
        body = md_to_jira(secs.get(key) or [], feat)
        if body and not all("<" in b and ">" in b and len(b) < 80 for b in body):
            parts.append("*%s* \\\\ " % title + " \\\\ ".join(body))
    parts.append("*THAM CHIẾU* \\\\ " + ref)
    text = " \\\\  \\\\ ".join(parts)
    if len(text) > JIRA_DESC_MAX:
        cut = " \\\\  \\\\ (Mô tả dài quá giới hạn của Jira, xem đủ trong PRD) \\\\  \\\\ *THAM CHIẾU* \\\\ " + ref
        text = text[:JIRA_DESC_MAX - len(cut)] + cut
    return text


BR0_DEF = re.compile(r"^\s*(?:[-*+]\s+)?[`*_]*BR-?0\.(\d+)[`*_]*")


def shared_rules(lines):
    """{số n: dòng Markdown} của rule dùng chung BR0.<n> định nghĩa ở PRD mục 4, dạng danh sách hoặc dòng bảng."""
    out = {}
    for ln in lines:
        s_ = ln.strip()
        if s_.startswith("|"):
            cells = [clean(c) for c in split_cells(s_)]
            m = re.fullmatch(r"BR-?0\.(\d+)", cells[0] if cells else "")
            if m:
                out.setdefault(int(m.group(1)), "- `BR0.%s` %s" % (m.group(1), " · ".join(c for c in cells[1:] if c and "<" not in c)))
            continue
        m = BR0_DEF.match(ln)
        if m:
            out.setdefault(int(m.group(1)), ln.rstrip())
    return out


def us_handoff(intent):
    """Đọc PRD và trả mọi thứ cần cho danh sách story: (meta, [story]) hoặc (None, thông báo lỗi)."""
    intent = resolve_intent(intent)
    imd = read(intent / "intent.md")
    if imd is None:
        return None, "Không thấy intent.md trong %s." % intent
    prd_p = stage_file(intent, "prd-generation")
    prd = read(prd_p)
    if prd is None:
        return None, "Chưa có %s, chưa lập được Story List." % rel(prd_p, intent)
    pfm, ifm = frontmatter(prd), frontmatter(imd)
    ifeat, pfeat = intent_feature(intent), valid_feature(pfm.get("feature", ""))
    feat = ifeat or pfeat
    if not feat:
        return None, ("Intent %s chưa có mã tính năng: intent.md và frontmatter prd.md đều thiếu feature. PO cấp mã trước: "
                      "python3 engine/scripts/po-tools.py feature-id --assign %s" % (intent.name, show(intent)))
    lines = prd.splitlines()
    blocks = prd_us_blocks(lines)
    if not blocks:
        return None, "Không thấy khối ## US<n> nào trong %s." % rel(prd_p, intent)
    iname = clean(ifm.get("intent", ""))
    iname = iname if iname and "<" not in iname else intent.name
    ver = clean(pfm.get("version", "")) or "0"
    status = clean(pfm.get("status", "")).lower()
    title = clean(pfm.get("title", "")) or next((clean(re.sub(r"^#\s*(\[PRD\])?", "", l)) for l in lines if l.startswith("# ")), intent.name)
    approved_at = clean(pfm.get("approved_at", ""))
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", approved_at)
    approved_at = "%s/%s/%s" % (m.group(3), m.group(2), m.group(1)) if m else approved_at
    epic, epic_by_unit, epics = jira_epics(imd)
    units = prd_unit_map(lines)
    so = load_state(intent)
    prof = clean(so.fm.get("profile", "")).upper()[:1] if so else ""
    ae = next((e for e in (so.stages if so else []) if e["slug"] == "design-alignment"), None)
    aligned = not (so is not None and prof in ("M", "L")) or (ae is not None and ae["mark"] in "xS")
    ux = read(intent / TEAM_DESIGNS[0][1])
    smap = ux_screen_map(ux) if ux is not None else None
    figma = re.findall(r"https?://[^\s|)\]]*figma[^\s|)\]]*", intent_row(imd, "Figma"))
    issues = prd_open_issues(lines)
    shared0 = shared_rules(lines)
    meta = {"intent": intent, "iname": iname, "feat": feat, "ifeat": ifeat, "pfeat": pfeat, "ver": ver, "status": status,
            "approved": status == "approved", "approved_at": approved_at, "tag": "%s/prd-v%s" % (iname, ver),
            "title": title, "prd_path": show(prd_p), "epic": epic, "epics": epics, "aligned": aligned}
    stories = []
    for b in blocks:
        n = b["num"]
        sid = "US-%s-%02d" % (feat, n)
        blines = lines[b["start"]:b["end"]]
        reasons = []
        if not meta["approved"]:
            reasons.append("PRD chưa duyệt (status %s)" % (status or "trống"))
        if not aligned:
            reasons.append("2.43 Design Alignment chưa duyệt")
        if re.search(r"❓\s*PO\b", "\n".join(blines)):
            reasons.append("US còn ❓PO")
        bacs = [a for a in prd_acs(blines, 0) if a["us"] == n]
        bbrs = {t for t in BR_RE.findall("\n".join(blines)) if int(t[0]) == n}
        if not bacs:
            reasons.append("chưa có AC")
        else:
            refs = set()
            for a in bacs:
                refs |= set(a["brs"])
            miss = sorted(bbrs - refs, key=lambda t: (int(t[1]), t[2]))
            if miss:
                reasons.append("BR chưa có AC: %s" % ", ".join(to_full(br_label(t), feat) for t in miss))
        mine = [it for it in issues if re.search(r"(?<![\w-])US%d\b" % n, it["all"])]
        blk = [it for it in mine if issue_blocks(it)]
        if blk:
            reasons.append("câu chặn còn mở ở Câu hỏi mở: %s" % ", ".join("#" + it["no"] if it["no"] else snippet(it["text"], 40) for it in blk))
        secs = split_us_block(lines, b["start"], b["end"])
        secs["us"] = tidy([l for l in secs["us"] if not PRIORITY_RE.search(l)])  # ưu tiên đã thành cột Priority
        used0 = sorted({int(t[1]) for t in BR_RE.findall("\n".join(blines)) if int(t[0]) == 0})
        if used0:
            secs["br"] = secs["br"] + [""] + [shared0[k] for k in used0 if k in shared0]
        screens = (smap or {}).get(n, [])
        if smap is not None and us_has_ui(secs["ui"]) and not screens:
            reasons.append("giao diện chưa có màn trong ux-design")
        prio, jprio = us_priority("\n".join(blines))
        deps = sorted(set(int(k) for k in re.findall(r"(?<![\w-])US(\d+)\b", "\n".join(secs["pre"])) if int(k) != n))
        unit = units.get(n, "")
        ref = "PRD %s v%s%s, %s · tag %s · US%d trong PRD" % (
            title, ver, (", duyệt ngày " + approved_at) if approved_at else "", meta["prd_path"], meta["tag"], n)
        if screens:
            ref += " · Màn: " + ", ".join(("%s %s" % (to_full(c, feat), nm)).strip() for c, nm in screens)
        if figma:
            ref += " · Figma: " + " · ".join(figma)
        uepic = epic_by_unit.get(int(unit[1:])) if unit else None
        stories.append({"num": n, "sid": sid, "title": clean(b["title"]) or sid, "unit": unit, "epic": uepic or epic,
                        "prio": prio, "jprio": jprio, "deps": deps,
                        "reasons": reasons, "issues": mine, "desc": jira_description(secs, feat, ref)})
    # story phụ thuộc: US nêu ở Pre-Condition chưa đạt vì lý do riêng của nó thì story này cũng chưa giao được
    own = dict((st["num"], [r for r in st["reasons"] if not r.startswith(("PRD chưa duyệt", "2.43 Design Alignment"))]) for st in stories)
    for st in stories:
        bad = [k for k in st["deps"] if own.get(k)]
        if bad:
            st["reasons"].append("phụ thuộc %s chưa đạt" % ", ".join("US-%s-%02d" % (feat, k) for k in bad))
    return meta, stories


def jira_rows(meta, stories):
    key, name, ptype = jira_config()
    rows = []
    for st in stories:
        com = ["Nguồn: PRD v%s%s, tag %s." % (meta["ver"], (" duyệt ngày " + meta["approved_at"]) if meta["approved_at"] else "", meta["tag"]),
               "Điều kiện giao Dev: " + ("đạt." if not st["reasons"] else "chưa đạt, " + "; ".join(st["reasons"]) + ".")]
        if st["issues"]:
            com.append("Câu hỏi còn mở trong PRD:")
            com += ["- %s" % clean(to_full(it["text"], meta["feat"])) for it in st["issues"]]
        com.append("Story point và thứ tự thực hiện: Dev điền.")
        rows.append([key, name, ptype, "Story", st["title"], st["jprio"], st["desc"], st["epic"], meta["feat"], st["sid"],
                     ("%s-%s" % (meta["feat"], st["unit"])) if st["unit"] else "", "\n".join(com)])
    return rows


def jira_csv_text(rows):
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(JIRA_COLS)
    w.writerows(rows)
    return buf.getvalue()


def jira_csv_path(meta):
    return meta["intent"] / "stories" / ("story-list-prd-v%s.csv" % meta["ver"])


def csv_version(p):
    """Khoá sắp xếp file Story List theo phiên bản PRD: v1.10 đứng sau v1.9."""
    m = re.search(r"prd-v(\d+(?:\.\d+)*)", p.name)
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


def stories_cmd(intent, write_out=False, only=None):
    meta, stories = us_handoff(intent)
    if meta is None:
        print(stories)
        return 2
    if only:
        n = us_number(only)
        stories = [s for s in stories if s["num"] == n]
        if not stories:
            print("prd.md không có khối của %s." % only)
            return 2
    key, name, _ = jira_config()
    print("# Story List: %s · PRD v%s (%s) · mã tính năng %s\n" % (meta["intent"].name, meta["ver"], meta["status"] or "chưa ghi status", meta["feat"]))
    if meta["ifeat"] and meta["pfeat"] and meta["ifeat"] != meta["pfeat"]:
        print("Lưu ý: intent.md ghi feature %s, prd.md ghi %s. Dùng %s; sửa frontmatter prd.md cho khớp.\n" % (meta["ifeat"], meta["pfeat"], meta["ifeat"]))
    notes = []
    if not key or not name:
        notes.append("domain.md chưa có jira_project_key hoặc jira_project_name ở frontmatter, cột Project key và Project name sẽ trống.")
    if not meta["epic"]:
        notes.append("intent.md chưa có mã Epic ở dòng Jira Epic, cột Epic Link sẽ trống.")
    elif len(meta["epics"]) > 1:
        notes.append("intent.md có nhiều Epic (%s). Dòng nào không ghi 'U<n>: <Epic>' thì dùng %s; sửa ở intent.md hoặc trong CSV." % (", ".join(meta["epics"]), meta["epic"]))
    for x in notes:
        print("Lưu ý: " + x)
    if notes:
        print()
    print(md_table(["Story", "Tên", "Ưu tiên", "Unit", "Epic", "Giao Dev", "Lý do"],
                   [(s["sid"], s["title"], s["prio"] or "-", s["unit"] or "-", s["epic"] or "-", "đạt" if not s["reasons"] else "chưa đạt",
                     "; ".join(s["reasons"]) or "-") for s in stories]))
    noprio = [s["sid"] for s in stories if not s["prio"]]
    if noprio:
        print("\nLưu ý: %d story chưa có dòng Ưu tiên trong PRD, cột Priority để trống: %s." % (len(noprio), ", ".join(noprio)))
    rows = jira_rows(meta, stories)
    path = jira_csv_path(meta)
    prev = sorted((p for p in (meta["intent"] / "stories").glob("story-list-prd-v*.csv") if p != path), key=csv_version) if (meta["intent"] / "stories").is_dir() else []
    if prev:
        import csv
        old = {}
        with open(prev[-1], encoding="utf-8", newline="") as f:
            data = list(csv.reader(f))
        hdr = data[0] if data else []
        if "Labels" in hdr and "Description" in hdr:
            li, di = hdr.index("Labels") + 1, hdr.index("Description")
            for r in data[1:]:
                if len(r) > max(li, di):
                    old[r[li]] = r[di]
        si, di = JIRA_COLS.index("Labels") + 1, JIRA_COLS.index("Description")
        changed = [r[si] for r in rows if r[si] in old and old[r[si]] != r[di]]
        added = [r[si] for r in rows if r[si] not in old]
        print("\nSo với %s: đổi %s; mới %s. Story đã import thì sửa trên Jira theo danh sách này." % (
            prev[-1].name, ", ".join(changed) or "không có", ", ".join(added) or "không có"))
        removed = sorted(k for k in old if k and k not in {r[si] for r in rows})
        if removed:
            print("Story có ở bản trước, không còn trong PRD: %s. Đóng hoặc huỷ trên Jira, không xoá." % ", ".join(removed))
    if not write_out:
        print("\nChạy thử, chưa ghi gì. Thêm --write để ghi %s." % rel(path, meta["intent"]))
        return 0
    if not meta["approved"]:
        print("\nChỉ ghi Story List từ PRD đã duyệt. PRD đang %s." % (meta["status"] or "chưa ghi status"))
        return 2
    if not meta["aligned"]:
        print("\nChỉ ghi Story List sau khi 2.43 Design Alignment được duyệt: các team đã thiết kế từ PRD và đã chốt trên Decision Brief.")
        return 2
    write(path, jira_csv_text(rows))
    print("\nĐã ghi %s, %d story. Import lên Jira bằng chức năng import CSV." % (rel(path, meta["intent"]), len(rows)))
    return 0


def dor(intent, story=None):
    meta, stories = us_handoff(intent)
    if meta is None:
        print(stories)
        return 2
    if story:
        n = us_number(story)
        stories = [s for s in stories if s["num"] == n]
        if not stories:
            print("prd.md không có khối của %s." % story)
            return 2
    npass = sum(1 for s in stories if not s["reasons"])
    print("# Điều kiện giao Dev: %s · PRD v%s\n" % (meta["intent"].name, meta["ver"]))
    print(md_table(["Story", "Đạt?", "Lý do"], [(s["sid"], "Đạt" if not s["reasons"] else "Chưa đạt", "; ".join(s["reasons"]) or "-") for s in stories]))
    print("\nKết luận: %d/%d story đạt điều kiện giao Dev." % (npass, len(stories)))
    return 0 if npass == len(stories) else 1


# ================================================================ manifest
MANIFEST_DIRS = ("engine", ".claude/commands", ".claude/agents")
MANIFEST_FILES = ("AGENTS.md", "CLAUDE.md", "GLOSSARY.md", "README.md", "USER-GUIDE.md", "DOMAIN-SETUP.md", "VERSION", "CHANGELOG.md")


def engine_files():
    found = set()
    rc, out = git("ls-files", "-z", "--", *(list(MANIFEST_DIRS) + list(MANIFEST_FILES)))
    if rc == 0:
        found.update(p for p in out.split("\0") if p and (REPO / p).is_file())
    for d in MANIFEST_DIRS:
        for root, dirs, files in os.walk(str(REPO / d)):
            dirs[:] = [x for x in dirs if x not in ("__pycache__", ".git")]
            for fn in files:
                if fn == ".DS_Store" or fn.endswith(".pyc"):
                    continue
                found.add((Path(root) / fn).relative_to(REPO).as_posix())
    found.update(f for f in MANIFEST_FILES if (REPO / f).is_file())
    return sorted(p for p in found if p != "engine/MANIFEST.txt")


def sha256(path):
    h = hashlib.sha256()
    with open(str(path), "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest(write_out=False):
    files = engine_files()
    ver = (read(REPO / "VERSION") or "").strip() or "chưa có file VERSION"
    lines = ["# PO-Workflow engine manifest · VERSION %s · %d file · sinh ngày %s bằng po-tools.py manifest" % (ver, len(files), today().isoformat())]
    lines += ["%s  %s" % (sha256(REPO / p), p) for p in files]
    text = "\n".join(lines) + "\n"
    if write_out:
        write(MANIFEST, text)
        print("Đã ghi %s, %d file." % (rel(MANIFEST, REPO), len(files)))
    else:
        print(text, end="")
    return 0


def engine_check(strict=False):
    text = read(MANIFEST)
    if text is None:
        print("Chưa có engine/MANIFEST.txt. Chạy: python3 engine/scripts/po-tools.py manifest --write")
        return 2
    want = {}
    for ln in text.splitlines():
        if ln.startswith("#") or not ln.strip():
            continue
        parts = ln.split("  ", 1)
        if len(parts) == 2:
            want[parts[1].strip()] = parts[0].strip()
    head = next((l for l in text.splitlines() if l.startswith("#")), "")
    have = engine_files()
    modified = [p for p in have if p in want and sha256(REPO / p) != want[p]]
    missing = [p for p in want if not (REPO / p).is_file()]
    new = [p for p in have if p not in want]
    print("# Engine so với manifest\n")
    print(head.lstrip("# "))
    print("")
    for title, items in (("Bị sửa", modified), ("Mất", missing), ("Mới, chưa có trong manifest", new)):
        print("## %s (%d)" % (title, len(items)))
        for p in items:
            print("- " + p)
        print("")
    if modified or missing or (strict and new):
        print("Kết luận: engine khác bản manifest. Sửa engine là việc của người giữ engine; sửa xong chạy selftest, "
              "manifest --write và ghi CHANGELOG. VERSION chỉ tăng khi phát hành, xem AGENTS.md mục Sửa engine.")
        return 1
    print("Kết luận: engine khớp manifest%s." % (", có file mới chưa ghi vào manifest; --strict coi đây là lỗi" if new else ""))
    return 0


# ================================================================ doctor
def resolve_ref(token):
    t = token.split("§")[0].strip().rstrip(",;")
    if not t:
        return None, None
    if "/" in t:
        return t, data_path(t).exists()
    for base in ("engine/knowledge", "domain/", "engine/templates", "engine/verification", "engine/protocol", ""):
        if (data_path(base) / t if base else REPO / t).exists():
            return t, True
    return t, False


def doctor():
    rows = []

    def add(name, level, detail, fix="-"):
        rows.append((name, level, detail, fix))

    name = git_user()
    add("git user.name", "Đạt" if name else "Lỗi", name or "chưa đặt, approve sẽ ghi người quyết là PO",
        "-" if name else 'git config --global user.name "Họ Tên"')
    pv = "%d.%d.%d" % sys.version_info[:3]
    add("Python từ 3.9", "Đạt" if sys.version_info >= (3, 9) else "Lỗi", pv, "-" if sys.version_info >= (3, 9) else "Cài Python 3.9 trở lên")
    cwd = Path.cwd()
    ok = (cwd / "AGENTS.md").exists() and (cwd / "engine").is_dir()
    add("Chạy từ gốc repo", "Đạt" if ok else "Lỗi", str(cwd), "-" if ok else 'cd "%s"' % REPO)
    sj = read(REPO / ".claude" / "settings.json") or ""
    if "po-hook.py" in sj:
        hb = ROOT / ".po" / "hooks" / "UserPromptSubmit.last"
        add("Hook ghi lượt PO", "Đạt" if hb.exists() else "Cảnh báo",
            ("chạy lần cuối %s" % (read(hb) or "").strip()) if hb.exists() else "chưa chạy lần nào trên máy này, approve sẽ từ chối",
            "-" if hb.exists() else "Mở Claude Code ở gốc repo và gõ một câu; kiểm python3 chạy được, xem .claude/settings.json")
    rc, out = git("status", "--porcelain", "--", "intents", "memory")
    if rc != 0:
        add("Thay đổi chưa commit ở intents/, memory/", "Cảnh báo", "không chạy được git status", "Kiểm lại git")
    else:
        ch = [l for l in out.splitlines() if l.strip()]
        add("Thay đổi chưa commit ở intents/, memory/", "Cảnh báo" if ch else "Đạt",
            ("%d file: %s" % (len(ch), ", ".join(l[3:] for l in ch[:3]) + (", ..." if len(ch) > 3 else ""))) if ch else "không có",
            "Commit và push để người khác thấy" if ch else "-")
    # repo engine chưa có domain là trạng thái hợp lệ: báo một dòng, bỏ các kiểm phụ thuộc domain
    no_domain = not DOMAIN_MD.exists()
    if no_domain:
        add("Domain pack", "Cảnh báo", "chưa có domain/domain.md; đây là repo engine hoặc sản phẩm chưa dựng domain",
            "Tạo repo cho sản phẩm từ repo này, chạy /new-domain theo DOMAIN-SETUP.md")
    srcs = [] if no_domain else live_sources()
    stale = [] if no_domain else stale_sources()
    nodate = [s for s in srcs if s["kind"] == "sống" and not s["date"]]
    if no_domain:
        pass
    elif not srcs:
        add("Nguồn sống trong domain.md mục 2", "Cảnh báo", "không đọc được bảng nguồn", "Kiểm bảng mục 2 của domain.md")
    else:
        lvl = "Cảnh báo" if stale or nodate else "Đạt"
        det = "; ".join(["%s đối chiếu %s" % (s["name"], s["date_txt"]) for s in stale] + ["%s chưa có ngày" % s["name"] for s in nodate]) or \
            "%d nguồn sống, đều đối chiếu trong %d ngày" % (sum(1 for s in srcs if s["kind"] == "sống"), STALE_DAYS)
        add("Nguồn sống quá %d ngày" % STALE_DAYS, lvl, det, "Đọc lại nguồn, sửa KB và ngày đối chiếu" if lvl != "Đạt" else "-")
    dups = duplicate_features([INTENTS])
    add("Mã tính năng trùng", "Lỗi" if dups else "Đạt",
        "; ".join("%s ở %s" % (fid, ", ".join(i.name for i in its)) for fid, its in dups) or "không có",
        "PO đến sau đổi số bằng feature-id --next, sửa feature trong intent.md và prd.md" if dups else "-")
    nofeat = [p.name for p in sorted(INTENTS.iterdir()) if p.is_dir() and (p / "intent.md").exists()
              and stage_file(p, "prd-generation").exists() and not intent_feature(p)] if INTENTS.is_dir() else []
    add("Intent có PRD chưa có mã tính năng", "Cảnh báo" if nofeat else "Đạt", ", ".join(nofeat) or "không có",
        "python3 engine/scripts/po-tools.py feature-id --assign intents/<intent>" if nofeat else "-")
    if not no_domain and not domain_code():
        add("Khoá code trong domain.md", "Cảnh báo", "chưa có, feature-id không cấp được mã", "Thêm code: <mã sản phẩm> vào frontmatter domain/domain.md")
    jk, jn, jt = jira_config()
    if not no_domain:
        add("Dự án Jira trong domain.md", "Đạt" if jk and jn else "Cảnh báo", "%s, %s, %s" % (jk, jn, jt) if jk and jn else "thiếu jira_project_key hoặc jira_project_name, Story List sẽ để trống cột Project",
            "-" if jk and jn else "Thêm jira_project_key, jira_project_name vào frontmatter domain/domain.md, xem DOMAIN-SETUP.md mục 5")
    dl = (read(DOMAIN_MD) or "").splitlines()
    nums = set(int(m.group(1)) for _, lvl, t in headings(dl) if lvl == 2 for m in [re.match(r"(\d+)\.", clean(t))] if m)
    miss = [str(n) for n in range(1, 7) if n not in nums]
    if not no_domain:
        add("domain.md đủ mục 1 đến 6", "Lỗi" if miss or not dl else "Đạt",
            ("thiếu mục %s" % ", ".join(miss)) if dl and miss else ("không thấy domain/domain.md" if not dl else "đủ"),
            "Viết theo DOMAIN-SETUP.md" if miss or not dl else "-")
    if not no_domain:
        # KB tối thiểu và bản đồ KB, theo engine/standards/domain-kb.md mục 7
        dd = ROOT / "domain"
        miss_kb = [n for n in KB_MIN if not (dd / n).exists()]
        add("KB tối thiểu theo domain-kb.md", "Cảnh báo" if miss_kb else "Đạt", ("thiếu " + ", ".join(miss_kb)) if miss_kb else "đủ",
            "Dựng từ engine/templates/domain/, xem engine/standards/domain-kb.md mục 7" if miss_kb else "-")
        rng = section_lines(dl, lambda t: "bản đồ kb" in t.lower())
        mapped = []
        if rng:
            for t in parse_tables(dl, rng[0], rng[1]):
                for cells, _ in t["rows"]:
                    mapped += [x for x in backticks(cell(cells, 0)) if x.endswith(".md") and "<" not in x]
        lost = [x for x in mapped if not (dd / x).exists()]
        add("File trong bản đồ KB", "Cảnh báo" if lost else "Đạt", ("không có " + ", ".join(lost)) if lost else "%d file đều có" % len(mapped),
            "Tạo file hoặc sửa domain.md mục 3" if lost else "-")
    kb = [show(p) for p in sorted((ROOT / "domain").rglob("*.md")) if "chưa viết" in (read(p) or "")] if (ROOT / "domain").is_dir() else []
    add("KB còn chữ 'chưa viết'", "Cảnh báo" if kb else "Đạt", ", ".join(kb) or "không có", "Viết nốt KB hoặc ghi vùng chưa phủ" if kb else "-")
    S = load_stages()
    bad = []
    for f in sorted(STAGES_DIR.glob("*.md")):
        st = parse_stage_file(f)
        for key in ("Template", "Checklist", "Knowledge"):
            for tok in backticks(st.meta.get(key, "")):
                if not re.search(r"\.md\b|/", tok):
                    continue
                t, ok = resolve_ref(tok)
                if no_domain and (tok.startswith("domain/") or "/" not in tok):
                    continue  # file của domain, chưa có ở repo engine
                if t and not ok:
                    bad.append("%s %s: %s" % (f.name, key, t))
    add("Đường dẫn Template, Checklist, Knowledge", "Lỗi" if bad else "Đạt", "; ".join(bad) or "mọi đường dẫn đều có", "Sửa bảng metadata của file stage" if bad else "-")
    nd = [n for n in S.notes if "Thư mục" in n]
    add("Bảng metadata stage", "Lỗi" if S.warnings else ("Cảnh báo" if S.notes else "Đạt"),
        "; ".join(S.warnings + S.notes)[:400] or "%d stage đọc được" % len(S.list),
        "Thêm dòng Thư mục và Lệch so với AWS vào bảng của file stage" if nd else ("Sửa file stage" if S.warnings else "-"))
    dfm = frontmatter(read(DOMAIN_MD))
    names = [x.strip() for x in [dfm.get("product", ""), dfm.get("company", "")] + dfm.get("names", "").strip("[]").split(",") if x.strip().strip("\"'")]
    names = list(dict.fromkeys(x.strip("\"'") for x in names))
    hits = []
    if names:
        rx = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(re.escape(n) for n in names) + r")(?![A-Za-z0-9])", re.I)
        targets = [p for p in engine_files() if (p.startswith(("engine/", ".claude/commands/", ".claude/agents/")) or p == "AGENTS.md")
                   and not p.startswith("engine/tests/")]
        for p in targets:
            text = read(REPO / p)
            if text is None:
                continue
            for i, ln in enumerate(text.splitlines()):
                m = rx.search(ln)
                if m:
                    hits.append("%s:%d (%s)" % (p, i + 1, m.group(1)))
    add("Tên sản phẩm trong engine", "Lỗi" if hits else "Đạt",
        ("%d chỗ: %s" % (len(hits), ", ".join(hits[:5]) + (", ..." if len(hits) > 5 else ""))) if hits else ("không có %s" % ", ".join(names) if names else "domain.md không có product, company"),
        "Chuyển dữ kiện sản phẩm vào domain/" if hits else "-")
    print("# Doctor\n")
    print(md_table(["Kiểm tra", "Kết quả", "Chi tiết", "Cách sửa"], rows))
    nerr = sum(1 for r in rows if r[1] == "Lỗi")
    nwarn = sum(1 for r in rows if r[1] == "Cảnh báo")
    print("\nKết luận: %d Lỗi, %d Cảnh báo." % (nerr, nwarn))
    return 1 if nerr else 0


# ================================================================ selftest
COMMANDS = ("status", "next", "check", "trace", "approve", "review-start", "archive", "replay", "feature-id",
            "stories", "dor", "index", "migrate", "doctor", "manifest", "engine-check", "selftest")
# Lệnh không có ca fixture, kèm lý do. Mọi lệnh khác phải có ít nhất một ca trong engine/tests/fixtures.
UNTESTED = {"selftest": "chính là bộ chạy các ca",
            "manifest": "đọc file engine của repo; CI chạy engine-check --strict trên repo thật ở mỗi lần push",
            "engine-check": "như manifest"}
# Lệnh không nhận thư mục intent: bộ chạy không chèn đường dẫn fixture vào sau tên lệnh.
NO_INTENT = ("index", "doctor", "manifest", "engine-check", "selftest")
HOOK_SCRIPT = REPO / "engine" / "scripts" / "po-hook.py"
COMPAT = ("chỉ chép engine", "chép engine và chạy migrate", "phải sửa intent bằng tay")


def parse_expected(path, errs=None):
    """Ca kiểm của một fixture. Dòng không nhận ra và ca không có điều kiện nào đều ghi vào errs."""
    errs = [] if errs is None else errs
    name = "%s/%s" % (Path(path).parent.name, Path(path).name)
    cases, cur = [], None
    for k, ln in enumerate((read(path) or "").splitlines(), 1):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        m = re.fullmatch(r"\[(.+)\]", s)
        if m:
            parts = shlex.split(m.group(1))
            cur = {"cmd": parts[0], "args": parts[1:], "exit": None, "has": [], "not": [], "files": [], "label": m.group(1)}
            cases.append(cur)
            continue
        if cur is None:
            errs.append("%s:%d dòng nằm ngoài ca nào: %s" % (name, k, s[:60]))
            continue
        if s.startswith("mã thoát:"):
            v = s.split(":", 1)[1].strip()
            if v.isdigit():
                cur["exit"] = int(v)
            else:
                errs.append("%s:%d mã thoát không phải số: %s" % (name, k, v))
        elif s.startswith("không có:"):
            cur["not"].append(s.split(":", 1)[1].strip().replace("\\n", "\n"))
        elif s.startswith("có:"):
            cur["has"].append(s.split(":", 1)[1].strip().replace("\\n", "\n"))
        elif s.startswith("tệp "):
            fm_ = re.match(r"tệp\s+(\S+)\s+(có|không có|giữ nguyên mục):\s*(.*)$", s)
            if fm_:
                kind = {"có": "has", "không có": "not", "giữ nguyên mục": "keep"}[fm_.group(2)]
                cur["files"].append((fm_.group(1), kind, fm_.group(3).replace("\\n", "\n")))
            else:
                errs.append("%s:%d dòng tệp sai cú pháp: %s" % (name, k, s[:60]))
        else:
            errs.append("%s:%d dòng không nhận ra: %s" % (name, k, s[:60]))
    for c in cases:
        if c["exit"] is None and not (c["has"] or c["not"] or c["files"]):
            errs.append("%s: ca [%s] không có điều kiện nào, luôn đạt" % (name, c["label"]))
    return cases


def file_errors(orig_dir, work_dir, checks, root=None):
    errs = []
    for path, kind, val in checks:
        txt = read(Path(root) / path[len("{root}/"):]) if root and path.startswith("{root}/") else read(Path(work_dir) / path)
        if kind == "has" and (txt is None or val not in txt):
            errs.append("%s thiếu chuỗi '%s'" % (path, val) if txt is not None else "không có tệp %s" % path)
        elif kind == "not" and txt is not None and val in txt:
            errs.append("%s có chuỗi không được có '%s'" % (path, val))
        elif kind == "keep":
            orig = read(Path(orig_dir) / path)
            for n in val.split():
                if story_section_text(orig, n) != story_section_text(txt, n):
                    errs.append("%s: mục %s đã bị đổi" % (path, n))
    return errs


def doc_files():
    out = []
    for p in sorted(REPO.rglob("*.md")):
        r = p.relative_to(REPO).as_posix()
        if r.startswith(("intents/", "engine/tests/", ".git/", "node_modules/", ".po/")) or "/archive/" in r:
            continue
        out.append((r, p))
    return out


def doc_sync_problems():
    """Tài liệu khớp script và engine: lệnh po-tools.py nhắc tới có thật, đường dẫn engine/ có thật,
    bảng stage ở README mục 3.2 đủ mã và tên của engine/stages."""
    out = []
    for r, p in doc_files():
        text = read(p) or ""
        for k, ln in enumerate(text.splitlines(), 1):
            for m in re.finditer(r"po-tools\.py\s+([a-z][a-z-]*)(?!\w)", ln):
                if m.group(1) not in COMMANDS:
                    out.append("%s:%d nhắc lệnh không có: po-tools.py %s" % (r, k, m.group(1)))
            for m in re.finditer(r"`(engine/[^`\s]+)`", ln):
                t = m.group(1).split("#")[0].rstrip(".,:;)")
                if any(ch in t for ch in "<>*{}") or "..." in t:
                    continue
                if not (REPO / t).exists():
                    out.append("%s:%d đường dẫn không có: %s" % (r, k, t))
    readme = read(REPO / "README.md") or ""
    for st in load_stages().list:
        if "| %s %s |" % (st.code, st.name) not in readme:
            out.append("README.md mục 3.2 thiếu dòng của stage %s %s" % (st.code, st.name))
    return out


def release_problems():
    """VERSION khớp mục mới nhất của CHANGELOG và đầu MANIFEST; mỗi bản từ 2.1.0 có mục Nâng cấp và dòng Tương thích."""
    out = []
    ver = (read(REPO / "VERSION") or "").strip()
    cl = read(REPO / "CHANGELOG.md") or ""
    heads = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", cl, re.M)
    if not heads:
        return ["CHANGELOG.md không có mục dạng '## [X.Y.Z]'"]
    if heads[0] != ver:
        out.append("VERSION ghi %s, mục mới nhất của CHANGELOG là %s" % (ver or "trống", heads[0]))
    dup = sorted(set(h for h in heads if heads.count(h) > 1))
    if dup:
        out.append("CHANGELOG có mục trùng: %s" % ", ".join(dup))
    mh = re.search(r"VERSION (\S+)", (read(MANIFEST) or "").split("\n", 1)[0])
    if mh and mh.group(1) != ver:
        out.append("MANIFEST.txt sinh với VERSION %s, VERSION hiện là %s: chạy manifest --write" % (mh.group(1), ver))
    parts = re.split(r"^## \[", cl, flags=re.M)[1:]
    for part in parts:
        v = part.split("]", 1)[0]
        if ver_tuple(v) < (2, 1, 0):
            continue
        if "### Nâng cấp" not in part:
            out.append("CHANGELOG %s thiếu mục ### Nâng cấp" % v)
        m = re.search(r"^Tương thích: (.+?)\.?\s*$", part, re.M)
        if not m or m.group(1) not in COMPAT:
            out.append("CHANGELOG %s thiếu dòng 'Tương thích: <%s>'" % (v, " | ".join(COMPAT)))
    return out


def selftest():
    fails, warns, passed = [], [], 0
    S = load_stages()
    files = sorted(STAGES_DIR.glob("*.md"))
    if not files:
        fails.append("engine/stages không có file stage nào")
    for f in files:
        st = parse_stage_file(f)
        hard = [p for p in st.problems if "Thư mục" not in p]
        if hard:
            fails.append("%s: %s" % (f.name, "; ".join(hard)))
        if not st.templates:
            fails.append("%s: không có dòng Template" % f.name)
        if not st.checklist:
            fails.append("%s: không có dòng Checklist" % f.name)
        for p in st.templates + st.checklist:
            t, ok = resolve_ref(p)
            if t and not ok:
                fails.append("%s: đường dẫn không có: %s" % (f.name, t))
        if not st.has_dir_row:
            warns.append("%s chưa có dòng Thư mục, đang suy từ Produces: %s" % (f.name, st.dir))
        if st.aws_diff is None:
            warns.append("%s chưa có dòng Lệch so với AWS" % f.name)
    if not S.reviewers:
        fails.append("profiles.md: không đọc được cột Reviewer của bảng profile")
    for prof, codes in sorted(S.reviewers.items()):
        for c in codes:
            stg = S.by_code.get(c)
            if stg is None:
                fails.append("profiles.md: profile %s bật reviewer ở %s nhưng không có file stage mã này" % (prof, c))
                continue
            if "ai-reviewer" not in stg.reviewer:
                fails.append("%s.md: profiles.md bật reviewer ở profile %s, nhưng dòng Reviewer ghi '%s'" % (stg.slug, prof, stg.reviewer))
                continue
            m = re.search(r"ai-reviewer\s+ở\s+([SML](?:\s*,\s*[SML])*)", stg.reviewer)
            if m and prof not in re.findall(r"[SML]", m.group(1)):
                fails.append("%s.md: Reviewer '%s' không gồm profile %s mà profiles.md bật" % (stg.slug, stg.reviewer, prof))
    fx_dirs = sorted(p for p in FIXTURES.iterdir() if p.is_dir()) if FIXTURES.is_dir() else []
    if not fx_dirs:
        fails.append("Không có fixture nào trong %s" % rel(FIXTURES, REPO))
    if not (TEST_ROOT / "domain" / "domain.md").exists():
        fails.append("Thiếu %s: domain dùng chung cho mọi fixture" % rel(TEST_ROOT / "domain" / "domain.md", REPO))
    covered = set()
    for fx in fx_dirs:
        exp = fx / "expected.txt"
        if not exp.exists():
            fails.append("%s: thiếu expected.txt" % fx.name)
            continue
        perr = []
        cases = parse_expected(exp, perr)
        fails += perr
        if not cases:
            fails.append("%s: expected.txt không có ca nào" % fx.name)
            continue
        covered |= set(c["cmd"] for c in cases)
        # mỗi fixture chạy trên gốc dữ liệu tạm: domain dùng chung ở engine/tests/root, cộng _root/ của fixture,
        # fixture nằm ở intents/<tên>; lệnh ghi không bao giờ sửa fixture thật hay dữ liệu của repo
        tmp = Path(tempfile.mkdtemp(prefix="po-selftest-"))
        try:
            root = tmp / "root"
            shutil.copytree(str(TEST_ROOT), str(root))
            if (fx / "_root").is_dir():
                shutil.copytree(str(fx / "_root"), str(root), dirs_exist_ok=True)
            work = root / "intents" / fx.name
            shutil.copytree(str(fx), str(work), ignore=shutil.ignore_patterns("_root", "expected.txt"))
            env = dict(os.environ, PO_TOOLS_ROOT=str(root), PO_TOOLS_TODAY=TEST_TODAY)

            def sub(a):
                return a.replace("{root}", str(root)).replace("{intent}", str(work))
            for c in cases:
                inp = None
                if c["cmd"] == "@hook":
                    argv = [sys.executable, str(HOOK_SCRIPT)]
                    inp = sub(read(work / c["args"][0]) or "").encode("utf-8")
                else:
                    args = [sub(a) for a in c["args"]]
                    if c["cmd"] not in NO_INTENT and not any("{root}" in a or "{intent}" in a for a in c["args"]):
                        args = [str(work)] + args
                    argv = [sys.executable, str(SCRIPT), c["cmd"]] + args
                r = subprocess.run(argv, cwd=str(REPO), env=env, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                out = r.stdout.decode("utf-8", "replace")
                errs = []
                if c["exit"] is not None and r.returncode != c["exit"]:
                    errs.append("mã thoát %d, cần %d" % (r.returncode, c["exit"]))
                errs += ["thiếu chuỗi '%s'" % h for h in c["has"] if h not in out]
                errs += ["có chuỗi không được có '%s'" % h for h in c["not"] if h in out]
                errs += file_errors(fx, work, c["files"], root)
                if errs:
                    fails.append("%s [%s]: %s" % (fx.name, c["label"], "; ".join(errs)))
                else:
                    passed += 1
        finally:
            shutil.rmtree(str(tmp), ignore_errors=True)
    for cmd in COMMANDS:
        if cmd not in covered and cmd not in UNTESTED:
            fails.append("Lệnh %s chưa có ca nào trong engine/tests/fixtures. Thêm ca, hoặc ghi lý do vào UNTESTED" % cmd)
    fails += ["Ca dùng lệnh không có: %s" % x for x in sorted(covered) if x not in COMMANDS and x != "@hook"]
    fails += doc_sync_problems()
    fails += release_problems()
    print("# Selftest\n")
    print("Ca fixture đạt: %d" % passed)
    print("\n## Lỗi (%d)" % len(fails))
    for x in fails:
        print("- " + x)
    print("\n## Cảnh báo (%d)" % len(warns))
    for x in warns:
        print("- " + x)
    print("\nKết luận: %s." % ("Không đạt" if fails else "Đạt"))
    return 1 if fails else 0


# ================================================================ migrate
MIG_PATHS = [
    (".claude/knowledge/domain/", "domain/"), (".claude/knowledge/domain", "domain"),
    (".claude/knowledge/product/", "engine/knowledge/"), (".claude/knowledge/product", "engine/knowledge"),
    (".claude/intents/", "intents/"), (".claude/intents", "intents"),
    (".claude/memory/team.md", "memory/team.md"), (".claude/memory/", "memory/"),
    (".claude/protocol/", "engine/protocol/"), (".claude/templates/", "engine/templates/"),
    (".claude/verification/", "engine/verification/"), (".claude/scripts/", "engine/scripts/"),
    (".claude/agents/product-lead.md", "engine/agents/ai-reviewer.md"), (".claude/agents/", "engine/agents/"),
]
MIG_HISTORY = ("archive/", "reviews/", "verification/")
MIG_HISTORY_FILES = ("decisions.md", "memory.md", "state.md")
MIG_PROTECT = [("aidlc-product-lead-agent", "\x00A\x00"), ("**Tech lead**", "\x00T\x00"), ("| Lead |", "\x00L\x00"),
               ("`❓BA` đổi thành", "\x00B\x00"), ("❓BA đổi thành", "\x00C\x00"), ("Proto-Unit thành Unit", "\x00P\x00"),
               ("`PU1` thành", "\x00U\x00"), ("product-lead thành", "\x00R\x00")]


def mig_project_map():
    """Tên dự án ở luồng v1 sang thư mục intent, ví dụ Billing sang 261005-billing."""
    out = {}
    if INTENTS.is_dir():
        for d in INTENTS.iterdir():
            m = re.match(r"\d{6}-(.+)$", d.name)
            if d.is_dir() and m:
                out[m.group(1).lower()] = d.name
    return out


def mig_text(text):
    """Chuẩn hoá một file sống của intent: đường dẫn engine 2.1, Unit, PIC, AI Reviewer, ❓PO."""
    pmap = mig_project_map()
    out = []
    for ln in text.splitlines():
        if ln.startswith("migrated-from:") and ".claude/projects/" in ln and "pre-aidlc:" not in ln:
            ln = ln.replace(".claude/projects/", "pre-aidlc:.claude/projects/", 1)
        else:
            def proj(m):
                name, rest = m.group(1), m.group(2) or ""
                slug = pmap.get(name.lower())
                if slug and not rest:
                    return "intents/%s/" % slug
                return "pre-aidlc:.claude/projects/%s/%s" % (name, rest)
            ln = re.sub(r"(?<!pre-aidlc:)\.claude/projects/([A-Za-z0-9_-]+)/([^\s`|)]*)", proj, ln)
        out.append(ln)
    t = "\n".join(out) + ("\n" if text.endswith("\n") else "")
    for a, b in MIG_PATHS:
        t = t.replace(a, b)
    t = re.sub(r"\.claude/commands/([a-z-]+)\.md", lambda m: "engine/%s/%s.md" % (
        "stages" if m.group(1) in stages().by_slug else "commands", m.group(1)), t)
    for a, b in MIG_PROTECT:
        t = t.replace(a, b)
    t = t.replace("giữ tên Unit, tương đương Proto-Unit", "giữ tên Unit, đúng thuật ngữ hiện hành")
    t = t.replace("Proto-Units", "Units").replace("Proto-Unit", "Unit")
    t = re.sub(r"(?<![\w-])PU(\d+)\b", r"U\1", t)
    t = t.replace("❓BA", "❓PO").replace("product-lead", "ai-reviewer").replace("Product Lead", "AI Reviewer")
    for a, b in (("Lead Design, Dev, QA", "Design PIC, Tech PIC, QA PIC"), ("lead Design, Dev, QA", "Design PIC, Tech PIC, QA PIC"),
                 ("lead Design, Tech, QA", "Design PIC, Tech PIC, QA PIC"), ("lead các team", "các PIC"), ("ba lead", "ba PIC"),
                 ("Tech lead", "Tech PIC"), ("Design lead", "Design PIC"), ("QA lead", "QA PIC")):
        t = t.replace(a, b)
    t = re.sub(r"(?<![\w-])lead(?![\w-])", "PIC", t)
    t = re.sub(r"(?<![\w-])Lead(?![\w-])", "PIC", t)
    for a, b in MIG_PROTECT:
        t = t.replace(b, a)
    return t


def mig_live_part(text, name):
    """memory.md: dòng mô tả đầu file lấy theo template. state.md: chuẩn hoá dòng stage chưa duyệt và hai mục
    Current, Versions; giữ nguyên Log và dòng stage đã duyệt hoặc bỏ qua vì đó là lịch sử."""
    lines = text.splitlines()
    if name == "memory.md":
        tpl = (read(REPO / "engine" / "templates" / "memory.md") or "").splitlines()
        head = next((x for x in tpl if x.startswith("Nhật ký quan sát")), None)
        for i, ln in enumerate(lines[:5]):
            if head and ln.startswith("Nhật ký quan sát") and ln != head:
                lines[i] = head
    else:
        sec = ""
        for i, ln in enumerate(lines):
            if ln.startswith("## "):
                sec = ln[3:].strip()
                continue
            live = sec in ("Current", "Versions") or (sec == "Stages" and re.match(r"^- \[[ ?R-]\]", ln))
            if live:
                lines[i] = mig_text(ln).rstrip("\n")
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def mig_alignment(intent, text):
    """Luồng 2.43: bỏ dòng 2.41 hld-brief và dòng hld-brief ở Versions; profile M, L thêm 2.43 design-alignment ngay sau 2.42.
    Intent đã có Epic trên Jira và PRD đã duyệt thì 2.43 ghi [S], vì đã giao Dev trước khi có stage này.
    2.41 đang dở thì Current chuyển sang 2.43. Trả (text mới, việc, [(file HLD Brief, đích trong archive)])."""
    lines = (text or "").splitlines()
    plan, moves = [], []
    hld = [i for i, ln in enumerate(lines) if re.match(r"^- \[.\] 2\.41 hld-brief\b", ln)]
    was_open = any(re.match(r"^- \[[-?R]\]", lines[i]) for i in hld)
    for i in reversed(hld):
        plan.append(("bỏ stage 2.41 hld-brief", "state.md", lines[i][:6]))
        del lines[i]
    vrows = [i for i, ln in enumerate(lines) if re.match(r"^\|\s*hld-brief\s*\|", ln)]
    for i in reversed(vrows):
        del lines[i]
    prof = clean(frontmatter(text).get("profile", "")).upper()[:1]
    if prof in ("M", "L") and not any(re.match(r"^- \[.\] 2\.43 design-alignment\b", ln) for ln in lines):
        k = next((i for i, ln in enumerate(lines) if re.match(r"^- \[.\] 2\.42 prd-generation\b", ln)), None)
        if k is not None:
            handed = lines[k].startswith("- [x]") and bool(JIRA_KEY.search(intent_row(read(Path(intent) / "intent.md") or "", "Jira Epic")))
            new = ("- [S] 2.43 design-alignment · intent đã có Epic trên Jira và đã giao Dev trước khi có stage này" if handed
                   else "- [ ] 2.43 design-alignment")
            lines.insert(k + 1, new)
            plan.append(("thêm stage 2.43 design-alignment", "state.md", "bỏ qua, đã giao Dev" if handed else "chưa làm"))
    if was_open:
        set_current(lines, "Stage", "2.43 design-alignment: chờ Design PIC, Tech PIC, QA PIC viết file thiết kế từ PRD đã duyệt")
        set_current(lines, "Next action", "Tạo ux-design.md, tech-design.md, test-design.md từ template theo engine/stages/design-alignment.md; "
                                          "gửi ba PIC đường dẫn PRD đã duyệt kèm hạn")
        plan.append(("đổi Current sang 2.43", "state.md", ""))
    d = Path(intent) / "inception" / "hld-brief"
    if hld and d.is_dir():
        for f in sorted(d.glob("*.md")):
            moves.append((f, Path(intent) / "archive" / "hld-brief" / ("%s-luong-cu-%s.md" % (f.stem, today().strftime("%Y%m%d")))))
    out = "\n".join(lines) + ("\n" if (text or "").endswith("\n") else "")
    return out, plan, moves


def mig_questions_v1(text, intent_name, code):
    """File câu hỏi luồng v1 (### `OQ-NN` — tiêu đề ... **Blocks:** Yes, bảng nhóm không chặn) sang dạng ## Q<n>.
    Giữ nguyên nội dung từng câu; mã cũ OQ-NN đứng trong tiêu đề. Trả về None nếu không nhận ra định dạng."""
    if re.search(r"^##\s+Q\d+\b", text, re.M) or not re.search(r"^###\s+`?OQ-\d+", text, re.M):
        return None
    lines = text.splitlines()
    owners = {}
    for t in parse_tables(lines):
        h = t["header"]
        oc = col(h, "Owner")
        if oc is None:
            continue
        for cells, _ in t["rows"]:
            m = re.search(r"OQ-\d+", cell(cells, 0))
            if m:
                owners[m.group(0)] = clean(cell(cells, oc)) or "PO"
    out, k, i = [], 0, 0
    total = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^###\s+`?(OQ-\d+)`?\s*[—-]\s*(.+)$", ln)
        if m:
            k += 1
            oq, title = m.group(1), m.group(2).strip()
            out.append("## Q%d. [%s] %s · %s" % (k, owners.get(oq, "PO"), oq, title))
            j = i + 1
            body = []
            while j < len(lines) and not re.match(r"^#{2,3}\s", lines[j]):
                body.append(lines[j])
                j += 1
            while body and (not body[-1].strip() or body[-1].strip() == "---"):
                body.pop()
            blocking = any(re.match(r"^\*\*Blocks:?\*\*:?\s*Yes", b.strip(), re.I) for b in body)
            body = [b for b in body if not re.match(r"^\*\*Blocks:?\*\*", b.strip(), re.I)]
            out.extend(body)
            out += ["Chặn: %s" % ("có" if blocking else "không"), "[Answer]:", ""]
            total += 1
            i = j
            continue
        # bảng câu không chặn ở luồng v1: mỗi dòng OQ thành một câu
        if ln.strip().startswith("|") and i + 1 < len(lines) and is_sep_row(split_cells(lines[i + 1].strip())):
            h = split_cells(ln.strip())
            qc, wc, pc, oc, bc = col(h, "Câu hỏi"), col(h, "Vì sao"), col(h, "Đề xuất"), col(h, "Owner"), col(h, "Blocks")
            j = i + 2
            rows = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(split_cells(lines[j].strip()))
                j += 1
            if qc is not None and rows and all(re.search(r"OQ-\d+", cell(r, 0)) for r in rows):
                # bảng tổng có chi tiết từng câu ở dưới thì giữ làm bảng tóm tắt; bảng không có chi tiết thì tách thành câu
                if any(re.search(r"^###\s+`?%s`?" % re.search(r"OQ-\d+", cell(r, 0)).group(0), text, re.M) for r in rows):
                    out.extend(lines[i:j])
                    i = j
                    continue
                for r in rows:
                    k += 1
                    oq = re.search(r"OQ-\d+", cell(r, 0)).group(0)
                    owner = (clean(cell(r, oc)) or "PO") if oc is not None else "PO"
                    out.append("## Q%d. [%s] %s · %s" % (k, owner, oq, clean(cell(r, qc))))
                    if wc is not None and clean(cell(r, wc)):
                        out.append("Vì sao hỏi: %s" % clean(cell(r, wc)))
                    if pc is not None and clean(cell(r, pc)):
                        out.append("Đề xuất: %s" % clean(cell(r, pc)))
                    blk = bc is not None and clean(cell(r, bc)).lower().startswith(("yes", "có"))
                    out += ["Chặn: %s" % ("có" if blk else "không"), "[Answer]:", ""]
                    total += 1
                i = j
                continue
            out.extend(lines[i:j])
            i = j
            continue
        out.append(ln)
        i += 1
    if not total:
        return None
    head = "Intent: %s · Cách trả lời: chưa chọn · Đã trả lời: 0/%d · Chuyển từ định dạng luồng v1 ngày %s; mã cũ OQ-NN giữ trong tiêu đề từng câu" % (
        intent_name, total, today().isoformat())
    at = next((n for n, l in enumerate(out) if l.startswith("# ")), -1)
    out.insert(at + 1, "")
    out.insert(at + 2, head)
    return "\n".join(out) + "\n"


def migrate(intent, words, feature=None, write_out=False):
    intent = resolve_intent(intent)
    so = load_state(intent)
    if so is None:
        print("Không thấy state.md trong %s." % intent)
        return 2
    day0 = today().isoformat()
    t_now = now().strftime("%Y-%m-%d %H:%M")
    who = git_user() or "PO"
    S = stages()
    plan, writes = [], {}
    # 1. file sống: đường dẫn, thuật ngữ
    for f in sorted(intent.rglob("*.md")):
        r = rel(f, intent)
        if r.startswith(MIG_HISTORY) or r in MIG_HISTORY_FILES:
            continue
        old = read(f)
        new = mig_text(old)
        if new != old:
            writes[f] = new
            plan.append(("chuẩn hoá", r, sum(1 for a, b in zip(old.splitlines(), new.splitlines()) if a != b)))
    # 1b. phần sống của file lịch sử: dòng mô tả memory.md; stage chưa duyệt, Current, Versions của state.md
    for name in ("memory.md", "state.md"):
        f = intent / name
        old = read(f)
        if old is None:
            continue
        new = mig_live_part(old, name)
        if new != old:
            writes[f] = new
            plan.append(("chuẩn hoá phần sống", name, sum(1 for a, b in zip(old.splitlines(), new.splitlines()) if a != b)))
    # 1c. luồng 2.43 thay 2.41 HLD Brief
    sp = intent / "state.md"
    old = writes.get(sp, read(sp))
    new, aplan, moves = mig_alignment(intent, old)
    if new != old:
        writes[sp] = new
    plan += aplan
    for src, dst in moves:
        plan.append(("chuyển HLD Brief của luồng cũ vào archive", rel(src, intent), rel(dst, intent)))
    # 2. file câu hỏi luồng v1 của stage chưa duyệt
    for e in so.stages:
        st = S.by_slug.get(e["slug"])
        if st is None or e["mark"] in "xS":
            continue
        qf = intent / st.dir / st.questions
        cur = writes.get(qf, read(qf))
        if cur is None:
            continue
        conv = mig_questions_v1(cur, intent.name, domain_code())
        if conv is not None:
            writes[qf] = conv
            n = len(parse_questions(conv)[0])
            plan.append(("đổi định dạng câu hỏi", rel(qf, intent), n))
    # 3. mã tính năng
    imd = intent / "intent.md"
    itext = writes.get(imd, read(imd)) or ""
    fid = clean(frontmatter(itext).get("feature", ""))
    if not fid or fid.startswith("<"):
        code = domain_code()
        fid = feature or (next_feature(code, [INTENTS]) if code else "")
        if fid:
            if not valid_feature(fid):
                print("Mã tính năng %s sai dạng <mã sản phẩm>-F<NNN>." % fid)
                return 2
            dup = [n for f, its in feature_map([INTENTS]).items() if f == fid for n in its if n != intent.name]
            if dup:
                print("Mã %s đã thuộc intent %s." % (fid, ", ".join(dup)))
                return 2
            writes[imd] = insert_feature(itext, fid)
            plan.append(("cấp mã tính năng", "intent.md", fid))
    prd = stage_file(intent, "prd-generation")
    if fid and prd.exists():
        ptext = writes.get(prd, read(prd))
        if clean(frontmatter(ptext).get("feature", "")) != fid:
            writes[prd] = insert_feature(ptext, fid)
            plan.append(("ghi mã tính năng", rel(prd, intent), fid))
    # 4. .gitkeep thừa
    keeps = [g for g in intent.rglob(".gitkeep") if any(x.name != ".gitkeep" for x in g.parent.iterdir())]
    for g in keeps:
        plan.append(("xoá .gitkeep thừa", rel(g, intent), ""))
    # 5. artifact đã duyệt khác bản chụp sau khi chuẩn hoá: chụp lại
    snaps = []
    for e in so.stages:
        if e["mark"] != "x":
            continue
        st = S.by_slug.get(e["slug"])
        if st is None:
            continue
        lp = legacy_pointer(intent, e["rest"])
        af = lp if lp is not None else (intent / st.dir / st.main)
        if not af.exists():
            continue
        arch, av = latest_archive(intent, e["slug"], af.stem)
        if arch is None:
            continue
        cur = writes.get(af, read(af))
        if norm_body(cur) != norm_body(read(arch)):
            changed = sum(1 for a, b in zip(norm_body(read(arch)).splitlines(), norm_body(cur).splitlines()) if a != b)
            snaps.append((e, af, arch, changed))
            plan.append(("chụp lại bản duyệt", "%s %s" % (e["code"], rel(af, intent)), "khác %s ở %d dòng" % (rel(arch, intent), changed)))
    print("# Migrate %s lên engine %s\n" % (intent.name, (read(REPO / "VERSION") or "?").strip()))
    print(md_table(["Việc", "File", "Chi tiết"], [(a, b, c) for a, b, c in plan]) if plan else "Không có gì cần đổi.")
    if not write_out:
        print("\nChạy thử, chưa ghi gì. Xem từng file đổi bằng cách so với git sau khi chạy --write; chạy lại với --write để ghi.")
        return 0
    if not plan:
        return 0
    for f, t in writes.items():
        write(f, t)
    for src, dst in moves:
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
    if moves and (intent / "inception" / "hld-brief").is_dir() and not any((intent / "inception" / "hld-brief").iterdir()):
        (intent / "inception" / "hld-brief").rmdir()
    for g in keeps:
        g.unlink()
    snap_names = []
    for e, af, arch, _ in snaps:
        fm = frontmatter(read(af))
        tag = "v" + (clean(fm.get("version", "")) or "0")
        dst = archive_dst(intent, e["slug"], af, tag)
        if dst.exists():
            dst = archive_dst(intent, e["slug"], af, tag + "-migrate")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(af), str(dst))
        snap_names.append(rel(dst, intent))
    dtext = read(intent / "decisions.md") or ""
    dec = next_dec(dtext)
    summary = "Chuẩn hoá dữ liệu lên engine %s: đường dẫn mới, Unit, PIC, AI Reviewer%s%s%s. Không đổi nội dung nghiệp vụ" % (
        (read(REPO / "VERSION") or "").strip(), ", mã tính năng %s" % fid if fid else "",
        "; luồng 2.43 thay 2.41 HLD Brief" if aplan else "",
        "; chụp lại bản duyệt " + " · ".join(snap_names) if snap_names else "")
    dtext, _ = add_decision(dtext, {"DEC": dec, "Ngày": t_now, "Stage": "migrate", "Quyết định": summary,
                                     "Nguyên văn": '"%s"' % words, "Người quyết": who, "Read when": "migrate, phiên bản, mã tính năng"})
    write(intent / "decisions.md", dtext)
    lines = (read(intent / "state.md") or "").splitlines()
    append_log(lines, "- %s migrate lên engine %s bởi %s, %s" % (t_now, (read(REPO / "VERSION") or "").strip(), who, dec))
    write(intent / "state.md", "\n".join(lines) + "\n")
    print("\nĐã ghi %d file, %s, nhật ký trong state.md. Chạy po-tools.py status để kiểm." % (len(writes) + len(snap_names), dec))
    return 0


# ================================================================ main
def main(argv):
    try:
        if hasattr(sys.stdout, "reconfigure") and (sys.stdout.encoding or "").lower().replace("-", "") != "utf8":
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if len(argv) < 2 or argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, args = argv[1], argv[2:]
    try:
        if cmd == "trace" and args:
            pos, kv = parse_opts(args, flags=("--write",))
            return trace(pos[0], write_out=kv.get("--write", False))
        if cmd == "archive" and len(args) >= 3:
            pos, kv = parse_opts(args, opts=("--label",))
            return archive(pos[0], pos[1], pos[2], kv.get("--label"))
        if cmd == "status":
            return status(args[0] if args else INTENTS)
        if cmd == "next" and args:
            return next_cmd(args[0])
        if cmd == "check" and len(args) >= 2:
            pos, kv = parse_opts(args, flags=("--strict",))
            return check(pos[0], pos[1], strict=kv.get("--strict", False))
        if cmd == "approve" and len(args) >= 2:
            pos, kv = parse_opts(args, flags=("--dry-run",), opts=("--words", "--who", "--version", "--accept-warnings", "--accept-review-gap"))
            if "--words" not in kv:
                print("Thiếu --words \"<lời duyệt nguyên văn của PO>\".")
                return 2
            return approve(pos[0], pos[1], kv["--words"], kv.get("--who"), kv.get("--version"), kv.get("--dry-run", False),
                           kv.get("--accept-warnings"), kv.get("--accept-review-gap"))
        if cmd == "review-start" and len(args) >= 2:
            return review_start(args[0], args[1])
        if cmd == "replay" and args:
            return replay(args[0])
        if cmd == "feature-id":
            pos, kv = parse_opts(args, flags=("--next", "--dry-run"), opts=("--assign",))
            return feature_id(pos[0] if pos else None, kv.get("--assign"), kv.get("--dry-run", False))
        if cmd == "stories" and args:
            pos, kv = parse_opts(args, flags=("--write",), opts=("--us",))
            if pos:
                return stories_cmd(pos[0], kv.get("--write", False), kv.get("--us"))
        if cmd == "dor" and args:
            pos, kv = parse_opts(args, opts=("--story",))
            if pos:
                return dor(pos[0], kv.get("--story"))
        if cmd == "migrate" and args:
            pos, kv = parse_opts(args, flags=("--write",), opts=("--words", "--feature"))
            if pos:
                return migrate(pos[0], kv.get("--words") or "chuẩn hoá theo engine mới", kv.get("--feature"), kv.get("--write", False))
        if cmd == "index":
            return index("--write" in args)
        if cmd == "manifest":
            return manifest("--write" in args)
        if cmd == "engine-check":
            return engine_check("--strict" in args)
        if cmd == "doctor":
            return doctor()
        if cmd == "selftest":
            return selftest()
    except ValueError as e:
        print("Sai tham số: %s" % e)
        return 2
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
