# <NN> · <Tên module>

| | |
|---|---|
| Mã module | <MODULE> |
| Ứng dụng hoặc portal | |
| Đường vào | <Menu → Mục → Màn hình> |
| Trạng thái | Active, Hidden, Planned hoặc Deprecated |
| Nguồn | <tài liệu, trang, mục> |

## 1. Vị trí trong hệ thống
<Module làm gì, ai dùng, nằm ở đâu trong luồng chung của sản phẩm.>

## 2. Thực thể và vòng đời
<Thực thể chính của module. Thực thể đổi trạng thái thì có bảng chuyển trạng thái và sơ đồ `stateDiagram-v2` theo `engine/standards/diagrams.md` mục 3.>

## 3. Chức năng và màn

| Chức năng | Màn | Vai dùng | Ghi chú |
|---|---|---|---|

## 4. Business rule

| Mã | Rule | Loại | Nguồn | Đã duyệt? |
|---|---|---|---|---|
| BR-<MODULE>-01 | | Định nghĩa hoặc Hành vi | | Có |

<Loại theo BABOK 10.9: Định nghĩa là ràng buộc dữ liệu hay cách tính; Hành vi là điều được phép, bắt buộc, bị cấm. Mã `KB-<MODULE>-NN` cho rule AI trích chưa duyệt.>

## 5. Field chính

| Field | Bắt buộc | Kiểu | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|

## 6. Sự kiện và tích hợp
<Sự kiện, thông báo, job, API mà module phát ra hoặc nhận; dẫn mã trong `events.md`, `integrations.md`.>

## 7. Quan hệ với module khác

| Module | Quan hệ | Ghi chú |
|---|---|---|

## 8. Tính năng ẩn hoặc đang tắt <!-- tuỳ chọn -->

## 9. Vùng chưa rõ
<Điểm nguồn không nói tới, ghi `❓PO`.>
