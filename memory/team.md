# Team memory

Bài học dùng chung cho mọi sản phẩm, đi theo engine: dựng domain mới thì giữ nguyên file này. Bài học chỉ đúng cho sản phẩm đang cài nằm ở `memory/project.md`.

AI đọc file này ở bước Load của mọi stage. Bài học có hiệu lực từ stage kế tiếp, không áp ngược cho stage đã duyệt. Dòng mới vào qua vòng học tại gate: ghi vào `project.md` trước, PO xác nhận đúng cho mọi sản phẩm thì chuyển sang đây. Không sửa tay giữa chừng một intent. Mâu thuẫn với `AGENTS.md` thì `AGENTS.md` thắng, và phải hỏi PO.

Dạng một dòng: `- <nội dung> (learned YYYY-MM-DD · <intent> <mã stage> · <tên người duyệt>)`. Các dòng đầu tiên chuyển từ sự cố và quyết định trước khi có quy ước này, nên chỉ có ngày; ngày là ngày sự việc xảy ra.

## Versioning
- Mốc tăng version là mỗi lần PO duyệt hoặc trả lời một đợt câu hỏi; sửa một dòng không tăng version. Bản đã duyệt phải được chụp lại trước khi sửa tiếp; một lần đã ghi đè bản duyệt ở Gate 1 mười lăm lần liên tiếp (learned 2026-10-06)

## Questions
- Không dựng danh sách câu hỏi kỹ thuật cho Dev. Chỉ hỏi câu mà đáp án làm đổi phạm vi hoặc business rule (learned 2026-10-05)
- Cần biết một cơ chế kỹ thuật có tồn tại không thì hỏi PO, không tự đào Swagger để kết luận (learned 2026-10-05)

## PRD
- PRD không có mục Database và API. Thay bằng mục Dữ liệu cần lưu giữ: thông tin nào phải lưu và vì sao (learned 2026-10-06)
- Ở 2.42 không hỏi lại người viết bảng thông tin, link Figma, tài khoản staging; để trống, người viết điền sau. Tiêu chí thành công lấy từ 1.1, không hỏi lại ở 2.42 (learned 2026-10-06)
- Không giữ bảng ví dụ của template. Hai PRD cũ mang nguyên chỉ số NPS của một app khác (learned 2026-09-23)
- Ràng buộc nghiệp vụ cho cách làm chỉ nêu cái gì phải đúng, không vẽ sequence, không thiết kế bảng, không chọn thuật toán (learned 2026-10-05)
- Define hết user story kể cả cái chưa làm, ghi "chưa làm" trong tiêu đề. Bức tranh đầy đủ giúp phân tích ảnh hưởng đúng (learned 2026-09-23)
- Thiết kế kỹ thuật không viết vào PRD; Tech PIC viết ở `tech-design.md`, theo ADR 0003. Một lần technical design backend viết thẳng vào PRD đã thay mất ràng buộc C1 đến C12, ba rule nền và định nghĩa chỉ số, làm gãy tham chiếu từ các US (learned 2026-10-12)

## Writing
- Không viết tắt trong tài liệu bàn giao. "Giải O2" phải là "Giải quyết mục tiêu O2" (learned 2026-10-01)
- Mã đứng liền nhau phải có dấu phân cách, nhiều trình hiển thị dính `US1US6` thành một chữ (learned 2026-10-01)
- Không ghi tài khoản staging hay thông tin nhạy cảm vào artifact; người đọc repo rộng hơn người viết (learned 2026-09-23)
- Trích mã thì kèm nội dung. Một dự án L sinh hàng trăm mã, không ai nhớ hết (learned 2026-10-01)
- Dọn dấu vết quy trình trước khi bàn giao. Dev và QA không tra được "9A" hay "Gate 3" là gì (learned 2026-09-23)
- Sơ đồ viết sẵn trong file dưới dạng Mermaid, không vẽ thêm sau khi publish. File nguồn là bản duy nhất (learned 2026-10-06)
