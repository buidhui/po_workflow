---
intent: alignment
artifact: prd
feature: LMS-F910
version: 1.0
status: approved
approved_at: 2026-10-10T09:00
---
# [PRD] Nhắc lịch học trong ứng dụng

# Specific Requirement

## US1: Cài đặt nhắc lịch

### 1/ User story

Là học viên, tôi chọn thời điểm nhận nhắc trước buổi học.

**Ưu tiên:** Must

### 4/ Acceptance criteria

**Tiêu chí chấp nhận**

- `AC1.1` Khi học viên chọn nhắc trước 30 phút và lưu, buổi học sau nhận nhắc đúng 30 phút trước giờ học. Theo `BR1.1`
- `AC1.2` Khi học viên nhập số phút lớn hơn 1440, hệ thống báo lỗi và không lưu. Theo `BR1.1`

**UI / UX / Rule UX / Rule UI**

| Màn hình | Giao diện | Field | Yêu cầu |
| --- | --- | --- | --- |
| Cài đặt nhắc | Ô số | Số phút | Từ 5 đến 1440 |

**Business requirement — Business rule**

- `BR1.1` Thời điểm nhắc từ 5 đến 1440 phút trước giờ học

## US2: Tắt nhắc cho một lớp

### 1/ User story

Là học viên, tôi tắt nhắc cho một lớp mà tôi không cần nhắc.

**Ưu tiên:** Should

### 2/ Pre - Condition

- US1 đã xong

### 4/ Acceptance criteria

**Tiêu chí chấp nhận**

- `AC2.1` Khi học viên tắt nhắc cho lớp A, buổi học của lớp A không còn nhắc. Theo `BR2.1`
- `AC2.2` Khi học viên đã bị khoá khỏi lớp, lớp đó không hiện trong danh sách tắt nhắc. Theo `BR2.1`

**Business requirement — Business rule**

- `BR2.1` Tắt nhắc áp cho lớp đang học
