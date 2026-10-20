# /po-evaluate

Đánh giá giải pháp sau khi phát hành, theo BABOK v3 chương 8 Solution Evaluation: đo kết quả (8.1), phân tích số đo (8.2), tìm hạn chế của giải pháp (8.3) và của tổ chức (8.4), đề xuất hành động để tăng giá trị (8.5). AWS AI-DLC không có bước này trong Ideation và Inception; phần gần nhất nằm ở phase Operation. Lệnh này khép vòng: tiêu chí thành công `SC<n>` đặt ở 1.1 và PRD mục 2 được đo lại sau phát hành.

Xác định intent: ưu tiên tham số lệnh; không có thì hỏi. Tính năng chưa phát hành thì dừng.

## 1. Khi nào chạy
Theo cột Thời điểm đo của từng tiêu chí thành công trong PRD mục 2, hoặc khi PO yêu cầu. Một intent có thể đánh giá nhiều lần; mỗi lần một file.

## 2. Đọc
PRD bản đã duyệt mới nhất: mục 1 mục tiêu `O<n>`, mục 2 tiêu chí thành công, mục 8 yêu cầu chuyển đổi; User Guide của intent; `decisions.md` mục Rủi ro; trạng thái tính năng trong `domain/00-index.md`.

## 3. Hỏi số liệu
Với mỗi `SC<n>`, hỏi người đo ghi trong PRD: giá trị thực tế, nguồn số liệu, ngày đo. AI không tự đặt số và không suy số từ dữ liệu không ai xác nhận. Chưa đo được thì ghi "chưa đo được" kèm lý do.

## 4. Phân tích
- So giá trị thực tế với giá trị hiện tại trước phát hành và giá trị mục tiêu: Đạt, Chưa đạt, Chưa đo được.
- Tiêu chí Chưa đạt: tìm nguyên nhân thuộc giải pháp, như lỗi, thiếu chức năng, Dev làm khác PRD, theo 8.3; hoặc thuộc tổ chức, như quy trình chưa đổi, người dùng chưa được đào tạo, chính sách, theo 8.4. Mỗi nguyên nhân có bằng chứng.
- Rủi ro trong sổ rủi ro đã xảy ra hay chưa; cập nhật trạng thái.

## 5. Khuyến nghị và quyết định
Mỗi khuyến nghị thuộc một loại: giữ nguyên; cải tiến bằng intent mới, ghi ở mục Intent liên quan của `intent.md`; điều chỉnh vận hành hoặc đào tạo; quay lui hoặc dừng tính năng. PO quyết; ghi DEC nguyên văn. Quyết định dừng tính năng thì đổi trạng thái trong `domain/00-index.md` sang Deprecated.

## Output
`evaluation/solution-evaluation-<YYMMDD>.md` trong intent, theo `engine/templates/solution-evaluation.md`. Dòng Log trong `state.md`. Tự kiểm theo `engine/verification/po-evaluate.md`.
