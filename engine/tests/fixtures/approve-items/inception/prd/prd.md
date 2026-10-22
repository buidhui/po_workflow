---
intent: approve-items
artifact: prd
feature: LMS-F913
version: 1.1
status: draft
---
# [PRD] Báo cáo doanh thu

# 6. User stories

## US1: Xuất báo cáo doanh thu theo tháng

### User story

Là quản lý, tôi cần xuất báo cáo doanh thu theo tháng, để đối soát.

**Ưu tiên:** Must

### Business rule

- `BR1.1` Báo cáo chỉ gồm đơn đã thanh toán.

### Tiêu chí chấp nhận

- `AC1.1` Đơn chưa thanh toán · Theo `BR1.1`
  - Given tháng có một đơn chưa thanh toán
  - When quản lý xuất báo cáo tháng đó
  - Then báo cáo không có đơn chưa thanh toán
