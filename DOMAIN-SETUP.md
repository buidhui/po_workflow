# Đưa một sản phẩm mới vào quy trình

Tài liệu này dành cho người phụ trách quy trình. Tài liệu mô tả các việc làm một lần khi đưa PO-Workflow vào một sản phẩm hoặc một công ty mới. Thao tác hằng ngày của PO ở [USER-GUIDE.md](USER-GUIDE.md); phương pháp ở [README.md](README.md).

## 1. Hai tầng của repo

Repo có hai tầng. Engine là phần không phụ thuộc sản phẩm: protocol, lệnh, template, checklist, agent, script, chuẩn bàn giao và gói kiến thức vai PO lấy từ AWS. Domain pack là knowledge base của một sản phẩm, nằm trọn trong thư mục `domain/`. Template của mọi artifact, kể cả PRD và User Guide, thuộc engine và dùng chung cho mọi sản phẩm. Chuẩn `engine/standards/domain-kb.md` định nghĩa domain cần những file nào và người phụ trách phải cung cấp thông tin gì.

```
domain/
├── domain.md            manifest: sản phẩm, nguồn, bản đồ KB, dữ kiện cho từng stage
├── 00-index.md          module, trạng thái tính năng, vùng chưa phủ
├── glossary.md          thuật ngữ nghiệp vụ
├── concept-model.md     thực thể nghiệp vụ và quan hệ
├── 01-<module>.md …     mỗi module một file
├── data-model.md        thực thể dữ liệu, quan hệ, thực thể dùng chung
├── permissions.md       ma trận vai và quyền
├── integrations.md      hệ thống ngoài, nhóm API, vùng API chưa phủ
├── events.md            sự kiện, thông báo, job
├── nfr-baseline.md      số liệu phi chức năng hiện có
├── product-direction.md định hướng, tenant, sản phẩm so sánh
└── corner-checklist.md  góc thường bị bỏ sót của sản phẩm
```

Hai phần nằm ngoài `domain/` nhưng thuộc về sản phẩm: `memory/project.md` chứa bài học riêng của sản phẩm, và `intents/` chứa các yêu cầu của sản phẩm. `memory/team.md` chứa bài học dùng chung cho mọi sản phẩm, như cách đánh phiên bản, cách đặt câu hỏi, cách viết PRD; file này đi theo engine.

Engine, gồm file stage, lệnh, checklist và `AGENTS.md`, không ghi cứng dữ kiện sản phẩm, kể cả tên sản phẩm; các file này trỏ về `domain.md` theo số mục. Vì vậy thay domain không làm thay đổi engine. Lệnh `/new-domain` dựng khung cho các bước dưới đây; phần cần quyết định vẫn do người phụ trách làm.

## 2. Tạo repo cho sản phẩm

Mỗi sản phẩm dùng một repo riêng, tương ứng với khái niệm space của AWS. Repo `po-workflow` tại https://github.com/buidhui/po_workflow chỉ chứa engine và tài liệu chung: `domain/` và `intents/` để trống, `memory/project.md` là bản trống. Engine được phát triển và kiểm thử ở repo này; repo sản phẩm không sửa engine.

1. Clone repo engine sang thư mục mới, đặt tên theo sản phẩm, ví dụ `git clone https://github.com/buidhui/po_workflow.git crm-po-workflow`.
2. Đổi tên remote `origin` thành `engine` bằng `git remote rename origin engine`. Remote này dùng để lấy bản engine mới.
3. Tạo repo mới cho sản phẩm trên GitHub, thêm làm remote `origin`, push nhánh `main`. Giữ `.github/workflows/gitleaks.yml` để quét thông tin nhạy cảm mỗi lần push.
4. Mở Claude Code tại thư mục gốc của repo mới, chạy `/new-domain` và làm tiếp từ mục 3.

Lấy bản engine mới bằng `git pull engine main`, sau đó làm theo mục Nâng cấp của bản đó trong `CHANGELOG.md`, gồm chạy `po-tools.py migrate` khi bản đó yêu cầu. Repo sản phẩm chỉ thêm file trong `domain/`, `intents/` và `memory/project.md`, nên lần pull không chạm phần của sản phẩm.

## 3. Thu thập nguồn sống

Quy trình chỉ vận hành đúng khi knowledge base bám vào nguồn thật. Trước khi viết knowledge base, liệt kê nguồn và phân loại:

| Loại nguồn | Ví dụ | Xếp vào |
|---|---|---|
| Tài liệu người dùng cuối | User guide, help center, trang tài liệu trực tuyến | Nguồn sống nếu còn được cập nhật |
| Cấu trúc dữ liệu | Schema cơ sở dữ liệu, ERD, data dictionary | Nguồn sống |
| Đặc tả API | Swagger, OpenAPI, Postman | Nguồn sống; nguồn tốt nhất cho field |
| Bảng sự kiện, thông báo, mail | Danh sách mail tự động, sự kiện hệ thống | Bản chốt nếu không còn file gốc |
| Rule nghiệp vụ chưa có văn bản | Ghi chép từ PO, Dev | Bản chốt, ghi rõ người cung cấp |

Mỗi nguồn ghi vào `domain.md` mục 2 với đường dẫn hoặc link, loại nguồn và ngày đối chiếu. Nguồn sống được đọc lại khi yêu cầu chạm tới vùng liên quan hoặc khi quá 30 ngày kể từ lần đối chiếu cuối; với bản chốt, AI hỏi PO khi có nghi ngờ.

## 4. Dựng knowledge base cùng AI

Knowledge base là bản chắt lọc từ nguồn. Mỗi file trả lời ba câu hỏi: có gì, ràng buộc gì, chạm vào đâu. Danh sách file, nội dung tối thiểu, mức bắt buộc và mức sẵn sàng ở `engine/standards/domain-kb.md` mục 2, 3 và 7; template ở `engine/templates/domain/`. Tên file giữ như chuẩn để lệnh tra được; file module được đánh số tự do vì stage tra theo bản đồ KB ở `domain.md` mục 3.

AI dựng từng file theo năm bước:

1. Người phụ trách đưa AI một nguồn và chỉ định file knowledge base cần viết. AI chắt lọc nội dung, mỗi rule một mã.
2. Rule có trong tài liệu chính thức hoặc đã được PO duyệt mang mã `BR-<MODULE>-NN`; rule AI trích từ văn xuôi và chưa được duyệt mang mã `KB-<MODULE>-NN`. Mỗi rule ghi loại định nghĩa hoặc hành vi, theo `engine/standards/domain-kb.md` mục 4.
3. Điểm nguồn không đề cập thì ghi `❓PO`; AI không tự điền.
4. PO duyệt từng file; duyệt xong thì ghi ngày đối chiếu vào `domain.md` mục 2.
5. Vùng chưa phủ ghi ở `00-index.md`, vùng API chưa phủ ghi ở `integrations.md`, để Impact Analysis không kết luận "không ảnh hưởng" ở vùng chưa có thông tin.

Tham khảo khối lượng: knowledge base của sản phẩm đầu tiên áp dụng quy trình gồm 16 file, khoảng 27.700 từ, chắt lọc từ 57 trang tài liệu người dùng, 85 bảng dữ liệu và 708 operation API, và phủ khoảng một nửa hệ thống.

## 5. Điền manifest

`domain.md` có sáu mục; `/new-domain` dựng khung và hỏi người phụ trách để điền.

1. Sản phẩm và phạm vi: tên, portal, ràng buộc tenant, vai người dùng, thiết bị hỗ trợ, mức accessibility mặc định để stage 2.3 không phải hỏi lại ở mỗi intent. Frontmatter có các khoá `product`, `company`, `code`, `names`, `jira_project_key`, `jira_project_name`, `jira_project_type`:
   - `code` là mã sản phẩm theo danh mục của công ty, dùng trong mã tính năng `<code>-F<NNN>` cho mọi team; mã này được xác định khi dựng domain và không ghi cứng trong engine.
   - `names` là các tên sản phẩm và công ty mà engine không được chứa.
   - Ba khoá Jira là dự án Jira nhận Story List. Script điền ba khoá này vào ba cột đầu của Story List; thiếu thì `doctor` cảnh báo.
   - Hai khoá tuỳ chọn cho đường đẩy qua Jira MCP: `jira_story_type` là tên loại issue cho story, mặc định `Story`; `jira_epic_mode` là cách gắn Epic, `parent` với dự án Jira Cloud dùng trường parent, `epic-link` với dự án còn trường Epic Link, mặc định `parent`. `doctor` báo lỗi khi `jira_epic_mode` sai giá trị.

   ```yaml
   jira_project_key: ABC
   jira_project_name: Tên dự án trên Jira
   jira_project_type: software
   jira_story_type: Story
   jira_epic_mode: parent
   ```

2. Nguồn sống và bản chốt, kèm ngày đối chiếu và phiên bản nguồn.
3. Bản đồ KB: file nào trả lời câu gì, dùng ở stage nào; vùng chưa phủ; quy ước mã.
4. Dữ kiện cho từng stage: file knowledge base đọc ở 1.1 và 1.4; sản phẩm so sánh mặc định cho 1.2; knowledge base và ví dụ cho 2.3; thực thể dùng chung, hệ thông báo, phân quyền, luồng tự sinh, tenant cho 2.31; nguồn field cho 2.42; nơi lưu tài liệu người dùng và nhóm người đọc cho User Guide.
5. Ví dụ dùng trong engine, để lệnh dùng chung có ví dụ đúng với sản phẩm.
6. Thành phần của domain pack.

Mục 4 quyết định chất lượng của từng stage. Mỗi stage chỉ đọc phần của mình trong mục này, nên thiếu phần nào thì stage tương ứng chạy thiếu dữ kiện.

## 6. Viết lại corner checklist

Chép `engine/knowledge/corner-checklist-aws.md` thành `domain/corner-checklist.md`, giữ phần "Cách dùng", thay toàn bộ phần "Điều kiện theo bề mặt" bằng các góc của sản phẩm mới. Nên đưa vào những corner case từng gây lỗi thật hoặc chắc chắn sẽ gặp: trạng thái kết thúc, người dùng bị khoá, dữ liệu cũ trước ngày bật tính năng, thao tác hàng loạt, hai người thao tác cùng lúc. Stage 2.3 và 2.42 quét theo file này.

## 7. Template và công cụ của công ty

Template artifact thuộc engine: PRD theo `engine/templates/prd.md`, cơ sở ở `engine/standards/adr/0004-template-prd-chuan.md`; User Guide theo `engine/templates/user-guide.md`. Domain không chứa template. Bản chính thức của mọi tài liệu là file trong git theo tag của bản đã duyệt.

Công ty muốn đăng bản đọc ra wiki hoặc công cụ tài liệu riêng thì tự thêm lệnh ở repo sản phẩm, ngoài thư mục `engine/`, và ghi nơi đăng ở khoá `published` trong frontmatter của artifact; `po-tools.py status` báo khi bản đăng lệch phiên bản. Template riêng của công ty, nếu có, chỉ dùng làm bảng ánh xạ khi đăng và không thay template của engine.

## 8. Chuẩn bàn giao cho các team

Chuẩn trong `engine/standards/` áp dụng nguyên vẹn cho sản phẩm mới. Các việc sau phải làm riêng cho từng sản phẩm:

1. Xác định mã sản phẩm `code` trong `domain.md` cùng người quản lý danh mục sản phẩm của công ty. Mã phải khác mã của mọi sản phẩm khác, vì mã tính năng `<code>-F<NNN>` đi vào story trên Jira, test case, tên nhánh và commit của mọi team. Số tính năng bắt đầu từ `F001`.
2. Thống nhất với Design, Tech và QA rằng PRD, ba file thiết kế ở 2.43, Decision Brief và story trên Jira là đầu vào chính thức. Template của ba file thiết kế nằm ở `engine/templates/`; team đã có mẫu riêng thì đối chiếu và đề xuất sửa template của engine. Kiểm lại dự án Jira khai ở mục 5 với người quản trị Jira.
3. Gửi các PIC ba chuẩn: `engine/standards/id-conventions.md` về mã, `engine/standards/naming-conventions.md` về tên nhánh, commit, tag test, frame Figma, và `engine/standards/handoff-rules.md` về quy tắc bàn giao. Phần áp dụng trong repo và công cụ của từng team có hiệu lực khi Tech PIC và QA PIC đồng ý.
4. Cấp quyền ghi repo cho Design PIC, Tech PIC, QA PIC và quyền đọc cho Dev. Trước khi cấp, rà `domain/` và `intents/` để loại tài khoản môi trường thử nghiệm và thông tin nhạy cảm.
5. Việc chia và theo dõi nằm trên Jira theo `engine/standards/adr/0002-story-tren-jira.md`; repo chỉ giữ file CSV theo phiên bản PRD và, khi đẩy qua MCP, `jira-map.json`. Muốn đẩy qua MCP thì cài Jira MCP cho Claude Code và cấp quyền tạo, sửa issue trong dự án.

## 9. Chạy thử

1. Mở Claude Code tại thư mục gốc của repo, chạy `python3 engine/scripts/po-tools.py doctor`, gõ một câu bất kỳ, chạy lại `doctor` và kiểm dòng Hook ghi lượt PO đã Đạt.
2. Chạy `/new-intent` với một yêu cầu nhỏ, profile S, đi tới PRD. Mục tiêu là kiểm stage tra đúng knowledge base và manifest; PRD chưa cần hoàn chỉnh.
3. Kiểm `po-tools.py status` báo khớp và `po-tools.py doctor` không còn dòng Lỗi.
4. Chạy một intent profile M qua 2.43 để kiểm vòng viết thiết kế và ký Decision Brief của các PIC, sau đó sinh Story List bằng `/po-stories`, import thử lên Jira và kiểm `po-tools.py dor`.
5. Bài học đầu tiên được ghi vào `memory/project.md` qua câu hỏi tại gate; bài học đúng cho mọi sản phẩm thì chuyển sang `memory/team.md`.

## 10. Checklist domain đã sẵn sàng

- [ ] `domain.md` đủ sáu mục, mục 4 có đủ các stage
- [ ] `domain.md` mục 2 có bảng nguồn kèm ngày đối chiếu; `00-index.md` có mục vùng chưa phủ
- [ ] Mỗi file knowledge base đã được PO duyệt
- [ ] `corner-checklist.md` viết theo sản phẩm mới, không còn ví dụ của sản phẩm trước
- [ ] Đủ knowledge base tối thiểu theo `engine/standards/domain-kb.md` mục 7; `doctor` không cảnh báo dòng KB tối thiểu và bản đồ KB
- [ ] Thông tin ở bảng mục 6 của chuẩn knowledge base đã có, hoặc phần thiếu đã ghi ở vùng chưa phủ
- [ ] `memory/project.md` trống, `intents/` trống, `memory/team.md` giữ nguyên
- [ ] `python3 engine/scripts/po-tools.py doctor` không còn dòng Lỗi. Lệnh kiểm `domain.md` đủ sáu mục, knowledge base tối thiểu, file trong bản đồ KB, template và checklist của mọi stage, và engine không chứa tên nào trong khoá `names`
- [ ] Hook ghi lượt PO đã chạy trên máy của mỗi PO
- [ ] Mã sản phẩm `code` đã xác định và không trùng sản phẩm khác; các PIC đã nhận chuẩn bàn giao và có quyền ghi repo
- [ ] Frontmatter `domain.md` có `jira_project_key` và `jira_project_name`; `doctor` không cảnh báo dòng Dự án Jira
- [ ] Đã chạy thử một intent S tới PRD, `po-tools.py status` khớp
