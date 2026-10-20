# Checklist: 2.4 User Stories

- [ ] **[BLOCK]** Mỗi US là một mục tiêu hoàn chỉnh của một vai, theo `engine/standards/story-splitting.md` mục 1
- [ ] **[BLOCK]** Không US nào chia theo màn hình, theo tầng kỹ thuật, theo từng business rule, hoặc là việc kỹ thuật thuần, theo mục 7 của nguyên tắc
- [ ] Mọi vai trong story thuộc danh sách vai của `domain.md` mục 1, hoặc được khai báo là vai mới
- [ ] US viết một câu tự nhiên theo vai, có vế "để ...". Tên có chữ "và" nối hai việc đã tách, hoặc thẻ ghi lý do giữ
- [ ] Đã xét dấu hiệu quá lớn ở mục 4 của nguyên tắc: hơn một vai hưởng giá trị, luồng hơn 7 bước, gồm cả cấu hình và sử dụng, chạm hơn 2 module. Story giữ dấu hiệu thì thẻ ghi lý do
- [ ] Không có story quá nhỏ: mỗi story có giá trị riêng và kiểm được độc lập
- [ ] **[BLOCK]** Mọi FR có US, hoặc Deferred, N/A kèm lý do. Không GAP khi mở gate
- [ ] Mọi US gắn một Unit. Unit đổi so với 1.4 có lý do
- [ ] Từ ba Unit có sơ đồ phụ thuộc Unit, phụ thuộc một chiều, khớp cột Phụ thuộc của bảng
- [ ] US chưa làm vẫn định nghĩa, ghi rõ
- [ ] Đánh số `US1`, `US2` liên tục. Mã không đánh lại
- [ ] **[BLOCK]** Mỗi US đủ thẻ chín mục, mục không có ghi "không có". Luồng chính ba đến bảy bước ở mức hành vi
- [ ] Thẻ đọc độc lập được: người viết PRD hiểu luồng, rule và vùng chạm mà không cần mở requirements
- [ ] Thẻ không có acceptance criteria, validate theo field, kiểu dữ liệu, mô tả UI
- [ ] Rule đã biết dẫn mã FR, BR, KB; dữ liệu và vùng chạm khớp Impact Matrix
- [ ] Thẻ nguồn. Assumptions & Open Questions có
- [ ] Reviewer ai-reviewer đã chạy
