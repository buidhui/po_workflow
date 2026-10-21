---
intent: alignment
artifact: tech-design
feature: LMS-F910
owner: Bình
version: 0.1
status: draft
inputs: prd@1.0
---
# Tech Design: Nhắc lịch học trong ứng dụng

## 1. Thành phần bị chạm
| Phía | Service, ứng dụng hoặc repo | Thay đổi | US |
|---|---|---|---|
| Backend | reminder-svc | Lưu thời điểm nhắc theo học viên | US1 |
| Frontend | student-app | Thêm mục cài đặt nhắc | US1 |

## 5. Frontend

### Màn và component
| SCR | Route | Component chính | Dùng lại hay mới | US |
|---|---|---|---|---|
| | /settings/reminder | ReminderForm | Mới | US1 |
