# /po-stories

Lập Story List từ PRD đã duyệt, sau gate 2.43 với profile M, L, mỗi Unit ở PRD mục 5 một story gồm các US của Unit, kiểm điều kiện sẵn sàng, sau đó đưa story lên Jira theo một trong hai đường: đẩy thẳng qua Jira MCP, hoặc import file CSV. Quy tắc ở `engine/standards/handoff-rules.md`, mã ở `engine/standards/id-conventions.md`, quyết định ở `engine/standards/adr/0002-story-tren-jira.md`.

## Chuẩn bị

1. Xác định intent từ tham số lệnh; thiếu thì hỏi. Intent phải có mã tính năng trong `intent.md`. Chưa có thì chạy `po-tools.py feature-id --assign intents/<slug>` sau khi PO đồng ý.
2. Xem trước: `python3 engine/scripts/po-tools.py stories intents/<slug>`. Script in mỗi story, mã `<tính năng>-U<n>`, kèm tên Unit, ưu tiên, các US, Epic, kết quả điều kiện sẵn sàng và mã issue trên Jira nếu đã đẩy; báo nếu `domain.md` thiếu `jira_project_key`, `jira_project_name`, nếu `intent.md` thiếu Epic hoặc có nhiều Epic. Bảng Units không khớp các khối US, như US chưa thuộc Unit nào hoặc US nằm trong hai Unit, làm lệnh dừng; báo PO, vì sửa bảng Units sau khi PRD đã duyệt phải qua change request.
3. Trình PO bảng xem trước. Story chưa đạt vì một US còn `❓PO`, thiếu AC, câu chặn, giao diện chưa có mã màn `SCR`, hoặc phụ thuộc Unit chưa đạt thì nói rõ từng lý do kèm mã US. Unit không có cột Ưu tiên và các US không có dòng Ưu tiên thì Priority để trống; nhắc PO bổ sung qua change request nếu cần. Intent có nhiều Epic thì hỏi PO gán Epic theo Unit bằng cách ghi `U<n>: <mã Epic>` vào dòng Jira Epic của `intent.md`.
4. Chọn đường: phiên có công cụ Jira của MCP, như `createJiraIssue`, `editJiraIssue`, `searchJiraIssuesUsingJql`, thì dùng đường A; không có thì dùng đường B. PO muốn import CSV thì dùng đường B.

## Đường A: đẩy qua Jira MCP

Script lập kế hoạch và ghi kết quả; AI gọi công cụ Jira. Script không gọi Jira.

1. Lập kế hoạch: `python3 engine/scripts/po-tools.py jira-sync intents/<slug>`. Script so PRD với `stories/jira-map.json` và xếp mỗi story vào một việc: tạo, cập nhật, giữ nguyên, gắn nhãn `removed-from-prd` cho story không còn trong PRD, hoặc gắn nhãn `merged-into-story` cho Unit đã gộp vào Unit khác và cho issue riêng của US từ lần đẩy theo từng US. Story chưa có trong map mà một US của Unit từng có issue riêng thì issue đó trở thành story của Unit, ghi ở trường `adopt`. Story chưa đạt điều kiện sẵn sàng vẫn được đẩy, mang nhãn `not-ready` và comment ghi lý do. Nội dung từng issue nằm ở `stories/jira-plan.json`.
2. Đối chiếu bản trên Jira khi kế hoạch có việc cập nhật: lấy Summary và Description của từng issue cần cập nhật bằng công cụ đọc issue của MCP, ghi vào một file JSON tạm ngoài repo dạng `{"<mã issue>": {"summary": "...", "description": "..."}}`, chạy lại `jira-sync intents/<slug> --remote <file>`. Issue bị sửa trên Jira sau lần đẩy trước hiện là "đã sửa trên Jira, chờ PO".
3. Trình PO bảng kế hoạch. Với mỗi issue đã sửa trên Jira, hỏi PO giữ bản trên Jira, tức bỏ qua story đó, hoặc ghi đè; PO chọn ghi đè thì chạy lại với `--overwrite <mã story>`. Chờ PO đồng ý bằng lời; không đẩy khi PO chưa trả lời.
4. Đẩy theo `stories/jira-plan.json`, từng mục:
   - `create`: trước khi tạo, tìm bằng câu JQL ở trường `jql` của mục; thấy issue có sẵn thì không tạo, ghi kết quả `found` kèm mã issue. Không thấy thì tạo issue với `issue_type`, Summary, Description dạng Markdown, Priority, nhãn ở `labels`, Epic qua trường `parent` hoặc Epic Link theo `epic_mode`; sau đó thêm comment ở `comment`.
   - `update`: thay Summary, Description, Priority, Epic; thêm nhãn ở `labels_add`, bỏ nhãn ở `labels_remove`, giữ các nhãn khác; thêm comment.
   - `remove`: không xoá issue; thêm nhãn ở `labels_add`, là `removed-from-prd` hoặc `merged-into-story`, và comment.
   - `unchanged`, `conflict` mà PO chọn giữ: không làm gì.
   - Sau khi tạo xong, với mỗi story có `blocked_by` hoặc `links_add`, tạo liên kết "is blocked by" tới issue của story được nêu.
5. Ghi kết quả vào một file JSON tạm ngoài repo dạng `{"<mã story>": {"key": "<mã issue>", "status": "ok"}}`. `status` là `ok`, `found`, `failed` hoặc `skipped`; lỗi thì ghi `failed` kèm `error`. Chạy `po-tools.py jira-sync intents/<slug> --record <file> --words "<lời đồng ý của PO, nguyên văn>"`. Script ghi `stories/jira-map.json` và một DEC.
6. Báo PO số issue đã tạo, cập nhật, gắn nhãn, issue lỗi, kèm mã issue. Nhắc PO commit `stories/jira-map.json` và `decisions.md`, chạy `po-tools.py index --write`.

## Đường B: import CSV

1. PRD đã duyệt, với profile M, L thì 2.43 đã duyệt, và PO đồng ý thì ghi: `po-tools.py stories intents/<slug> --write`. Script ghi `intents/<slug>/stories/story-list-prd-v<phiên bản>.csv`.
2. Có story đổi so với bản CSV trước: liệt kê để PO sửa các story đó trên Jira và báo đúng PIC; story mới thì PO import riêng.
3. Nhắc PO commit file CSV, gắn tag theo lệnh script in ra, sau đó import file lên Jira. Profile S commit cùng PRD đã duyệt; profile M, L commit cùng Decision Brief đã duyệt.

## Quy tắc chung

- Không sửa nội dung nghiệp vụ trong CSV hoặc trên Jira; nghiệp vụ chỉ đổi khi PRD đổi qua change request.
- Không sửa tay `stories/jira-map.json` và `stories/jira-plan.json`; hook chặn.
- Không xoá issue trên Jira, kể cả story đã bỏ khỏi PRD.
- Mã issue không ghi vào PRD; bảng của lệnh `stories` và `intents/INDEX.md` đọc từ `jira-map.json`.
