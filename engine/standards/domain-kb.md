# Chuẩn knowledge base của domain

Domain pack chỉ chứa tri thức về sản phẩm. Quy trình, template artifact, chuẩn bàn giao và chuẩn sơ đồ nằm trong engine, dùng chung cho mọi sản phẩm. Knowledge base, gọi tắt là KB, là đầu vào của mọi stage: thiếu KB thì AI phải hỏi PO nhiều hơn, và Impact Analysis dễ kết luận "không ảnh hưởng" ở vùng chưa có thông tin.

Tài liệu này định nghĩa KB cần những gì, để người phụ trách dựng domain biết phải cung cấp gì. Cách làm từng bước ở `DOMAIN-SETUP.md`; template của từng file ở `engine/templates/domain/`.

## 1. Cơ sở

- BABOK v3 9.3 Business Knowledge: người phân tích cần hiểu sản phẩm đang có (solution knowledge), tổ chức (organization knowledge) và ngành (industry knowledge). KB ghi lại ba loại hiểu biết này để AI và PO mới dùng được ngay.
- BABOK v3 6.1 Analyze Current State liệt kê các yếu tố của hiện trạng: nhu cầu, cơ cấu tổ chức, năng lực và quy trình, công nghệ và hạ tầng, chính sách, kiến trúc nghiệp vụ, tài sản nội bộ, yếu tố bên ngoài. Mỗi yếu tố có một file KB ứng với nó ở mục 2.
- BABOK v3 3.4 Plan Business Analysis Information Management: thông tin phân tích được tổ chức, có mức trừu tượng rõ, truy vết được, dùng lại được, lưu ở nơi mọi người truy cập, có thuộc tính như nguồn và trạng thái. Quy ước ở mục 4.
- BABOK v3 5.2 Maintain Requirements: yêu cầu đã hiện thực được giữ lại để dùng cho thay đổi sau. Vòng cập nhật ở mục 5.
- AWS AI-DLC: thư mục `knowledge/` của space để tự do, nhưng stage Reverse Engineering ở 2.1 sinh ra một bộ cố định cho hệ đang chạy: tổng quan nghiệp vụ, kiến trúc, cấu trúc code, tài liệu API, danh mục thành phần, công nghệ, phụ thuộc; glossary đặt ở `knowledge/aidlc-shared/`. Chuẩn này giữ ý đó ở mức nghiệp vụ, vì PO không cần cấu trúc code.

## 2. Thành phần của KB

| File | Trả lời câu gì | Kỹ thuật BABOK | Bắt buộc | Stage đọc |
|---|---|---|---|---|
| `domain.md` | Sản phẩm là gì, vai người dùng, tenant, thiết bị, mã sản phẩm, dự án Jira, nguồn và ngày đối chiếu, bản đồ KB, dữ kiện cho từng stage | 3.4 | Có | Mọi stage |
| `00-index.md` | Sản phẩm có những module và tính năng nào, trạng thái từng tính năng, vùng chưa phủ, câu hỏi để sau | 10.22 Functional Decomposition | Có | Mọi stage |
| `glossary.md` | Mỗi thuật ngữ nghĩa là gì, tên trên giao diện, tên trong dữ liệu, từ dễ nhầm | 10.23 Glossary | Có | 1.1, 2.3, 2.42 |
| `concept-model.md` | Thực thể nghiệp vụ nào chứa thực thể nào, ranh giới giữa chúng, điều không được làm khi mô hình hoá | 10.11 Concept Modelling | Có | 1.1, 2.3, 2.31 |
| `NN-<module>.md` | Mỗi module: làm gì, thực thể và vòng đời, chức năng và màn, business rule, field chính, sự kiện, quan hệ với module khác | 10.22, 10.9 Business Rules Analysis, 10.44 State Modelling | Có, ít nhất các module mà intent đầu tiên chạm | 2.3, 2.31, 2.42 |
| `data-model.md` | Thực thể dữ liệu, quan hệ, khoá, field quan trọng, thực thể dùng chung dễ vỡ | 10.15 Data Modelling, 10.12 Data Dictionary | Có | 2.31, 2.42 |
| `permissions.md` | Vai nào được làm gì trên đối tượng nào, phạm vi dữ liệu theo vai | 10.39 Roles and Permissions Matrix | Có | 2.3, 2.31, 2.42 |
| `integrations.md` | Hệ ngoài nào nối với sản phẩm, chiều dữ liệu, tần suất; nhóm API và vùng API chưa có trong KB | 10.24 Interface Analysis | Có khi sản phẩm có API hoặc tích hợp | 1.4, 2.31, 2.42 |
| `events.md` | Sự kiện, thông báo, email, job định kỳ; cái nào đang bật | 10.24 Interface Analysis | Có khi sản phẩm có | 2.3, 2.31 |
| `nfr-baseline.md` | Số liệu hiện có: số người dùng, khối lượng dữ liệu, thời gian phản hồi, khả dụng, bảo mật, accessibility | 10.30 Non-Functional Requirements Analysis | Khuyến nghị; bắt buộc trước intent đầu tiên có NFR | 2.3, 2.42 |
| `product-direction.md` | Sản phẩm đang đi về đâu, mô hình tenant, phần đang gắn cứng cho một khách hàng, sản phẩm so sánh | 6.2 Define Future State, 10.4 Benchmarking and Market Analysis | Có | 1.1, 1.2, 1.4, 2.31 |
| `corner-checklist.md` | Góc hay bị bỏ sót của sản phẩm này | 10.27 Lessons Learned | Có | 2.3, 2.31, 2.42 |

Tên file giữ như bảng để lệnh tra được. Module đặt số `01`, `02` theo thứ tự tuỳ ý, vì stage tra theo bản đồ KB ở `domain.md` mục 3.

## 3. Nội dung tối thiểu của từng file

Template ở `engine/templates/domain/` có đủ các mục dưới đây.

- `00-index.md`: bảng module với mã module, file, mô tả một dòng, trạng thái; bảng tính năng có trạng thái Hidden, Planned, Deprecated; vùng chưa phủ; câu hỏi để sau.
- `glossary.md`: bảng Thuật ngữ · Định nghĩa · Tên trên giao diện · Tên trong dữ liệu · Từ dễ nhầm · Nguồn.
- `concept-model.md`: sơ đồ khái niệm `flowchart` hoặc `erDiagram` không có kiểu dữ liệu; bảng quan hệ chứa; nguyên tắc mô hình hoá, mỗi nguyên tắc có mã `DP-NN`.
- File module: vị trí trong hệ thống; thực thể và vòng đời, có sơ đồ trạng thái khi thực thể đổi trạng thái; chức năng và màn; business rule; field chính; sự kiện và tích hợp; quan hệ với module khác; tính năng ẩn hoặc đang tắt; vùng chưa rõ; nguồn.
- `data-model.md`: sơ đồ `erDiagram`; bảng thực thể với khoá, quan hệ, số bảng trỏ tới; danh sách thực thể dùng chung dễ vỡ.
- `permissions.md`: ma trận Thao tác × Vai với Được, Không, Có điều kiện; phạm vi dữ liệu theo vai; cơ chế phân quyền của hệ, như vai cố định hay chính sách cấu hình được.
- `integrations.md`: bảng hệ ngoài với chiều dữ liệu, tần suất, ai sở hữu; bảng nhóm API với vùng đã có trong KB và vùng chưa phủ; endpoint có mà tính năng không có.
- `events.md`: bảng sự kiện với mã, khi nào phát sinh, gửi cho ai, kênh, đang bật hay tắt, chạy theo sự kiện hay theo lịch.
- `nfr-baseline.md`: bảng chỉ số theo nhóm hiệu năng, khối lượng, khả dụng, bảo mật, accessibility, với giá trị hiện tại, nguồn số liệu, ngày đo.
- `product-direction.md`: định hướng và lộ trình; mô hình tenant và các câu kiểm chiều tenant; phần đang gắn cứng cho một khách hàng; sản phẩm so sánh.
- `corner-checklist.md`: chép từ `engine/knowledge/corner-checklist-aws.md`, giữ phần Cách dùng, thay danh sách điều kiện bằng góc của sản phẩm.

## 4. Quy ước

- Mã business rule: `BR-<MODULE>-NN` khi rule có trong tài liệu chính thức hoặc đã được PO duyệt; `KB-<MODULE>-NN` khi AI trích từ văn bản và chưa ai duyệt. `<MODULE>` là mã module trong `00-index.md`, không đặt mã theo chủ đề. `NN` hai chữ số, không dùng lại số đã cấp.
- Mỗi rule ghi loại theo BABOK 10.9: định nghĩa, tức ràng buộc dữ liệu hay cách tính; hoặc hành vi, tức điều được phép, bắt buộc, bị cấm. Rule ghi kèm nguồn và trạng thái duyệt.
- Trạng thái tính năng: Active đang dùng; Hidden có code nhưng đang ẩn; Planned PRD đã duyệt, chưa phát hành; Deprecated đã bỏ, dữ liệu còn.
- Điểm nguồn không nói tới ghi `❓PO`, không để AI tự điền.
- Ngày đối chiếu nguồn chỉ ghi ở `domain.md` mục 2, một nơi duy nhất.
- Sơ đồ theo `engine/standards/diagrams.md`.
- Kết luận cũ bị phát hiện sai thì sửa và ghi "đã đính chính" kèm ngày, không xoá dấu vết.

## 5. Vòng cập nhật

1. Khi PRD được duyệt: AI ghi phần thay đổi của tính năng vào file module, `glossary.md`, `data-model.md`, `permissions.md`, `events.md` với trạng thái Planned, dẫn mã tính năng và phiên bản PRD.
2. Khi tính năng phát hành, cùng lúc viết User Guide: đổi Planned thành Active, đối chiếu lại với sản phẩm thật, sửa chỗ Dev làm khác PRD.
3. Khi một intent phát hiện KB sai hoặc thiếu: sửa ngay, ghi ngày ở `domain.md` mục 2 nếu đã đọc lại nguồn.
4. Mỗi quý, hoặc khi `po-tools.py doctor` báo nguồn quá 30 ngày: đọc lại nguồn sống và cập nhật.

## 6. Người phụ trách domain cần cung cấp

| Thông tin | Dùng để dựng | Dạng chấp nhận | Trước intent đầu tiên |
|---|---|---|---|
| Tổng quan sản phẩm: mục tiêu, người dùng, ứng dụng hoặc portal, vai | `domain.md` mục 1 | Văn bản, slide, buổi giới thiệu có ghi chép | Bắt buộc |
| Mã sản phẩm theo danh mục công ty, dự án Jira nhận story | Frontmatter `domain.md` | Mã, key và tên dự án | Bắt buộc |
| Tài liệu người dùng hiện có | File module | User guide, help center, video hướng dẫn | Bắt buộc; không có thì một buổi demo có ghi chép |
| Danh sách module và tính năng, kể cả tính năng ẩn hoặc đang tắt | `00-index.md` | Sitemap, menu, danh sách trên Jira | Bắt buộc |
| Thuật ngữ nghiệp vụ | `glossary.md` | Danh sách sẵn có; không có thì AI dựng nháp từ tài liệu, PO duyệt | Bắt buộc |
| Schema dữ liệu có cột, kiểu, khoá | `data-model.md` | Export schema, ERD, data dictionary | Bắt buộc |
| Đặc tả API | `integrations.md` | OpenAPI, Swagger, Postman | Bắt buộc khi có API |
| Ma trận phân quyền hoặc bản export chính sách phân quyền | `permissions.md` | Bảng vai và quyền, export từ hệ phân quyền | Bắt buộc |
| Danh sách sự kiện, thông báo, email, job định kỳ và trạng thái bật tắt | `events.md` | Bảng cấu hình, danh sách mẫu email | Bắt buộc khi có |
| Hệ thống ngoài và cách tích hợp | `integrations.md` | Sơ đồ kiến trúc, tài liệu tích hợp | Bắt buộc khi có |
| Số liệu vận hành: số người dùng, khối lượng dữ liệu, thời gian phản hồi, SLA | `nfr-baseline.md` | Dashboard giám sát, báo cáo vận hành | Khuyến nghị |
| Định hướng sản phẩm, lộ trình, mô hình tenant | `product-direction.md` | Roadmap, tài liệu chiến lược | Bắt buộc |
| Sản phẩm so sánh, tối đa ba | `product-direction.md`, `domain.md` mục 4 phần 1.2 | Tên và đường dẫn trang trợ giúp | Bắt buộc |
| Sự cố và lỗi từng gặp, góc từng bị bỏ sót | `corner-checklist.md` | Danh sách bug, postmortem, kinh nghiệm của QA | Bắt buộc |
| Nơi lưu tài liệu người dùng và các đối tượng người dùng | `domain.md` mục 4 phần User Guide | Đường dẫn repo hoặc công cụ tài liệu | Khi cần viết User Guide |
| Quyền đọc mã nguồn | Đối chiếu khi tài liệu thiếu | Quyền đọc repo | Tuỳ chọn |

Thông tin nào chưa có thì ghi vào `00-index.md` mục vùng chưa phủ, không chờ đủ mới bắt đầu.

## 7. Mức sẵn sàng

- Tối thiểu để chạy intent đầu tiên: `domain.md` đủ 6 mục; `00-index.md`, `glossary.md`, `concept-model.md`, `data-model.md`, `permissions.md`, `product-direction.md`, `corner-checklist.md`; file module cho mọi module mà intent đầu chạm; vùng chưa phủ ghi rõ.
- Đầy đủ: mọi module có file; `integrations.md`, `events.md`, `nfr-baseline.md` có số liệu; không còn rule `KB-*` chưa duyệt; mọi nguồn sống đối chiếu trong 30 ngày.
- `po-tools.py doctor` kiểm `domain.md` đủ 6 mục, các file bắt buộc ở mục tối thiểu có mặt, mọi file trong bản đồ KB tồn tại, và nguồn sống quá 30 ngày.
