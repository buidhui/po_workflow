---
intent: <slug>
artifact: tech-design
feature: <mã tính năng>
owner: <Tech PIC>
version: 0.1
status: draft
inputs: <prd@1.0>
---
# Tech Design: <Tên tính năng>

<Tech PIC viết từ PRD đã duyệt, trỏ về mã trong PRD. Tương ứng 2.6 Domain Design, 2.8 Contract Design, 3.1 Functional Design và 3.3 NFR Design của AWS. Xoá dòng hướng dẫn khi viết.>

## 1. Thành phần bị chạm
| Service hoặc repo | Thay đổi | US |
|---|---|---|

## 2. Quyết định kỹ thuật
<Mỗi quyết định: bối cảnh, phương án đã xét, chọn gì, hệ quả. Dạng ADR.>

## 3. Dữ liệu
<Entity mới hoặc đổi, quan hệ, migration dữ liệu cũ.>

## 4. API và hợp đồng giữa thành phần <!-- tuỳ chọn -->
<Endpoint mới hoặc đổi, sự kiện, hợp đồng với hệ ngoài.>

## 5. Đáp ứng business rule và NFR
| Mã | Cách đáp ứng | Ghi chú |
|---|---|---|

<Mỗi BR và NFR trong PRD một dòng.>

## 6. Unit of work, thứ tự và độ lớn
| Unit of work | Gồm US | Phụ thuộc | Độ lớn ước lượng |
|---|---|---|---|

<Story nào quá lớn để làm trong một sprint thì ghi ở đây, theo `engine/standards/story-splitting.md` mục 4.>

## 7. Ý kiến về PRD
| Mã | Lập trường | Nội dung | Lý do |
|---|---|---|---|

<Lập trường: Đồng ý, Đề xuất sửa, Phản đối. Không có ý kiến thì ghi một dòng "Đồng ý với PRD bản <version>".>

## 8. Rủi ro và câu hỏi cần chốt
| # | Nội dung | Cần ai trả lời | Chặn |
|---|---|---|---|
