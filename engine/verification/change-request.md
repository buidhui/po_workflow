# Checklist: Change Request

## Ghi nhận
- [ ] **[BLOCK]** Đã phân loại: chạm stage đã `[x]` mới đi đường CR
- [ ] `CR<n>` có trong bảng Change requests của `decisions.md`, trạng thái Chờ quyết cho tới khi PO quyết
- [ ] **[BLOCK]** Mọi artifact sẽ sửa đã chụp `pre-CR<n>` vào `archive/`

## Điểm re-entry
- [ ] **[BLOCK]** Lấy stage thấp nhất bị sai lệch, không lấy stage dễ sửa nhất
- [ ] **[BLOCK]** Dòng CR trong `decisions.md` có đủ cột đánh giá: mã bị chạm, mục tiêu bị ảnh hưởng, effort và mốc, độ khẩn; rủi ro mới đã vào sổ rủi ro
- [ ] **[BLOCK]** PO đã quyết Nhận, Hoãn hoặc Bác; quyết định ghi bằng `po-tools.py cr`, có DEC nguyên văn, trước khi chụp archive và sửa artifact
- [ ] **[BLOCK]** PO đã xác nhận impact preview: stage mở lại, artifact đổi, gate duyệt lại

## Chế độ sửa
- [ ] **[BLOCK]** Chỉ sửa phần bị chạm, không viết lại cả artifact
- [ ] Version frontmatter tăng; Lịch sử phiên bản có dòng `CR<n>`, PRD theo template cũ dùng bảng Document version
- [ ] PRD chỉ chạm US bị ảnh hưởng; frontmatter `status` về `draft` cho tới khi duyệt lại
- [ ] `state.md`: stage mở lại đã về `[R]` qua `--reopen` của lệnh `cr`; Open CR có mã CR
- [ ] Reviewer đã chạy ở stage có reviewer theo profile

## Tác động ngược
- [ ] `po-tools.py trace` không GAP, không ORPHAN
- [ ] Đã kiểm business rule mồ côi, mã tham chiếu gãy, Out of scope lỗi thời

## Sau duyệt
- [ ] Approve không còn mã biến mất so với bản duyệt trước, hoặc PO đã quyết từng mã
- [ ] Archive bản mới, Versions trong `state.md` cập nhật, CR đóng bằng `po-tools.py cr ... dong`
- [ ] Bản đăng ngoài repo, nếu có, đã đăng lại theo bản mới
