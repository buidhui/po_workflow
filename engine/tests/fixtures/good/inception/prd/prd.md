---
intent: good
artifact: prd
feature: LMS-F901
version: 0.1
status: draft
services: reminder-svc, notification-svc
---
# [PRD] Nhắc lịch học

# Specific Requirement

## US1: Nhắc qua email

### 1/ User story

Là học viên, tôi nhận email nhắc trước buổi học để không quên giờ học.

**Ưu tiên:** Must

### 2/ Pre - Condition

- Học viên đã ghi danh vào lớp có lịch học

### 3/ Scenario

Hệ thống tìm buổi học bắt đầu sau 24 giờ, gửi email nhắc, ghi nhận đã gửi.

### 4/ Acceptance criteria

**Tiêu chí chấp nhận**

- `AC1.1` Khi còn 24 giờ tới buổi học chưa bị huỷ, học viên nhận một email nhắc. Theo `BR1.1`
- `AC1.2` Khi buổi học bị huỷ trước giờ gửi, học viên không nhận email nhắc. Theo `BR1.1`

**Business requirement — Business rule**

- BR1.1 Email nhắc gửi trước giờ học 24 giờ, chỉ cho buổi học chưa bị huỷ

### 5/ Out of scope

- Nhắc qua SMS

### 6/ Conner case

## US2: Nhắc trong ứng dụng

### 1/ User story

Là học viên, tôi nhận thông báo trong ứng dụng trước giờ học.

**Ưu tiên:** Should

### 4/ Acceptance criteria

**Tiêu chí chấp nhận**

- `AC2.1` Khi còn 1 giờ tới buổi học, học viên thấy thông báo trong ứng dụng. Theo `BR2.1`
- `AC2.2` Khi còn hơn 1 giờ tới buổi học, học viên không thấy thông báo. Theo `BR2.1`

**Business requirement — Business rule**

- BR2.1 Thông báo hiện trước giờ học 1 giờ
