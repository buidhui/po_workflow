# Checklist: Change Request

## Ghi nhận
- [ ] **[BLOCK]** Đã phân loại: chạm stage đã `[x]` mới đi đường CR
- [ ] `CR<n>` có trong bảng Change requests của `decisions.md`, kèm DEC ghi nguyên văn PO
- [ ] **[BLOCK]** Mọi artifact sẽ sửa đã chụp `pre-CR<n>` vào `archive/`

## Điểm re-entry
- [ ] **[BLOCK]** Lấy stage thấp nhất bị sai lệch, không lấy stage dễ sửa nhất
- [ ] **[BLOCK]** PO đã xác nhận impact preview: stage mở lại, artifact đổi, gate duyệt lại

## Chế độ sửa
- [ ] **[BLOCK]** Chỉ sửa phần bị chạm, không viết lại cả artifact
- [ ] Version frontmatter tăng; Lịch sử phiên bản có dòng `CR<n>`, PRD theo template cũ dùng bảng Document version
- [ ] PRD chỉ chạm US bị ảnh hưởng; frontmatter `status` về `draft` cho tới khi duyệt lại
- [ ] `state.md`: stage mở lại và stage sau bị chạm đã về `[R]` hoặc `[ ]`
- [ ] Reviewer đã chạy ở stage có reviewer theo profile

## Tác động ngược
- [ ] `po-tools.py trace` không GAP, không ORPHAN
- [ ] Đã kiểm business rule mồ côi, mã tham chiếu gãy, Out of scope lỗi thời

## Sau duyệt
- [ ] Archive bản mới, CR đóng trong bảng, Versions trong `state.md` cập nhật
- [ ] Artifact bàn giao đã publish lại Lark nếu trước đó đã lên
