# Checklist: 2.3 Requirements Analysis

## Tra KB trước khi hỏi
- [ ] **[BLOCK]** Mỗi hạng mục đã tra theo bản đồ KB trong `domain.md`: đã có chưa, rule hiện có, Hidden, sự kiện và mail, vùng KB chưa phủ
- [ ] Yêu cầu trùng thứ đã có được nêu ngay, kèm mã KB
- [ ] Chạm dữ liệu: nguồn sống đã đọc lại nếu quá một tháng kể từ Last verified
- [ ] Vùng KB chưa phủ ghi `❓PO`, không kết luận "chưa có" hay "không ảnh hưởng"

## FR, NFR
- [ ] **[BLOCK]** Mỗi FR kiểm chứng được, có mã ổn định, ưu tiên, cờ Existing, New, Changed, nguồn
- [ ] **[BLOCK]** Không có FR mô tả bảng, endpoint, thuật toán. FR mô tả điều phải đúng
- [ ] NFR có chỉ số đo được. NFR chưa có chỉ số không bị bỏ: ghi OQ để PO chốt chỉ số
- [ ] Constraints ghi hằng số cứng hay cấu hình

## Góc
- [ ] Mỗi góc áp dụng trong `corner-checklist.md` của domain đã thành FR, assumption có lý do, hoặc out of scope
- [ ] Đã xét ba mục trong Completeness Checklist của AWS: audit log cho thao tác nhạy cảm; lưu giữ và xoá dữ liệu; accessibility và thiết bị. Mức accessibility và thiết bị lấy mặc định ở `domain.md` mục 1, chỉ hỏi khi intent khác mặc định

## Câu hỏi và nguồn
- [ ] Không hỏi kỹ thuật cho Dev. Chỉ hỏi câu đổi phạm vi hoặc rule
- [ ] Câu chặn đã trả lời. Nguyên văn
- [ ] **[BLOCK]** Thẻ nguồn ở mọi khối. Assumptions & Open Questions có cờ Chặn và owner
- [ ] Sources read có Last verified và mục chưa tra được

## Giao
- [ ] Reviewer ai-reviewer đã chạy ở M, L
- [ ] Profile S: PRD rút gọn là stage kế, không chạy 2.31
