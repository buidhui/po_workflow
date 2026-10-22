---
intent: approve-items
artifact: prd
feature: LMS-F913
version: 1.0
status: approved
---
# [PRD] Báo cáo doanh thu

# 6. User stories

## US1: Đổi mật khẩu khi đã đăng nhập

### Business rule

- `BR1.1` Nếu mật khẩu cũ sai thì từ chối.

### Tiêu chí chấp nhận

- `AC1.1` Sai mật khẩu cũ · Theo `BR1.1`
  - Given học viên đã đăng nhập
  - When nhập sai mật khẩu cũ
  - Then hệ thống báo lỗi

## US2: Xem lịch sử đăng nhập

### Business rule

- `BR2.1` Chỉ hiện 30 ngày gần nhất.

### Tiêu chí chấp nhận

- `AC2.1` Quá 30 ngày · Theo `BR2.1`
  - Given có lượt đăng nhập 40 ngày trước
  - When mở lịch sử
  - Then không thấy lượt đó
