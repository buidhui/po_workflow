---
intent: <slug>
phase: <ideation | inception>
date: <YYYY-MM-DD>
result: <Đạt | Không đạt>
---
# Phase check: <IDEATION | INCEPTION> · <slug>

Kiểm ranh giới phase trước khi mở gate cuối của phase. Giữ bảng của phase đang kiểm, xoá bảng kia. Không đạt thì sửa stage tương ứng trước, không mở gate.

## Ideation sang Inception, kiểm ở 1.7; profile M kiểm ở gate chung của 1.1 và 1.4
| # | Điều kiện | Kết quả | Chi tiết |
|---|---|---|---|
| 1 | Mọi objective trong intent-statement có ít nhất một hạng mục In scope phục vụ | Đạt / Không đạt | |
| 2 | Mọi Unit truy về một objective | | |
| 3 | Out of scope không mâu thuẫn In scope | | |
| 4 | Câu hỏi mở có cờ Chặn đã đóng, hoặc chuyển thành assumption có lý do | | |
| 5 | Mọi khối khẳng định có thẻ nguồn | | |

## Inception, kiểm ở gate cuối của phase: 2.43 với profile M, L; 2.42 với profile S
Ở 2.42, mọi profile: chạy `python3 engine/scripts/po-tools.py trace <intent-dir> --write`, script điền năm dòng đầu; AI kiểm dòng 7 đến 9. Profile M, L: dòng 6 ghi "Chờ 2.43" ở 2.42; trước gate 2.43, AI điền dòng 6 và cập nhật Kết luận.
| # | Điều kiện | Kết quả | Chi tiết |
|---|---|---|---|
| 1 | Mọi FR có US, hoặc Deferred, N/A có lý do | | |
| 2 | Mọi US truy về FR có thật | | |
| 3 | Mọi US làm đợt này có trong PRD | | |
| 4 | Mọi BR thuộc một US có trong PRD | | |
| 5 | Mọi BR có AC trỏ tới | | |
| 6 | M, L: Decision Brief ở 2.43 đủ chữ ký, hoặc Accept as-is có DEC | | |
| 7 | Conflict trong Impact Matrix đều có DEC | | |
| 8 | Field Intake không còn `❓PO` chưa chuyển thành OQ | | |
| 9 | Câu hỏi mở có cờ Chặn đã đóng | | |

## Kết luận
<Đạt: mở gate. Không đạt: liệt kê stage phải sửa và vì sao.>
