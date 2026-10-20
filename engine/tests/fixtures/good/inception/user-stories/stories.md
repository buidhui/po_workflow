---
intent: good
artifact: stories
version: 0.2
status: draft
inputs: requirements@1.0
---
# User Stories: Nhắc lịch học

## Danh sách
| US | User story, một câu theo vai | Vai | Unit | MoSCoW | FR nguồn | Đợt này? |
|---|---|---|---|---|---|---|
| US1 | Là học viên, tôi nhận email nhắc trước buổi học để không quên giờ học | Học viên | U1 | Must | FR1.1 | Có |
| US2 | Là học viên, tôi nhận thông báo trong ứng dụng trước giờ học | Học viên | U1 | Should | FR1.2 | Có |

### US1: Nhắc qua email
- Vai và mục tiêu: học viên muốn được nhắc qua email để không quên buổi học [FR1.1]
- Bối cảnh: học viên đã ghi danh vào lớp có lịch học; hệ thống tự kích hoạt theo lịch [2.3 Q1]
- Luồng chính: hệ thống tìm buổi học bắt đầu sau 24 giờ, gửi email nhắc, ghi nhận đã gửi [FR1.1]
- Nhánh đáng kể: buổi học bị huỷ thì không gửi [Q1]
- Rule đã biết: FR1.1 nhắc trước 24 giờ [FR1.1]
- Dữ liệu và vùng chạm: lịch học, email học viên, một mail nhắc mới [2.3 Q1]
- Ngoài phạm vi của US này: không có
- Phụ thuộc: không có
- Chưa rõ: không có

### US2: Nhắc trong ứng dụng
- Vai và mục tiêu: học viên muốn thấy thông báo trong ứng dụng trước giờ học [FR1.2]
- Bối cảnh: học viên đang dùng ứng dụng trong ngày có buổi học [2.3 Q1]
- Luồng chính: hệ thống tìm buổi học bắt đầu sau 1 giờ, đẩy thông báo, học viên bấm để mở lớp [FR1.2]
- Nhánh đáng kể: buổi học bị huỷ thì không đẩy thông báo [Q1]
- Rule đã biết: FR1.2 nhắc trước 1 giờ [FR1.2]
- Dữ liệu và vùng chạm: lịch học, thông báo trong ứng dụng [2.3 Q1]
- Ngoài phạm vi của US này: không có
- Phụ thuộc: US1 dùng chung bộ tìm buổi học [suy ra]
- Chưa rõ: không có

## FR sang US
| FR | US | Trạng thái: OK, GAP, Deferred, N/A | Ghi chú |
|---|---|---|---|
| FR1 | US1, US2 | OK | qua FR con |
| FR1.1 | US1 | OK | |
| FR1.2 | US2 | OK | |
| FR2 | - | Deferred | Sang đợt 2 theo DEC1 |

## Units
| Unit | Gồm US | Phụ thuộc | Release độc lập? | Ghi chú |
|---|---|---|---|---|
| U1 | US1, US2 | không | Có | |
Thứ tự gợi ý: U1. Dev chốt thứ tự thật.

## Assumptions & Open Questions
| # | Nội dung | Loại | Chặn | Owner |
|---|---|---|---|---|
| A1 | Học viên mở email trong ngày | [assumption] | không | PO |
