# Project memory

Bài học chỉ đúng cho sản phẩm đang cài trong `domain/`. Dựng domain mới thì đưa file này về bản trống, theo `DOMAIN-SETUP.md`. Bài học dùng chung cho mọi sản phẩm nằm ở `memory/team.md`.

AI đọc file này ở bước Load của mọi stage. Bài học có hiệu lực từ stage kế tiếp, không áp ngược cho stage đã duyệt. Vòng học tại gate ghi vào đây trước, sau đó hỏi PO bài học có đúng cho mọi sản phẩm không; có thì chuyển sang `team.md`.

Dạng một dòng: `- <nội dung> (learned YYYY-MM-DD · <intent> <mã stage> · <tên người duyệt>)`.
