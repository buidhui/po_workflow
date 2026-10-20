# Đưa một sản phẩm mới vào quy trình

Tài liệu này dành cho người phụ trách quy trình và mô tả việc làm một lần khi đưa quy trình sang một sản phẩm hoặc công ty khác. Thao tác hằng ngày của PO ở [USER-GUIDE.md](USER-GUIDE.md); phương pháp ở [README.md](README.md).

## 1. Hai tầng của repo

Engine là phần không phụ thuộc sản phẩm: protocol, lệnh, template chung, checklist, agent, script, chuẩn bàn giao, gói kiến thức vai PO từ AWS. Domain pack là mọi thứ riêng của sản phẩm và công ty, nằm trọn trong một thư mục:

```
domain/
├── domain.md                      manifest: sản phẩm, nguồn, bản đồ KB, dữ kiện cho từng stage
├── 00-index.md, 01-<module>.md …  knowledge base của sản phẩm
├── corner-checklist.md            góc hay sót, viết lại theo nghiệp vụ của domain
└── templates/
    ├── user-guide.md              template User Guide theo chuẩn tài liệu của công ty
    └── prd.md                     chỉ khi công ty bắt buộc template PRD riêng; ghi đè template chuẩn
```

Hai phần nằm ngoài thư mục đó nhưng thuộc về domain, phải làm mới khi đổi domain: `memory/project.md` chứa bài học riêng của sản phẩm hiện tại, và `intents/` chứa việc của sản phẩm hiện tại. `memory/team.md` là bài học dùng chung cho mọi sản phẩm, như cách đánh version, cách hỏi, cách viết PRD và publish; file này đi theo engine, giữ nguyên.

Engine, gồm file stage, lệnh, checklist và `AGENTS.md`, không ghi cứng dữ kiện sản phẩm, kể cả tên sản phẩm; các file này trỏ về `domain.md` theo mục. Vì vậy đổi domain không ảnh hưởng tới engine. Lệnh `/new-domain` dựng khung cho các bước dưới đây; phần cần người quyết định vẫn do người làm.

## 2. Tạo space mới

Mỗi sản phẩm một repo riêng, AWS gọi là một space. Repo `po-workflow` chỉ chứa engine và tài liệu chung: `domain/` và `intents/` để trống, `memory/project.md` là bản trống. Engine được phát triển và kiểm thử ở repo này; repo sản phẩm không sửa engine.

1. Clone repo `po-workflow` sang thư mục mới, đặt tên theo sản phẩm, ví dụ `crm-po-workflow`.
2. Đổi tên remote đang có thành `engine`: `git remote rename origin engine`. Remote này dùng để lấy bản engine mới.
3. Tạo remote mới cho repo sản phẩm, đặt tên `origin`, push nhánh `main`. Giữ `.github/workflows/gitleaks.yml` để quét thông tin nhạy cảm mỗi lần push.
4. Chạy `/new-domain` và làm tiếp từ mục 3.

Lấy bản engine mới: `git pull engine main`, sau đó làm theo mục Nâng cấp của bản mới trong `CHANGELOG.md`, gồm `po-tools.py migrate` khi bản đó yêu cầu. Repo sản phẩm chỉ thêm file trong `domain/`, `intents/` và `memory/project.md`, nên lần pull không đụng phần của sản phẩm. Repo sản phẩm có từ trước khi tách engine ra repo riêng thì không chung lịch sử git với `po-workflow`; lấy bản mới bằng cách chép đè các file có trong `engine/MANIFEST.txt`, theo đầu `CHANGELOG.md`.

## 3. Thu nguồn sống

Quy trình chỉ vận hành được khi KB bám vào nguồn thật. Trước khi viết KB, liệt kê nguồn và phân loại:

| Loại nguồn | Ví dụ | Xếp vào |
|---|---|---|
| Tài liệu người dùng cuối | user guide, help center, GitBook | nguồn sống nếu còn cập nhật |
| Cấu trúc dữ liệu | schema DB, ERD, data dictionary | nguồn sống |
| Đặc tả API | Swagger, OpenAPI, Postman | nguồn sống, là nguồn tốt nhất cho field |
| Bảng sự kiện, thông báo, mail | danh sách mail tự động, event | bản chốt nếu không còn file gốc |
| Rule nghiệp vụ truyền miệng | ghi từ PO, Dev | bản chốt, ghi rõ người cung cấp |

Mỗi nguồn ghi vào `domain.md` mục 2 với đường dẫn hoặc link, loại, ngày đối chiếu. Nguồn sống được đọc lại khi yêu cầu chạm tới vùng đó hoặc quá 30 ngày kể từ lần đối chiếu cuối; bản chốt thì hỏi PO khi nghi ngờ.

## 4. Dựng KB cùng AI

KB là bản chắt lọc từ nguồn. Mỗi file trả lời ba câu hỏi: có gì, ràng buộc gì, chạm vào đâu. Thứ tự và quy ước dưới đây giữ nguyên cho mọi domain để command tra được:

| File | Nội dung | Bắt buộc |
|---|---|---|
| `00-index.md` | mục lục, trạng thái tính năng kể cả Hidden, mục "câu hỏi để sau". Bảng nguồn ghi ở `domain.md` mục 2 | có |
| `01` đến `NN` | mỗi module nghiệp vụ một file: khái niệm, luồng chính, rule có mã, màn, dữ liệu | có |
| `data-model` | bảng, khoá ngoại, quan hệ, shared entity dễ vỡ | có |
| `events` hoặc `mail-events` | sự kiện, thông báo, mail tự động và trạng thái bật tắt | nếu sản phẩm có |
| `api-surface` | nhóm API, vùng chưa phủ, endpoint có nhưng tính năng không có | có |
| `product-direction` | portal, tenant, phần đóng cứng, hướng sản phẩm | có |
| `domain-principles` | quan hệ chứa giữa các thực thể, ranh giới thực thể | có |

Số thứ tự tự do, vì command tra file theo bản đồ KB trong `domain.md` mục 3; tên file phải ghi vào bản đồ này.

Cách làm với AI, từng file một:

1. Đưa AI một nguồn và chỉ định file KB cần viết. AI chắt lọc, mỗi rule một mã.
2. Mã rule: `BR-<MODULE>-NN` khi rule có trong tài liệu chính thức, `KB-<MODULE>-NN` khi AI trích từ văn xuôi và chưa ai duyệt. Hai loại khác nhau về độ tin cậy, không gộp.
3. Điểm nguồn không đề cập thì ghi `❓PO`, không để AI tự điền.
4. PO duyệt từng file; duyệt xong ghi ngày đối chiếu vào `domain.md` mục 2.
5. Ghi rõ vùng KB chưa phủ ngay trong `api-surface`, để Impact Analysis không kết luận "không ảnh hưởng" ở vùng chưa có thông tin.

Về khối lượng: KB của sản phẩm đầu tiên áp dụng quy trình có 16 file, khoảng 27.700 từ, chắt từ 57 trang tài liệu người dùng, 85 bảng và 708 operation, và vẫn chỉ phủ khoảng một nửa hệ thống.

## 5. Điền manifest

`domain.md` có 6 mục; `/new-domain` dựng khung và hỏi PO để điền:

1. Sản phẩm và phạm vi: tên, portal, ràng buộc tenant, vai người dùng, thiết bị hỗ trợ và mức accessibility mặc định để 2.3 không phải hỏi lại mỗi intent. Frontmatter có `product`, `company`, `code`, `names`, và các khoá Jira `jira_project_key`, `jira_project_name`, `jira_project_type`. `code` là mã sản phẩm theo danh mục của công ty, dùng trong mã tính năng `<code>-F<NNN>` cho mọi team; mã này chốt khi dựng domain và không ghi cứng trong engine. `names` là các tên sản phẩm và công ty mà engine không được chứa. `jira_project_key`, `jira_project_name`, `jira_project_type` là dự án Jira nhận Story List, ví dụ:

   ```yaml
   jira_project_key: ABC
   jira_project_name: Tên dự án trên Jira
   jira_project_type: software
   ```

   Script lấy 3 khoá này điền vào 3 cột đầu của Story List; thiếu thì `doctor` cảnh báo
2. Nguồn sống và bản chốt, kèm ngày đối chiếu và phiên bản nguồn
3. Bản đồ KB: file nào trả lời câu gì, dùng ở stage nào; vùng chưa phủ; quy ước mã
4. Dữ kiện cho từng stage: KB đọc ở 1.1 và 1.4; sản phẩm so sánh mặc định cho 1.2; KB và ví dụ cho 2.3; shared entity, hệ thông báo, phân quyền, luồng tự sinh, tenant cho 2.31; nguồn field và template PRD cho 2.42; đích publish; đích User Guide
5. Ví dụ dùng trong engine, để command dùng chung cho mọi domain
6. Thành phần của pack

Mục 4 quyết định chất lượng của từng stage: mỗi stage chỉ đọc phần của mình trong mục này, nên thiếu phần nào thì stage đó chạy thiếu dữ kiện.

## 6. Viết lại corner checklist

Chép `engine/knowledge/corner-checklist-aws.md` thành `domain/corner-checklist.md`, giữ phần "Cách dùng", thay toàn bộ "Điều kiện theo bề mặt" bằng góc của domain mới. Corner case nên đưa vào là loại từng gây lỗi thật hoặc chắc chắn sẽ gặp: trạng thái kết thúc, người dùng bị khoá, dữ liệu cũ trước ngày bật tính năng, thao tác hàng loạt, hai người làm cùng lúc. Stage 2.3 và 2.42 quét theo file này.

## 7. Template của công ty

Template PRD: mặc định dùng template chuẩn `engine/templates/prd.md`, chung cho mọi sản phẩm, nên domain không cần file template PRD. Cơ sở của từng mục và bảng ánh xạ từ template công ty sang template chuẩn ở `engine/standards/adr/0004-template-prd-chuan.md`. Chỉ khi công ty bắt buộc template riêng cho sản phẩm thì đặt file đó ở `domain/templates/prd.md` và ghi tên mục cấm đổi trong `domain.md` mục 4 phần 2.42; file này ghi đè template chuẩn, theo cùng thứ tự với AWS.

Template User Guide: theo cấu trúc tài liệu người dùng mà công ty đang dùng, như GitBook, Confluence, Notion. Đích publish ghi ở `domain.md` phần Publish; nếu không dùng Lark thì `/publish-lark` không áp dụng và cần một lệnh publish khác cho công cụ đó.

## 8. Chuẩn bàn giao cho các team

Chuẩn trong `engine/standards/` áp dụng nguyên vẹn cho sản phẩm mới; chỉ phần sau phải làm cho từng sản phẩm:

1. Chốt mã sản phẩm `code` trong `domain.md` với người quản lý danh mục sản phẩm của công ty. Mã phải khác mã của mọi sản phẩm khác, vì mã tính năng `<code>-F<NNN>` đi vào story trên Jira, test case, tên nhánh và commit của mọi team. Số tính năng bắt đầu từ `F001`.
2. Thống nhất với Design, Tech và QA rằng PRD, ba file thiết kế ở 2.43, Decision Brief và story trên Jira là đầu vào chính thức; template của ba file thiết kế ở `engine/templates/`, team đã có mẫu riêng thì sửa template cho khớp, theo README mục 6. Dự án Jira nhận Story List đã ghi ở frontmatter `domain.md` từ mục 5; kiểm lại với người quản trị Jira. Gửi các PIC `engine/standards/id-conventions.md` và `engine/standards/handoff-rules.md`.
3. Cấp quyền ghi repo cho Design PIC, Tech PIC, QA PIC, và quyền đọc cho Dev. Trước khi cấp, rà `domain/` và `intents/` để loại tài khoản staging và thông tin nhạy cảm.
4. Việc chia và theo dõi nằm trên Jira theo `engine/standards/adr/0002-story-tren-jira.md`; repo chỉ giữ file CSV theo phiên bản PRD. Quy ước mã và quy tắc bàn giao giữ nguyên.

## 9. Chạy thử

1. Chạy `/new-intent` với một yêu cầu nhỏ, profile S, đi tới PRD. Mục tiêu là kiểm tra stage tra đúng KB và manifest, chưa cần PRD hoàn chỉnh.
2. `python3 engine/scripts/po-tools.py status` báo khớp, `po-tools.py doctor` không còn dòng Lỗi.
3. Chạy một intent profile M qua 2.43 để kiểm vòng viết thiết kế và ký Decision Brief của các PIC, sau đó sinh Story List bằng `/po-stories`, import thử lên Jira và kiểm `po-tools.py dor`.
4. Bài học đầu tiên ghi vào `project.md` qua câu hỏi tại gate; bài học đúng cho mọi sản phẩm thì chuyển sang `team.md`.

## 10. Checklist domain đã sẵn sàng

- [ ] `domain.md` đủ 6 mục, mục 4 có đủ các stage
- [ ] `domain.md` mục 2 có bảng nguồn kèm ngày đối chiếu; `00-index.md` có mục vùng chưa phủ
- [ ] Mỗi file KB đã được PO duyệt
- [ ] `corner-checklist.md` viết theo domain, không còn ví dụ của sản phẩm trước
- [ ] Không có `templates/prd.md`, hoặc có vì công ty bắt buộc và tên mục cấm đổi đã ghi ở `domain.md` mục 4 phần 2.42
- [ ] `project.md` trống, `intents/` trống, `team.md` giữ nguyên
- [ ] `python3 engine/scripts/po-tools.py doctor` không còn dòng Lỗi. Lệnh kiểm `domain.md` đủ 6 mục, file Template và Checklist của mọi stage tồn tại, và engine không còn tên nào trong khoá `names` của `domain.md`
- [ ] Mã sản phẩm `code` đã chốt và không trùng sản phẩm khác; các PIC đã nhận chuẩn bàn giao và có quyền ghi repo
- [ ] Frontmatter `domain.md` có `jira_project_key` và `jira_project_name`; `doctor` không cảnh báo dòng Dự án Jira
- [ ] Chạy thử một intent S tới PRD, `po-tools.py status` khớp
