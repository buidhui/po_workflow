---
intent: <slug>
artifact: stories
version: 0.1
status: draft
inputs: <artifact đầu vào@version, ví dụ requirements@1.0; stage đầu tiên ghi none>
---
# User Stories: <Tên tính năng>

## Danh sách
| US | User story, một câu theo vai | Vai | Unit | MoSCoW | FR nguồn | Đợt này? |
|---|---|---|---|---|---|---|
| US1 | | | U1 | Must | FR1, FR2 | Có |

### US1: <tên>
- Vai và mục tiêu: <ai, muốn làm gì, để được gì> [FR1]
- Bối cảnh: <portal, điểm vào, điều kiện trước, ai hoặc sự kiện nào kích hoạt> [Q2]
- Luồng chính: <ba đến bảy bước ở mức hành vi, người dùng làm gì và hệ thống đáp gì; không mô tả UI, không field> [FR1] [FR2]
- Nhánh đáng kể: <ngoại lệ hay rẽ nhánh làm đổi luồng; góc nhỏ để PRD>
- Rule đã biết: <FR, BR, KB chi phối, mỗi mã kèm một dòng nghĩa>
- Dữ liệu và vùng chạm: <entity, màn, mail, báo cáo, lấy từ Impact Matrix>
- Ngoài phạm vi của US này: <một hai dòng, hoặc "không có">
- Phụ thuộc: <US, Unit khác, hệ ngoài, hoặc "không có">
- Chưa rõ: <câu hỏi gắn vai phải trả lời, hoặc "không có">

<Thẻ đủ để PO viết PRD chi tiết ở 2.42 mà không cần mở lại requirements. Không acceptance criteria, không validate theo field, không kiểu dữ liệu; phần đó ở PRD.>

## Vai trong tính năng <!-- tuỳ chọn -->
| Vai | Mục tiêu trong tính năng | Khó khăn hiện tại | Mức quen công nghệ | Tần suất dùng |
|---|---|---|---|---|
<Chỉ các vai có trong story của intent này, để Design PIC dùng khi thiết kế ở 2.43. Vai mới, chưa có trong `domain.md` mục 1, ghi rõ là vai mới. Theo persona của AWS product-guide.>

## FR sang US
| FR | US | Trạng thái: OK, GAP, Deferred, N/A | Ghi chú |
|---|---|---|---|

## Units
| Unit | Gồm US | Phụ thuộc | Release độc lập? | Ghi chú |
|---|---|---|---|---|
Thứ tự gợi ý: <...>. Dev quyết thứ tự thật.
<Từ ba Unit trở lên: sơ đồ phụ thuộc Unit, `flowchart LR`, mũi tên từ Unit phải có trước tới Unit phụ thuộc, theo `engine/standards/diagrams.md` mục 4. PRD mục 5 chép lại sơ đồ này.>
Thay đổi so với 1.4: <tách, gộp, thêm, vì sao>

## Assumptions & Open Questions
| # | Nội dung | Loại | Chặn | Owner |
|---|---|---|---|---|
