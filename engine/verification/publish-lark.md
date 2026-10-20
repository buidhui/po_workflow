# Checklist: Publish Lark

## Tiền điều kiện
- [ ] **[BLOCK]** Frontmatter `status: approved`
- [ ] Lark target đọc từ `intent.md` mục Lark; thiếu đã hỏi và ghi lại
- [ ] Token hết hạn thì hỏi PO cấp quyền lại, không báo "không kết nối được"

## Xác nhận trước khi đẩy
- [ ] **[BLOCK]** Đã trình PO: artifact và version, intent node, tạo mới hay cập nhật
- [ ] Đã cảnh báo nếu References chứa tài khoản staging
- [ ] PO bỏ qua thì không đẩy gì, không coi là lỗi

## Chuyển đổi
- [ ] **[BLOCK]** Fidelity 1:1, không tóm tắt, không gộp mục, không lược dòng
- [ ] Frontmatter YAML đã bỏ
- [ ] Bảng giữ đủ cột và dòng; mã tham chiếu và link giữ nguyên; mục đã xoá không thêm lại
- [ ] Có ảnh thì đã chèn lại theo `order.txt`, hoặc báo rõ ảnh nào chưa chèn

## Idempotent
- [ ] **[BLOCK]** Đã có tài liệu thì overwrite đúng doc cũ, không tạo doc mới
- [ ] **[BLOCK]** Tài liệu nằm trong intent node, không nằm thẳng dưới node cha chung
- [ ] Tên trên Lark giữ nguyên tên PO đã đặt

## Sau khi publish
- [ ] **[BLOCK]** Đã đọc lại và đối chiếu: heading từng cấp, số bảng, số dòng bảng, gạch đầu dòng, bảng trắng bằng số khối mermaid, không còn code block sơ đồ, số ảnh
- [ ] Lệch thật đã báo cụ thể mục nào
- [ ] `intent.md` mục Lark và `state.md` cột Lark đã cập nhật version, token, ngày
