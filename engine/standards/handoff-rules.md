# Quy tắc bàn giao liên team

Áp cho đầu ra PO giao cho Design, Tech và QA. Quy ước mã ở `id-conventions.md`, cách đặt tên và liên kết ở Figma, git, test, API ở `naming-conventions.md`, quyết định giao việc trên Jira ở `adr/0002-story-tren-jira.md`, quyết định thiết kế ở file riêng và chốt trên Decision Brief ở `adr/0003-thiet-ke-cua-team-va-decision-brief.md`.

## Hai mốc làm việc với các team

| Mốc | Khi nào | Đầu vào | Kết quả |
|---|---|---|---|
| Checkpoint | Stage 2.43, sau khi PRD được duyệt | PRD đã duyệt; ba team viết `ux-design.md`, `tech-design.md`, `test-design.md` từ PRD | Họp trên Decision Brief, 3 PIC ký; cỡ story và thay đổi PRD được chốt |
| Giao Dev | Sau gate 2.43; profile S sau gate 2.42 | Story List import lên Jira | Story đạt điều kiện giao Dev |

## Story và chia việc

Story là đơn vị nghiệm thu. PO chia story ở 2.4 theo `story-splitting.md`; cỡ story được Tech PIC xác nhận ở checkpoint 2.43. Story List giữ nguyên cách chia đó: mỗi US trong PRD là một story trên Jira. Mỗi team tự chia việc từ story: Design theo màn hình, một màn có thể phục vụ nhiều story; Dev theo Unit of work, một Unit gồm một hoặc nhiều story, chia tiếp thành sub-task nếu cần; QA theo tiêu chí chấp nhận, mỗi AC ít nhất một test case.

## Story List

Sau khi PRD được duyệt, và với profile M, L sau gate 2.43, `/po-stories` sinh `intents/<intent>/stories/story-list-prd-v<phiên bản>.csv`. Mỗi US một dòng, 12 cột theo mẫu import CSV của Jira:

| Cột | Nội dung | Nguồn |
|---|---|---|
| Project key, Project name, Project type | Dự án Jira | Frontmatter `domain/domain.md`: `jira_project_key`, `jira_project_name`, `jira_project_type` |
| Issue Type | `Story` | Cố định |
| Summary | Tên user story | Tiêu đề `## US<n>` trong PRD |
| Priority | Must thành Highest, Should thành High, Could thành Medium | Dòng Ưu tiên của US trong PRD; thiếu thì để trống |
| Description | Mô tả, điều kiện trước, kịch bản, tiêu chí chấp nhận, giao diện và validate, business rule, dữ liệu, NFR, ngoài phạm vi, tham chiếu tới PRD, tag và mã màn lấy từ `ux-design.md`. Viết theo cú pháp Jira, mã đầy đủ | Khối US trong PRD |
| Epic Link | Mã Epic | Dòng Jira Epic của `intent.md`. Intent có nhiều Epic thì ghi thêm `U2: <mã Epic>` để gán theo Unit |
| Labels, 3 cột | Mã tính năng, mã story, mã tính năng kèm Unit | PRD, bảng Units |
| Comment | Nguồn PRD và tag, kết quả điều kiện giao Dev, câu hỏi còn mở của story, nhắc Dev điền story point và thứ tự | PRD |

- PRD là nguồn duy nhất của nội dung nghiệp vụ. Không sửa phần mô tả trên Jira ngoài change request.
- Chỉ ghi CSV từ PRD đã duyệt, và với profile M, L thì sau khi 2.43 được duyệt. Chưa đủ thì lệnh chỉ in bản xem trước.
- Sơ đồ và khối mã trong PRD không chép sang Jira; Description thay mỗi sơ đồ bằng dòng "Sơ đồ hoặc khối mã: xem trong PRD".

## Ai làm gì trên story Jira

| Team | Việc |
|---|---|
| PO | Import CSV, kiểm Epic, trả lời câu hỏi nghiệp vụ. Đổi nghiệp vụ thì đi change request, sau đó sửa story theo bản CSV mới |
| Design PIC | Gắn mã màn hình `SCR` và link thiết kế vào story; frame Figma đặt tên bắt đầu bằng mã màn đầy đủ |
| Tech PIC | Gom story vào Unit of work, chia sub-task, ước lượng story point, ghi nhánh code; nhánh mang key Jira của story, commit có trailer mã yêu cầu |
| QA PIC | Viết test case mã `TC`, mỗi test case ghi mã AC mà nó kiểm; test tự động gắn tag mã AC đầy đủ |

Câu hỏi về nghiệp vụ ghi bằng comment trên story, gắn người phải trả lời. Câu trả lời làm đổi PRD thì PO đi qua change request; không sửa nghiệp vụ ngay trên Jira.

## Điều kiện giao Dev, DoR

Checkpoint là buổi họp trên Decision Brief ở 2.43. Story được giao cho Dev khi:
1. PRD đã duyệt.
2. Profile M, L: 2.43 Design Alignment đã duyệt.
3. US có ít nhất một tiêu chí chấp nhận.
4. Mọi business rule của US có ít nhất một tiêu chí chấp nhận trỏ tới.
5. US không còn `❓PO`, và mục Câu hỏi mở của PRD không còn câu chặn gắn với US đó. PRD theo template cũ dùng mục Open Issues.
6. US có bảng giao diện thì có màn trong `ux-design.md`, bảng Danh sách màn.
7. US nêu ở Tiền điều kiện là phải xong trước cũng đạt các điều kiện trên.

Đây là bản hẹp phía PO của Definition of Ready bên AWS. AWS có thêm hai mục mà PO-Workflow để cho team khác: thiết kế đã được xem, do Design PIC xác nhận trên Jira; story đã được ước lượng, do Dev làm trên Jira. Kiểm bằng `python3 engine/scripts/po-tools.py dor intents/<intent>`. Kết quả cũng ghi ở cột Comment của CSV. Độ phủ test case, tức mọi AC có test case, do QA theo dõi trên Jira; script không kiểm.

## Phiên bản và thay đổi

- File CSV mang phiên bản PRD đã sinh ra nó, ví dụ `story-list-prd-v1.0.csv`. Mỗi lần PRD duyệt có tag `<intent>/prd-v<version>`.
- PRD lên bản mới qua change request thì sinh CSV mới. Script so với bản CSV trước và in story nào đổi, story nào mới. PO sửa story đã import trên Jira theo danh sách đó và import riêng các story mới.
- Test case ghi bản PRD đã dùng khi chạy, để xác định kết quả còn đúng hay không sau một change request.

## Git

Commit file CSV trước khi gắn tag: profile S cùng lần commit PRD đã duyệt, profile M, L cùng lần commit Decision Brief đã duyệt.
