# Checklist: Generate User Guide

## Tiền điều kiện
- [ ] **[BLOCK]** PRD của intent có `status: approved`
- [ ] **[BLOCK]** Tính năng đã dev xong; User Guide mô tả cái đang chạy

## Phân bài
- [ ] Mỗi đối tượng người dùng một bài riêng, hậu tố theo đối tượng, không gộp
- [ ] Đối tượng khớp `domain.md` mục 4 phần User Guide

## Cấu trúc
- [ ] Đủ bốn mục theo `engine/templates/user-guide.md`: Thông tin chung · Các bước thực hiện · Lưu ý và quy tắc nghiệp vụ · Lỗi thường gặp
- [ ] **[BLOCK]** Có Module chính và Module liên quan
- [ ] Có điều kiện trước khi bắt đầu: quyền, dữ liệu cần có trước
- [ ] Mỗi bước một hành động; mỗi thao tác có dòng kết quả

## Giọng văn và nội dung
- [ ] **[BLOCK]** Không còn tên bảng, field kỹ thuật, endpoint, mã rule
- [ ] Business rule khớp PRD, đã dịch sang ngôn ngữ người dùng cuối
- [ ] Out of scope của PRD không đưa vào
- [ ] Mục 4 có lỗi thật, lấy từ validate, disable, tooltip, câu thông báo của bảng giao diện

## Ảnh
- [ ] Viewport 1920×1080, headless; tên file `NN-<role>-<mô-tả>.png`
- [ ] Ảnh đã copy về `user-guide/screenshots/` trong intent, không để trong thư mục tạm
- [ ] Không chụp được thì có `<!-- ẢNH: … -->` và `pending-screenshots.md`

## Sau khi viết
- [ ] Đã trình PO review
- [ ] **[BLOCK]** Đã cập nhật KB `domain/` theo `engine/standards/domain-kb.md` mục 5: trạng thái tính năng sang Active, rule, field, quan hệ module khớp sản phẩm thật, nguồn là PRD nào
- [ ] `state.md` có dòng Log
