---
intent: <slug>
artifact: ux-design
feature: <mã tính năng>
owner: <Design PIC>
version: 0.1
status: draft
inputs: <prd@1.0>
---
# UX Design: <Tên tính năng>

<Design PIC viết từ PRD đã duyệt, trỏ về mã trong PRD. Tương ứng 2.5 Refined Mockups của AWS: mockups, interaction-spec, design-system-mapping, accessibility-checklist. Xoá dòng hướng dẫn khi viết.>

## 1. Danh sách màn
| SCR | Tên màn | Mới hoặc sửa | US | Figma |
|---|---|---|---|---|
| SCR1 | | | US1 | |

<Mỗi US có bảng giao diện trong PRD phải có ít nhất một màn. Story List lấy mã màn từ bảng này.>

## 2. Luồng và tương tác
<Theo từng US: điều hướng giữa các màn, hành vi khi thao tác, trạng thái rỗng, lỗi, đang tải, không có quyền. Khuyến nghị sơ đồ luồng màn: mỗi nút là một màn có mã `SCR`, nhãn mũi tên là thao tác người dùng. PRD có vòng đời trạng thái thì màn hiển thị trạng thái phải khớp các trạng thái trong sơ đồ của PRD. Theo `engine/standards/diagrams.md`.>

## 3. Thành phần giao diện <!-- tuỳ chọn -->
<Component dùng lại từ design system, component mới, biến thể.>

## 4. Accessibility
<Mức theo `domain.md` mục 1. Điểm cần lưu ý: tương phản, thao tác bằng bàn phím, nhãn cho trình đọc màn hình, cỡ chữ.>

## 5. Ý kiến về PRD
| Mã | Lập trường | Nội dung | Lý do |
|---|---|---|---|

<Lập trường: Đồng ý, Đề xuất sửa, Phản đối. Không có ý kiến thì ghi một dòng "Đồng ý với PRD bản <version>".>

## 6. Rủi ro và câu hỏi cần trả lời
| # | Nội dung | Cần ai trả lời | Chặn |
|---|---|---|---|
