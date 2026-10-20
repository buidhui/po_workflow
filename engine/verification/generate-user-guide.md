# Checklist: Generate User Guide

## Tiền điều kiện
- [ ] **[BLOCK]** PRD của intent có `status: approved`
- [ ] **[BLOCK]** Tính năng đã dev xong; User Guide mô tả cái đang chạy

## Phân bài
- [ ] Chạm cả hai hệ thì hai bài riêng `-student` và `-ops`, không gộp
- [ ] Đặt đúng repo và đối tượng theo `domain.md` mục 4 phần User Guide

## Cấu trúc
- [ ] Đủ bốn mục: I. Thông tin chung · II. Hướng dẫn chi tiết · III. Lưu ý và quy tắc nghiệp vụ · IV. Lỗi thường gặp
- [ ] **[BLOCK]** Có khai báo `Phạm vi & Module liên quan`: module chính, chức năng chính, module liên quan
- [ ] Có `Điều kiện tiên quyết`: quyền, dữ liệu cần có trước
- [ ] Đúng cú pháp của công cụ tài liệu ghi trong `domain.md` mục 4 phần User Guide, theo template của domain

## Giọng văn và nội dung
- [ ] **[BLOCK]** Không còn tên bảng, field kỹ thuật, endpoint, mã rule
- [ ] Business rule khớp PRD, đã dịch sang ngôn ngữ người dùng cuối
- [ ] Out of scope của PRD không đưa vào
- [ ] Mục IV có lỗi thật, lấy từ validate, disable, tooltip của bảng UI

## Ảnh
- [ ] Viewport 1920×1080, headless; tên file `NN-<role>-<mô-tả>.png`
- [ ] Ảnh đã copy về `user-guide/screenshots/` trong intent, không để trong thư mục tạm
- [ ] Không chụp được thì có `<!-- ẢNH: … -->` và `pending-screenshots.md`

## Sau khi viết
- [ ] Đã trình PO review
- [ ] **[BLOCK]** Đã cập nhật ngược KB `domain/`: rule mới, field đổi, quan hệ module mới, mã `KB-*`, nguồn là PRD nào
- [ ] `state.md` có dòng Log
