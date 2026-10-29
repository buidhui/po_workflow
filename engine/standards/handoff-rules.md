# Quy tắc bàn giao liên team

Áp cho đầu ra PO giao cho Design, Tech và QA. Quy ước mã ở `id-conventions.md`, cách đặt tên và liên kết ở Figma, git, test, API ở `naming-conventions.md`, quyết định giao việc trên Jira ở `adr/0002-story-tren-jira.md`, quyết định thiết kế ở file riêng và thống nhất trên Decision Brief ở `adr/0003-thiet-ke-cua-team-va-decision-brief.md`.

## Hai mốc làm việc với các team

| Mốc | Khi nào | Đầu vào | Kết quả |
|---|---|---|---|
| Checkpoint | Stage 2.43, sau khi PRD được duyệt | PRD đã duyệt; ba team viết `ux-design.md`, `tech-design.md`, `test-design.md` từ PRD | Họp trên Decision Brief, 3 PIC ký; cỡ từng Unit, cỡ story và thay đổi PRD được thống nhất |
| Bàn giao cho Dev | Sau gate 2.43; profile S sau gate 2.42 | Story List đẩy lên Jira qua MCP hoặc import CSV | Story đạt điều kiện sẵn sàng |

## Story và chia việc

User story (US) là đơn vị nghiệm thu; story trên Jira là đơn vị Dev nhận vào sprint. PO chia US ở 2.4 theo `story-splitting.md` và gắn mỗi US vào một Unit. Ở checkpoint 2.43, Tech PIC xác nhận mỗi Unit độc lập và vừa một sprint; bảng Units ở PRD mục 5 là bản chốt. Mỗi Unit là một story trên Jira, gồm một hoặc nhiều US; Unit không tương ứng nhiều story, vì Unit quá lớn được tách thành hai Unit. Mỗi team tự chia việc: Design theo màn hình, một màn có thể phục vụ nhiều US; Dev chia story thành sub-task Backend, Frontend; QA theo tiêu chí chấp nhận, mỗi AC ít nhất một test case.

## Story List

Sau khi PRD được duyệt, và với profile M, L sau gate 2.43, `/po-stories` sinh `intents/<intent>/stories/story-list-prd-v<phiên bản>.csv`. Mỗi Unit một dòng, 12 cột theo mẫu import CSV của Jira; khi Unit có từ hai US, file có thêm cột Labels cho mã các US còn lại. Khi PRD không có mục Units, như với profile S, cả PRD là một story `<tính năng>-U1`:

| Cột | Nội dung | Nguồn |
|---|---|---|
| Project key, Project name, Project type | Dự án Jira | Frontmatter `domain/domain.md`: `jira_project_key`, `jira_project_name`, `jira_project_type` |
| Issue Type | `Story` | Khoá `jira_story_type` ở frontmatter `domain.md`, mặc định `Story` |
| Summary | Tên Unit | Cột Tên của bảng Units, PRD mục 5; khi thiếu, nối tên các US |
| Priority | Must thành Highest, Should thành High, Could thành Medium | Cột Ưu tiên của bảng Units; khi thiếu, lấy mức cao nhất trong dòng Ưu tiên của các US |
| Description | Khối của từng US trong Unit, mỗi khối mở đầu bằng mã và tên US: mô tả, điều kiện trước, kịch bản, tiêu chí chấp nhận, giao diện và validate, business rule, dữ liệu, NFR, ngoài phạm vi, tham chiếu tới PRD, tag và mã màn lấy từ `ux-design.md`. Viết theo cú pháp Jira, mã đầy đủ | Bảng Units và các khối US trong PRD |
| Epic Link | Mã Epic | Dòng Jira Epic của `intent.md`. Intent có nhiều Epic thì ghi thêm `U2: <mã Epic>` để gán theo Unit |
| Labels, 3 cột trở lên | Mã tính năng, mã story `<tính năng>-U<n>`, mã đầy đủ của từng US | PRD, bảng Units |
| Comment | Nguồn PRD và tag, kết quả điều kiện sẵn sàng, câu hỏi còn mở của các US, danh sách US, nhắc Dev điền story point và thứ tự | PRD |

- PRD là nguồn duy nhất của nội dung nghiệp vụ. Không sửa phần mô tả trên Jira ngoài change request.
- Chỉ ghi CSV từ PRD đã duyệt, và với profile M, L thì sau khi 2.43 được duyệt. Chưa đủ thì lệnh chỉ in bản xem trước.
- Bảng Units phải khớp các khối US: mỗi US thuộc đúng một Unit, Unit không ghi US không có trong PRD. Khi không khớp, `stories`, `dor`, `jira-sync` dừng và báo lỗi; `check` của 2.42 báo trước.
- Sơ đồ và khối mã trong PRD không chép sang Jira; Description thay mỗi sơ đồ bằng dòng "Sơ đồ hoặc khối mã: xem trong PRD".

## Đẩy story qua Jira MCP

Phiên AI có công cụ Jira của MCP thì `/po-stories` đẩy story thẳng lên Jira thay cho import CSV, theo `adr/0002-story-tren-jira.md` mục bổ sung. Nội dung story giống bản CSV, khác ở hai điểm: Description viết bằng Markdown, và story của Unit được phụ thuộc thành liên kết "is blocked by". Unit được phụ thuộc lấy từ cột Phụ thuộc của bảng Units và từ mục Tiền điều kiện của các US.

| Việc | Khi nào | Trên Jira |
|---|---|---|
| Tạo | Story chưa có trong `stories/jira-map.json` | Tìm theo nhãn mã story bằng JQL trước, loại các issue đã có trong map; không thấy thì tạo issue, gắn nhãn mã tính năng, mã story, mã các US, thêm comment nguồn PRD |
| Chuyển issue cũ | Story chưa có trong map, nhưng một US của Unit từng được đẩy thành issue riêng | Issue của US đầu tiên trở thành story của Unit, được cập nhật như việc Cập nhật; issue riêng của các US còn lại được gắn nhãn `merged-into-story` |
| Cập nhật | Nội dung, nhãn, Epic hoặc liên kết đổi so với lần đẩy trước | Thay mô tả, thêm comment ghi bản PRD mới và mã thêm, bỏ |
| Giữ nguyên | Không đổi | Không làm gì |
| Gắn nhãn `removed-from-prd` | Story có trong map, không còn trong PRD | Thêm nhãn và comment; không xoá issue |
| Gắn nhãn `merged-into-story` | Unit ghi "gộp vào U<n>" ở PRD mục 5, hoặc US từng là issue riêng nay nằm trong story của Unit | Thêm nhãn và comment ghi story nhận; không xoá issue |

- Story chưa đạt điều kiện sẵn sàng vẫn được đẩy, mang nhãn `not-ready` và comment ghi lý do. Story đạt ở lần đẩy sau thì nhãn được bỏ.
- Trước khi cập nhật, AI lấy bản trên Jira để script so với bản đẩy lần trước. Issue đã bị sửa tay trên Jira thì PO quyết định giữ bản trên Jira hoặc ghi đè.
- PO đồng ý bằng lời trước khi đẩy. `jira-sync --record` ghi kết quả vào `stories/jira-map.json` và một DEC, chỉ khi lời đồng ý có trong 3 lượt gần nhất của PO.
- `stories/jira-map.json` và `stories/jira-plan.json` do script ghi, hook chặn sửa tay. Mã issue không ghi vào PRD.
- Engine không phụ thuộc MCP. Không có MCP thì dùng CSV.

## Ai làm gì trên story Jira

| Team | Việc |
|---|---|
| PO | Đẩy story qua MCP hoặc import CSV, kiểm Epic, trả lời câu hỏi nghiệp vụ. Đổi nghiệp vụ thì đi change request, sau đó đẩy lại; dùng CSV thì sửa story theo bản CSV mới |
| Design PIC | Gắn mã màn hình `SCR` và link thiết kế vào story; frame Figma đặt tên bắt đầu bằng mã màn đầy đủ |
| Tech PIC | Chia story thành sub-task Backend, Frontend, ước lượng story point, ghi nhánh code; nhánh mang key Jira của story, commit có trailer mã yêu cầu |
| QA PIC | Viết test case mã `TC`, mỗi test case ghi mã AC mà nó kiểm; test tự động gắn tag mã AC đầy đủ |

Câu hỏi về nghiệp vụ ghi bằng comment trên story, gắn người phải trả lời. Câu trả lời làm đổi PRD thì PO đi qua change request; không sửa nghiệp vụ ngay trên Jira.

## Điều kiện sẵn sàng, DoR

Checkpoint là buổi họp trên Decision Brief ở 2.43. Story trên Jira được giao cho Dev khi mọi US của Unit đạt bảy điều kiện dưới đây; điều kiện 7 không xét US nằm cùng Unit, và Unit ở cột Phụ thuộc cũng phải đạt:
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
- Dùng đường MCP thì chạy lại `/po-stories`: `jira-sync` chỉ cập nhật story đổi, tạo story mới, gắn nhãn `removed-from-prd` cho story bị bỏ và `merged-into-story` cho Unit đã gộp vào Unit khác.
- Test case ghi bản PRD đã dùng khi chạy, để xác định kết quả còn đúng hay không sau một change request.

## Git

Commit file CSV trước khi gắn tag: profile S cùng lần commit PRD đã duyệt, profile M, L cùng lần commit Decision Brief đã duyệt. Đẩy qua MCP thì commit `stories/jira-map.json` cùng `decisions.md` sau mỗi lần đẩy.
