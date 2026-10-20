# /po-stories

Lập Story List để import lên Jira từ PRD đã duyệt, sau gate 2.43 với profile M, L, mỗi US một dòng theo mẫu import CSV của Jira, sau đó kiểm điều kiện giao Dev. Quy tắc ở `engine/standards/handoff-rules.md`, mã ở `engine/standards/id-conventions.md`, quyết định ở `engine/standards/adr/0002-story-tren-jira.md`.

1. Xác định intent từ tham số lệnh; thiếu thì hỏi. Intent phải có mã tính năng trong `intent.md`. Chưa có thì chạy `po-tools.py feature-id --assign intents/<slug>` sau khi PO đồng ý.
2. Xem trước: `python3 engine/scripts/po-tools.py stories intents/<slug>`. Script in mỗi story kèm ưu tiên, Unit, Epic và kết quả điều kiện giao Dev; báo nếu `domain.md` thiếu `jira_project_key`, `jira_project_name`, nếu `intent.md` thiếu Epic hoặc có nhiều Epic; có bản CSV trước thì in story nào đổi, story nào mới.
3. Trình PO bảng xem trước. Story chưa đạt vì `❓PO`, thiếu AC, câu chặn, giao diện chưa có mã màn `SCR`, hoặc phụ thuộc story chưa đạt thì nói rõ từng lý do. Story thiếu dòng Ưu tiên thì cột Priority để trống; nhắc PO bổ sung qua change request nếu cần. Intent có nhiều Epic thì hỏi PO gán Epic theo Unit bằng cách ghi `U<n>: <mã Epic>` vào dòng Jira Epic của `intent.md`.
4. PRD đã duyệt, với profile M, L thì 2.43 đã duyệt, và PO đồng ý thì ghi: `po-tools.py stories intents/<slug> --write`. Script ghi `intents/<slug>/stories/story-list-prd-v<phiên bản>.csv`.
5. Có story đổi so với bản CSV trước: liệt kê để PO sửa các story đó trên Jira và báo đúng PIC; story mới thì PO import riêng.
6. Nhắc PO commit file CSV, gắn tag theo lệnh script in ra, sau đó import file lên Jira. Profile S commit cùng PRD đã duyệt; profile M, L commit cùng Decision Brief đã duyệt.

Không sửa nội dung nghiệp vụ trong CSV hoặc trên Jira; nghiệp vụ chỉ đổi khi PRD đổi qua change request.
