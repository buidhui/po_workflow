---
intent: <slug>
artifact: tech-design
feature: <mã tính năng>
owner: <Tech PIC, chịu trách nhiệm cả file và duyệt Decision Brief>
contributors: <người viết phần Backend, người viết phần Frontend, nếu khác Tech PIC>
version: 0.1
status: draft
inputs: <prd@1.0, ux-design@0.1>
---
# Tech Design: <Tên tính năng>

<Tech PIC viết cùng người phụ trách Backend và Frontend, từ PRD đã duyệt và danh sách màn của ux-design, trỏ về mã trong PRD. Tương ứng các stage của AWS: 2.6 Domain Design, 2.8 Contract Design, 3.1 Functional Design, gồm `frontend-components.md` khi tính năng có giao diện, và 3.3 NFR Design. Phía nào không bị chạm thì ghi "Không đổi" kèm lý do, không xoá mục. Xoá dòng hướng dẫn khi viết.>

## 1. Thành phần bị chạm

| Phía | Service, ứng dụng hoặc repo | Thay đổi | US |
|---|---|---|---|
| Backend | | | |
| Frontend | | | |

<Tuỳ chọn: sơ đồ thành phần, mỗi service hoặc ứng dụng một nút, mũi tên theo phụ thuộc, theo `engine/standards/diagrams.md`.>

## 2. Quyết định kỹ thuật

<Mỗi quyết định theo dạng ADR: bối cảnh, phương án đã xét, chọn gì, hệ quả; ghi quyết định thuộc Backend, Frontend hay cả hai.>

## 3. Hợp đồng giữa Frontend và Backend

<Điểm nối để hai phía làm song song. Theo 2.8 Contract Design của AWS: đặc tả OpenAPI hoặc AsyncAPI để trong repo của Dev, bảng dưới tóm tắt và trỏ về mã PRD. Mã lỗi khớp câu thông báo ở bảng giao diện của PRD. Tích hợp nhiều bước thì thêm sơ đồ tuần tự.>

| Operation | Phương thức và đường dẫn, hoặc tên sự kiện | Phục vụ US, BR | Mã lỗi và câu thông báo | Phân quyền |
|---|---|---|---|---|

## 4. Backend

### Dữ liệu
<Entity mới hoặc đổi, quan hệ, chỉ mục, dữ liệu cần giữ lịch sử; chuyển đổi dữ liệu cũ theo các dòng TR ở PRD mục 8. Tuỳ chọn sơ đồ `erDiagram`.>

### Xử lý nghiệp vụ
<Service, job định kỳ, hàng đợi, sự kiện phát ra; nơi kiểm business rule và phân quyền; giao dịch; chống xử lý trùng khi gọi lại; ghi nhật ký cho thao tác nhạy cảm.>

## 5. Frontend

### Màn và component
<Theo danh sách màn `SCR` của ux-design, theo `frontend-components` của AWS 3.1: cây component, component dùng lại từ design system, component mới.>

| SCR | Route | Component chính | Dùng lại hay mới | US |
|---|---|---|---|---|

### Trạng thái và dữ liệu phía client
<State của từng màn và nơi giữ: trong component, store dùng chung, cache; cách đồng bộ với API; trạng thái đang tải, rỗng, lỗi, không có quyền. Đối tượng có vòng đời ở PRD mục 4 thì màn hiển thị đúng các trạng thái của sơ đồ.>

### Validate và thông báo
<Validate phía client theo bảng giao diện của PRD; validate nào chỉ làm ở Backend; câu thông báo lấy nguyên từ PRD.>

### Hiệu năng, accessibility, đa ngôn ngữ
<Phân trang, tải dần, kích thước gói tải; mức accessibility theo `domain.md` mục 1; chuỗi hiển thị và đa ngôn ngữ.>

## 6. Đáp ứng business rule, NFR và yêu cầu chuyển đổi

| Mã | Đáp ứng ở | Cách đáp ứng | Ghi chú |
|---|---|---|---|
| | Backend, Frontend hoặc cả hai | | |

<Mỗi BR, NFR, TR trong PRD một dòng. Rule kiểm ở Frontend thì Backend vẫn kiểm lại.>

## 7. Cỡ Unit và kế hoạch thực hiện

| Unit | Gồm US | Phần việc Backend | Phần việc Frontend | Độ lớn ước lượng | Vừa một sprint? | Đề xuất |
|---|---|---|---|---|---|---|

<Mỗi Unit ở PRD mục 5 một dòng; mỗi Unit là một story trên Jira. Vừa một sprint ghi Có hoặc Không. Unit không vừa một sprint hoặc chưa độc lập thì đề xuất tách, gộp hoặc chuyển US sang Unit khác, theo `engine/standards/story-splitting.md` mục 8; US quá lớn để làm trong một sprint thì ghi theo mục 4. Backend và Frontend làm song song thì nối qua hợp đồng ở mục 3; phần việc của từng phía thành sub-task trên Jira.>

## 8. Ý kiến về PRD

| Mã | Lập trường | Nội dung | Lý do |
|---|---|---|---|

<Lập trường: Đồng ý, Đề xuất sửa, Phản đối. Không có ý kiến thì ghi một dòng "Đồng ý với PRD bản <version>".>

## 9. Rủi ro và câu hỏi cần trả lời

| # | Nội dung | Cần ai trả lời | Chặn |
|---|---|---|---|

<Rủi ro mới thì ghi vào sổ rủi ro trong `decisions.md` với mã `RK<n>`, ở đây trỏ mã.>
