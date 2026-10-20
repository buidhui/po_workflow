#!/usr/bin/env python3
"""Hook của Claude Code cho PO-Workflow, theo các hook của AWS AI-DLC. Chỉ dùng thư viện chuẩn, đọc payload JSON từ stdin.

- UserPromptSubmit và PostToolUse của AskUserQuestion: ghi lượt người thật vào .po/turns.jsonl. `po-tools.py approve`
  chỉ ghi duyệt khi lời PO có nguyên văn trong sổ này, như HUMAN_TURN của AWS.
- PreToolUse của Edit, Write, MultiEdit, NotebookEdit: chặn AI tự đánh [x] trong state.md, sửa phần thân artifact đã
  duyệt khi không có change request mở, sửa dòng DEC cũ trong decisions.md, AI Reviewer ghi ngoài reviews/, phiên
  chính sửa file review đã có hoặc file digest.
- PreToolUse của Bash: chặn lệnh đụng sổ lượt người, lệnh sửa state.md, decisions.md, archive/ bằng shell, và subagent
  chạy lệnh ghi của po-tools.py.

Lỗi bất ngờ thì cho qua: hook chặn lỗi vô ý, không phải sandbox, như AWS ghi ở runtime-integrity. Mỗi lần chạy ghi
giờ vào .po/hooks/<sự kiện>.last để `po-tools.py doctor` biết hook có chạy.
"""
import datetime
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("po_tools", str(HERE / "po-tools.py"))
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)

KEEP_TURNS = 200
FILE_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit")
WRITE_CMDS = re.compile(r"po-tools\.py\s+(approve|archive|migrate|review-start)\b")
GUARDED = r"(?:(?:state|decisions)\.md\b|/archive/|\.digest\b)"
SHELL_EDIT = re.compile(r"\bsed\s+-[a-zA-Z]*i|\bperl\s+-[a-zA-Z]*i|\btee\b|\bmv\b|\bcp\b|\brm\b|python3?\s+-c|\btruncate\b")
GUARDED_SHELL = re.compile(GUARDED)
REDIRECT_INTO = re.compile(r">{1,2}\s*['\"]?[^\s|;&]*" + GUARDED)


def stamp():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def deny(reason):
    """Chặn lệnh: JSON permissionDecision trên stdout và mã thoát 2 kèm lý do trên stderr, như AWS làm cho Claude Code."""
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}, ensure_ascii=False))
    sys.stderr.write(reason + "\n")
    return 2


def heartbeat(event):
    d = T.ROOT / ".po" / "hooks"
    d.mkdir(parents=True, exist_ok=True)
    (d / (re.sub(r"[^A-Za-z]", "", event) + ".last")).write_text(stamp() + "\n", encoding="utf-8")


def record(text, kind):
    text = (text or "").strip()
    if not text:
        return
    T.TURNS.parent.mkdir(parents=True, exist_ok=True)
    lines = (T.read(T.TURNS) or "").splitlines()[-(KEEP_TURNS - 1):]
    lines.append(json.dumps({"ts": stamp(), "kind": kind, "text": text}, ensure_ascii=False))
    T.TURNS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def answer_text(payload):
    """Lựa chọn và ghi chú của PO trong AskUserQuestion."""
    parts = []
    ti = payload.get("tool_input") or {}
    ans = ti.get("answers")
    if isinstance(ans, dict):
        parts += [str(v) for v in ans.values()]
    ann = ti.get("annotations")
    if isinstance(ann, dict):
        parts += [str(v.get("notes")) for v in ann.values() if isinstance(v, dict) and v.get("notes")]
    resp = payload.get("tool_response")
    if not parts and resp:
        parts.append(resp if isinstance(resp, str) else json.dumps(resp, ensure_ascii=False))
    return "\n".join(parts)


def new_content(tool, ti, old):
    """Nội dung file sau lệnh sửa; None khi không tính được, khi đó để công cụ tự báo lỗi."""
    if tool == "Write":
        return ti.get("content", "")
    edits = [ti] if tool == "Edit" else (ti.get("edits") or []) if tool == "MultiEdit" else None
    if edits is None or old is None:
        return None
    cur = old
    for e in edits:
        a, b = e.get("old_string", ""), e.get("new_string", "")
        if not a or a not in cur:
            return None
        cur = cur.replace(a, b) if e.get("replace_all") else cur.replace(a, b, 1)
    return cur


def intent_of(path):
    """(thư mục intent, đường dẫn bên trong intent) khi file nằm trong intents/<intent>/."""
    try:
        r = path.resolve().relative_to(T.INTENTS.resolve())
    except ValueError:
        return None, None
    if len(r.parts) < 2:
        return None, None
    return T.INTENTS / r.parts[0], Path(*r.parts[1:]).as_posix()


def only_publish_keys(old, new):
    """Chỉ đổi khoá published* ở đầu file, hoặc lark* của bản cũ, phần thân giữ nguyên: ghi nơi đăng bản đọc được phép."""
    if T.norm_body(old) != T.norm_body(new):
        return False
    a, b = T.frontmatter(old), T.frontmatter(new)
    keys = set(a) | set(b)
    return all(k.startswith(("published", "lark")) for k in keys if a.get(k) != b.get(k))


def approved_artifact(intent, path):
    """Stage đã duyệt mà file là artifact của nó, hoặc None."""
    so = T.load_state(intent)
    if so is None:
        return None
    S = T.stages()
    for e in so.stages:
        if e["mark"] != "x":
            continue
        st = S.by_slug.get(e["slug"])
        if st is None:
            continue
        lp = T.legacy_pointer(intent, e["rest"])
        cands = [lp] if lp is not None else [intent / st.dir / a for a in st.artifacts]
        if any(c is not None and c.resolve() == path.resolve() for c in cands):
            return so, e, st
    return None


def pre_file(payload):
    tool, ti = payload.get("tool_name"), payload.get("tool_input") or {}
    fp = ti.get("file_path") or ti.get("notebook_path") or ""
    if not fp:
        return 0
    path = Path(fp) if Path(fp).is_absolute() else T.ROOT / fp
    agent = payload.get("agent_type") or ""
    intent, inner = intent_of(path)
    if agent == "ai-reviewer":
        if inner is None or not re.fullmatch(r"reviews/review-[a-z0-9-]+-\d+\.md", inner):
            return deny("AI Reviewer chỉ ghi đúng một file review trong intents/<intent>/reviews/, không sửa file nào khác. "
                        "Xem engine/protocol/review-protocol.md.")
        return 0
    if intent is None:
        return 0
    if re.fullmatch(r"reviews/review-[a-z0-9-]+-\d+\.digest", inner):
        return deny("File digest do po-tools.py review-start ghi, không sửa tay.")
    if re.fullmatch(r"reviews/review-[a-z0-9-]+-\d+\.md", inner) and path.exists():
        return deny("File review là kết quả của AI Reviewer, phiên chính không sửa. Phản hồi finding ghi ở gate và decisions.md; "
                    "cần review lại thì chạy review-start và gọi reviewer.")
    old = T.read(path)
    new = new_content(tool, ti, old)
    if new is None:
        return 0
    if inner == "state.md" and old is not None:
        before, after = len(re.findall(r"^- \[x\]", old, re.M)), len(re.findall(r"^- \[x\]", new, re.M))
        if after > before:
            return deny("Chỉ python3 engine/scripts/po-tools.py approve được đánh dấu stage đã duyệt [x], sau khi PO duyệt ở gate. "
                        "Đánh [?] khi trình gate, chờ PO trả lời, sau đó chạy approve với lời PO.")
    if inner == "decisions.md" and old is not None:
        keep = set(new.splitlines())
        gone = [ln for ln in old.splitlines() if re.match(r"^\|\s*DEC\d+\s*\|", ln) and ln not in keep]
        if gone:
            dec = re.match(r"^\|\s*(DEC\d+)", gone[0]).group(1)
            return deny("decisions.md chỉ được thêm dòng, không sửa hay xoá dòng DEC cũ (%s). Quyết định đổi thì thêm dòng DEC "
                        "mới ghi rõ thay %s." % (dec, dec))
    hit = approved_artifact(intent, path) if old is not None else None
    if hit and not only_publish_keys(old, new):
        so, e, st = hit
        if not T.open_crs(intent, so):
            return deny("%s là artifact của %s %s đã duyệt. Sửa sau khi duyệt phải qua /change-request: mở CR, stage về [R], "
                        "sau đó mới sửa." % (inner, e["code"], st.name))
    return 0


def pre_bash(payload):
    cmd = (payload.get("tool_input") or {}).get("command") or ""
    if re.search(r"\.po/|turns\.jsonl|po-hook", cmd):
        return deny("Sổ lượt người trong .po/ chỉ hook ghi và chỉ po-tools.py đọc; lệnh shell không đụng tới.")
    if payload.get("agent_type") and WRITE_CMDS.search(cmd):
        return deny("Subagent không chạy lệnh ghi của po-tools.py (approve, archive, migrate, review-start). "
                    "Phiên chính chạy sau khi PO quyết.")
    if REDIRECT_INTO.search(cmd) or (GUARDED_SHELL.search(cmd) and SHELL_EDIT.search(cmd)):
        return deny("Không sửa state.md, decisions.md, archive/ hay file digest bằng lệnh shell. Dùng Edit để hook kiểm được, "
                    "hoặc lệnh của po-tools.py.")
    return 0


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return 0
    ev = payload.get("hook_event_name") or ""
    try:
        if ev:
            heartbeat(ev)
        if ev == "UserPromptSubmit":
            record(payload.get("prompt"), "prompt")
        elif ev == "PostToolUse" and payload.get("tool_name") == "AskUserQuestion":
            record(answer_text(payload), "answer")
        elif ev == "PreToolUse" and payload.get("tool_name") in FILE_TOOLS:
            return pre_file(payload)
        elif ev == "PreToolUse" and payload.get("tool_name") == "Bash":
            return pre_bash(payload)
    except Exception:  # hook không bao giờ làm hỏng phiên; lỗi bất ngờ thì cho qua
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
