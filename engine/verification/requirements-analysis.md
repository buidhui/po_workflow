# Checklist: 2.3 Requirements Analysis

## Tra KB trước khi hỏi
- [ ] **[BLOCK]** Mỗi hạng mục đã tra theo bản đồ KB trong `domain.md`: đã có chưa, rule hiện có, Hidden, sự kiện và mail, vùng KB chưa phủ
- [ ] Yêu cầu trùng thứ đã có được nêu ngay, kèm mã KB
- [ ] Chạm dữ liệu: nguồn sống đã đọc lại nếu quá một tháng kể từ Last verified
- [ ] Vùng KB chưa phủ ghi `❓PO`, không kết luận "chưa có" hay "không ảnh hưởng"

## FR, NFR
- [ ] **[BLOCK]** Mỗi FR kiểm chứng được, có mã ổn định, ưu tiên, cột Phục vụ, cờ Existing, New, Changed, nguồn
- [ ] Mỗi FR viết theo một mẫu EARS; FR Changed dẫn mã rule KB mà nó đổi
- [ ] Mọi mục tiêu `O<n>` có ít nhất một FR phục vụ, theo BABOK 7.3
- [ ] **[BLOCK]** Không có FR mô tả bảng, endpoint, thuật toán. FR mô tả điều phải đúng
- [ ] NFR có chỉ số đo được. NFR chưa có chỉ số không bị bỏ: ghi OQ để PO chốt chỉ số
- [ ] Constraints ghi hằng số cứng hay cấu hình

## Chất lượng theo BABOK 7.2
- [ ] Đơn nhất: mỗi FR một hành vi; hai hành vi nối bằng "và" đã tách thành FRn.m
- [ ] Không mơ hồ: không dùng từ không đo được như nhanh, dễ, thân thiện, linh hoạt, hợp lý, phù hợp, tối ưu, một số, nếu cần, và/hoặc
- [ ] Nhất quán: không hai FR trái nhau, không trái rule KB mà không ghi là Changed
- [ ] Khả thi, có ưu tiên, dễ hiểu với người không tham gia buổi hỏi

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
