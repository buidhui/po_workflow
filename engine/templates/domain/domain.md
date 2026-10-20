---
domain: <mã ngắn của domain, chữ thường>
product: <tên sản phẩm>
company: <tên công ty>
code: <mã sản phẩm theo danh mục công ty, dùng trong mã tính năng <code>-F<NNN>>
names: <các tên sản phẩm và công ty mà engine không được chứa, cách nhau bằng dấu phẩy>
jira_project_key: <key dự án Jira nhận Story List>
jira_project_name: <tên dự án Jira>
jira_project_type: software
updated: <YYYY-MM-DD>
---
# Domain: <tên sản phẩm>

Manifest của knowledge base, theo `engine/standards/domain-kb.md`. Engine đọc file này ở đầu mỗi phiên và ở bước Load của mọi stage.

## 1. Sản phẩm và phạm vi
- Sản phẩm: <tên, các ứng dụng hoặc portal, phần nằm ngoài phạm vi>
- Tenant: <một hay nhiều tổ chức dùng chung; hằng số nào phải cấu hình theo tổ chức>
- Vai người dùng: <các vai hay gặp>
- Thiết bị và accessibility mặc định: <ví dụ web máy tính và điện thoại, WCAG 2.1 mức AA>

## 2. Nguồn sống và bản chốt

| Nguồn | Loại | Ở đâu | Đối chiếu lần cuối | Phiên bản nguồn |
|---|---|---|---|---|
| <tài liệu người dùng> | sống | <đường dẫn> | <DD/MM/YYYY> | <commit, ngày build, số trang> |

Nguồn sống được đọc lại khi yêu cầu chạm vùng đó hoặc quá 30 ngày; bản chốt là nguồn không còn file gốc, nghi ngờ thì hỏi PO.

## 3. Bản đồ KB

| File | Trả lời câu gì | Stage dùng |
|---|---|---|
| `00-index.md` | danh mục module, trạng thái tính năng, vùng chưa phủ | mọi stage |
| `glossary.md` | thuật ngữ nghiệp vụ | 1.1, 2.3, 2.42 |
| `concept-model.md` | thực thể nghiệp vụ và quan hệ chứa | 1.1, 2.3, 2.31 |
| `01-<module>.md` | <module> | 2.3, 2.31, 2.42 |
| `data-model.md` | thực thể dữ liệu, quan hệ, thực thể dùng chung | 2.31, 2.42 |
| `permissions.md` | vai và quyền | 2.3, 2.31, 2.42 |
| `integrations.md` | hệ ngoài, nhóm API, vùng API chưa phủ | 1.4, 2.31, 2.42 |
| `events.md` | sự kiện, thông báo, job | 2.3, 2.31 |
| `nfr-baseline.md` | số liệu phi chức năng hiện có | 2.3, 2.42 |
| `product-direction.md` | định hướng, tenant, sản phẩm so sánh | 1.1, 1.2, 1.4, 2.31 |
| `corner-checklist.md` | góc hay sót | 2.3, 2.31, 2.42 |

Vùng KB chưa phủ: <tóm tắt, chi tiết ở `00-index.md`>.

## 4. Dữ kiện cho từng stage

### 1.1 Intent Capture
<file cần đọc để biết yêu cầu thuộc phần nào của sản phẩm>

### 1.2 Market Research
Sản phẩm so sánh mặc định: <tối đa ba>. <cách lấy tài liệu của họ nếu trang chặn tải tự động>

### 1.4 Scope Definition
<vùng chưa phủ, định hướng>

### 2.3 Requirements Analysis
<file module, file sự kiện, file dữ liệu cần đọc; một ví dụ yêu cầu trùng thứ đã có trong sản phẩm>

### 2.31 Impact Analysis
- Thực thể dùng chung dễ vỡ: <từ `data-model.md`>
- Hệ thông báo: <từ `events.md`>
- Phân quyền: <từ `permissions.md`>
- Luồng tự sinh: <nếu có>
- Tính năng ẩn: <từ `00-index.md`>
- Tenant: <các câu kiểm ở `product-direction.md`>

### 2.42 PRD Generation
Nguồn field theo thứ tự tin cậy: <đặc tả API, `data-model.md`, file module>.

### User Guide
Nơi lưu tài liệu người dùng của sản phẩm: <đường dẫn hoặc công cụ>. Đối tượng người dùng, mỗi đối tượng một bài: <danh sách>. Ví dụ đổi giọng từ PRD sang User Guide: <một ví dụ>.

## 5. Ví dụ dùng trong engine
- Change request cần quay lại từ 2.3: <một ví dụ của sản phẩm>
- Câu trả lời nguyên văn kèm chữ cái: <ví dụ>
- Góc hay sót của sản phẩm: <ba tới năm góc>

## 6. Thành phần của domain pack
<danh sách file trong `domain/`, khớp bản đồ KB>
