---
intent: check-rules
artifact: prd
feature: LMS-F908
version: 0.1
status: draft
---
# [PRD] Luật kiểm máy

# Database

Bảng reminders.

# Specific Requirement

## US1: Nhắc qua email

### 1/ User story

Là học viên, tôi nhận email nhắc trước buổi học.

### 4/ Acceptance criteria

**Tiêu chí chấp nhận**

- `AC1.1` Khi còn 24 giờ tới buổi học, học viên nhận một email nhắc. Theo `BR1.1`

**UI / UX / Rule UX / Rule UI**

| Màn hình | Giao diện | Field | Yêu cầu |
| --- | --- | --- | --- |
| Cài đặt | Công tắc | Nhắc qua email | Mặc định bật |

**Business requirement — Business rule**

- `BR1.1` Email nhắc gửi trước giờ học 24 giờ
