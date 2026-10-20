# /po-review

Theo `engine/protocol/review-protocol.md`. Không sửa artifact. Không ghi `state.md` trừ khi được gọi từ một stage.

1. Xác định artifact và stage. Thư mục stage cho biết slug; `--stage` để chỉ rõ. File ngoài `intents/` hoặc có `--shadow` thì chạy chế độ shadow.
2. Input Readiness Gate: artifact có đủ nền chưa, stage trước đã approve chưa. Thiếu thì báo và hỏi có review tiếp không. Review PRD trên Impact Matrix chưa duyệt là review trên cát.
3. Gọi AI Reviewer theo `engine/protocol/review-protocol.md` mục Gọi reviewer. Trước khi gọi, chạy kiểm bằng máy và lưu vào `verification/<slug>-machine.md`. Truyền đường dẫn, không dán nội dung: file stage, questions file, artifact, artifact đầu vào, `GLOSSARY.md`, KB liên quan, kết quả kiểm bằng máy, sổ finding `reviews/findings-<slug>.md` nếu có. Không truyền file review cũ. Yêu cầu ghi `reviews/review-<slug>-<NN>.md`, NN là số lần trước cộng một. Nói với PO một câu: "Để AI Reviewer xem qua trước khi anh/chị đọc."
4. Đọc file review, cấp ID cho finding mới và cập nhật sổ finding. Trình verdict, finding Open và Reopened, summary. PO quyết: sửa, hoặc ghi quyết định vào sổ finding và `decisions.md` (Accepted risk, Rejected kèm lý do, Reopened). Review không hoàn tất thì làm theo mục Review không hoàn tất của review-protocol.

## Chế độ shadow, tài liệu người khác viết
Trước khi gọi agent: tóm tắt tài liệu để PO xác nhận hiểu đúng. Agent nhận thêm nhiệm vụ: quét KB, API spec, so với hệ thống thật; findings chia ba nhóm sai, thiếu, mơ hồ; phụ lục A nguồn đã đọc kể cả chưa tra được; phụ lục B câu AI tự trả lời được kèm nguồn và độ chắc. Mục đích là tìm điểm sai so với hệ thống thật; cách viết không chấm.
