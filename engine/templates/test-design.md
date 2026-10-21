---
intent: <slug>
artifact: test-design
feature: <mã tính năng>
owner: <QA PIC>
version: 0.1
status: draft
inputs: <prd@1.0>
---
# Test Design: <Tên tính năng>

<QA PIC viết từ PRD đã duyệt, trỏ về mã trong PRD. AWS không có bước thiết kế test trước khi code; gần nhất là việc quality agent kiểm tính kiểm thử được của AC ở 2.4 và hướng dẫn test ở 3.6 Build and Test. Test case chi tiết viết trên Jira, mã `TC`. Xoá dòng hướng dẫn khi viết.>

## 1. Phạm vi và chiến lược
<Loại test: chức năng, hồi quy, tích hợp, hiệu năng, bảo mật; môi trường; phần không test và vì sao.>

## 2. Phủ tiêu chí chấp nhận
| AC | Cách kiểm | Dữ liệu cần | Ưu tiên |
|---|---|---|---|

<Mỗi AC trong PRD một dòng. AC không kiểm thử được ghi ở mục 5. PRD có vòng đời trạng thái thì thêm bảng phủ chuyển trạng thái: mỗi mũi tên trong sơ đồ của PRD ít nhất một ca, cộng ca cho chuyển trạng thái không hợp lệ, theo `engine/standards/diagrams.md` mục 3.>

## 3. Vùng hồi quy
<Tính năng có sẵn bị chạm, lấy từ Impact Matrix của intent.>

## 4. Dữ liệu và môi trường
<Dữ liệu cần dựng, tài khoản, cấu hình, hệ ngoài cần giả lập.>

## 5. Ý kiến về PRD
| Mã | Lập trường | Nội dung | Lý do |
|---|---|---|---|

<AC không kiểm thử được, thiếu nhánh lỗi hoặc giá trị biên, corner case PRD chưa nói, BR mơ hồ. Lập trường: Đồng ý, Đề xuất sửa, Phản đối.>

## 6. Rủi ro và câu hỏi cần trả lời
| # | Nội dung | Cần ai trả lời | Chặn |
|---|---|---|---|
