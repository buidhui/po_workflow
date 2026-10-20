# ADR 0001: Nơi lưu file story

| | |
|---|---|
| Trạng thái | Đã thay bằng ADR 0002 ngày 2026-10-19 |
| Ngày | 2026-10-19 |
| Người quyết định | PO phụ trách PO-Workflow |

## Bối cảnh

Đầu ra của PO là đầu vào của Design, Tech và QA. Mỗi user story cần một tài liệu chung, mỗi team viết một mục, có trạng thái để team sau biết khi nào nhận việc. Cần chọn nơi lưu và định dạng.

## Các lựa chọn đã xét

| Lựa chọn | Được | Mất |
|---|---|---|
| Git, Markdown, trong repo của PO | Có phiên bản, so được khác biệt, tag cho từng bản duyệt; agent AI của mọi team đọc được; PRD và story cùng một nơi nên sinh story từ PRD không phải đồng bộ | Team khác cần quyền ghi vào repo của PO và thấy được phần làm việc nội bộ của PO |
| Git, Markdown, repo spec riêng | Tách phần nội bộ của PO | Thêm một bước đẩy sang repo khác; hai repo phải đồng bộ phiên bản |
| Confluence hoặc Lark | Quen với người không dùng Git | Không so được khác biệt theo dòng; agent khó đọc đúng bản đã chốt; trạng thái và mã khó kiểm bằng máy |
| Docx | Quen thuộc | Không so được khác biệt, agent khó đọc, dễ có nhiều bản |

## Quyết định

File story lưu bằng Markdown trong repo của PO, tại `intents/<intent>/stories/`. Lark vẫn là nơi người đọc xem PRD và HLD Brief đã duyệt.

## Hệ quả

- Design PIC, Tech PIC, QA PIC cần quyền ghi vào repo của PO, như đã có cho HLD Brief.
- Phần nội bộ của PO, gồm `decisions.md`, `memory.md`, questions file, cũng hiển thị với các team. Trước khi mở quyền, PO rà tài khoản staging và thông tin nhạy cảm; workflow gitleaks quét mỗi lần push.
- Agent của Dev đọc story và PRD theo tag, qua `intents/INDEX.md`.
- Nếu sau này cần tách quyền, chuyển `stories/` sang repo spec riêng; quy ước mã và quy tắc bàn giao giữ nguyên.
