# Checklist: 2.42 PRD Generation

Áp cho PRD theo template chuẩn `engine/templates/prd.md`. PRD đã duyệt theo template cũ, có mục Specific Requirement, chỉ kiểm phần áp được.

## Tiền điều kiện
- [ ] **[BLOCK]** M, L: stories approved. S: requirements approved
- [ ] **[BLOCK]** Field Intake đã PO xác nhận. `❓PO` chưa quyết thành câu hỏi mở

## Mục 1 tới 5
- [ ] Bối cảnh và mục tiêu, Ngoài phạm vi, Giải pháp tổng thể, Units tóm tắt từ artifact đã duyệt, không viết nội dung mới. Ràng buộc nghiệp vụ cho cách làm chỉ có điều phải đúng
- [ ] **[BLOCK]** Mỗi mục tiêu có ít nhất một tiêu chí thành công `SC<n>` đo được, có cách đo và ngưỡng. Ngưỡng chưa có số liệu nền ghi là đề xuất và có giả định ở mục 9. Không còn dòng mẫu
- [ ] Bảng thông tin có mã tính năng, PO, ba PIC, Figma, tài liệu liên quan. Không có trạng thái tài liệu hay người duyệt trong thân PRD
- [ ] **[BLOCK]** Không có mục Database và API. Không sequence diagram, cấu trúc bảng, thuật toán, thư viện

## Mục 6, từng US
- [ ] US đánh số liên tục. US chưa làm ghi rõ trong tiêu đề
- [ ] Mỗi US đủ các mục con bắt buộc: User story, Tiền điều kiện, Luồng chính, Business rule, Tiêu chí chấp nhận, Giao diện và validate, Dữ liệu, Trường hợp ngoại lệ, Ngoài phạm vi của US
- [ ] Mỗi US có dòng Ưu tiên Must, Should hoặc Could, khớp `stories.md`; ưu tiên không phải Must có một câu lý do
- [ ] US phụ thuộc US khác ghi mã `US<n>` ở Tiền điều kiện
- [ ] BR mã `BR<US>.<n>`, không trùng, viết theo một trong năm mẫu EARS của template. Rule chạm tính năng có sẵn dẫn mã KB
- [ ] **[BLOCK]** Mỗi US có danh sách tiêu chí mã `AC<US>.<n>`, không trùng. Mỗi tiêu chí theo cấu trúc Given/When/Then, When chỉ một hành động hoặc sự kiện, Then kiểm được, có đạt hoặc không đạt
- [ ] **[BLOCK]** Mọi BR có ít nhất một tiêu chí trỏ tới. Luồng chính và mỗi nhánh đáng kể có tiêu chí
- [ ] **[BLOCK]** Mỗi US có ít nhất một tiêu chí cho nhánh lỗi hoặc bị từ chối. Mỗi ngưỡng số có tiêu chí ở giá trị biên
- [ ] Bảng giao diện đúng dạng A hoặc B, cột Yêu cầu đủ định dạng, placeholder, options, mặc định, disable, tooltip, validate, câu thông báo, hành vi. Validate của một màn gom thành một tiêu chí trỏ về bảng
- [ ] Một dữ kiện ghi ở một nơi: câu thông báo không chép lại giữa bảng giao diện, BR và tiêu chí chấp nhận
- [ ] **[BLOCK]** Trường hợp ngoại lệ: mọi coverage gap của Impact Matrix đã gắn vào US nó chạm, mỗi góc có luật, câu hỏi mở, hoặc ngoài phạm vi. Mục không trống
- [ ] **[BLOCK]** Frontmatter `feature:` và hàng Mã tính năng có mã tính năng của intent
- [ ] **[BLOCK]** Field hiện có ghi là hiện có. Không tự thêm field
- [ ] **[BLOCK]** Tính năng có đối tượng đổi trạng thái thì mục 4 có Vòng đời trạng thái: bảng chuyển trạng thái và sơ đồ khớp nhau, mọi trạng thái tới được từ nút Bắt đầu, trạng thái cuối nối tới nút Kết thúc. `po-tools.py check` kiểm phần khớp
- [ ] Mỗi chuyển trạng thái có ít nhất một tiêu chí chấp nhận; chuyển trạng thái bị cấm có tiêu chí cho nhánh lỗi
- [ ] Sơ đồ theo `engine/standards/diagrams.md`: dùng `flowchart`, nhãn mũi tên một dòng; từ ba Unit có sơ đồ phụ thuộc; luồng có từ hai điểm rẽ có sơ đồ luồng
- [ ] Hằng số ghi cứng hay cấu hình
- [ ] Sự kiện, mail bị chạm đối chiếu file sự kiện trong KB
- [ ] **[BLOCK]** M, L: điểm phụ thuộc thiết kế hay kỹ thuật mà artifact đã duyệt chưa nói có `[đề xuất]` và câu hỏi mở gắn tên PIC. PRD không quy định cách làm kỹ thuật

## Mục 7 tới 10
- [ ] NFR áp cho cả tính năng có chỉ số đo; NFR riêng của US được liệt kê mã US. Chưa có chỉ số thì có câu hỏi mở
- [ ] **[BLOCK]** Chuyển đổi và triển khai phủ đủ Impact Matrix mục Transition và mục Tenant. Điểm PO chưa quyết ghi `[đề xuất]`
- [ ] Mỗi giả định có hệ quả nếu sai
- [ ] **[BLOCK]** Câu hỏi mở có người trả lời và việc bị chặn. PRD còn tối đa 3 chỗ `❓PO`

## Chất lượng từng yêu cầu, theo ISO/IEC/IEEE 29148 mục 5.2.5 và 5.2.6
- [ ] Mỗi BR và tiêu chí: cần thiết, không mơ hồ, đơn nhất, khả thi, kiểm chứng được, đúng với nguồn
- [ ] Cả PRD: đầy đủ so với `stories.md`, nhất quán giữa các US, không hai luật trái nhau

## Truy vết và review
- [ ] **[BLOCK]** Traceability: không GAP, không ORPHAN. `verification/phase-check-inception.md` đạt; profile M, L để dòng 6 tới 2.43
- [ ] Reviewer ai-reviewer đã chạy, sau `po-tools.py review-start`, và artifact không đổi sau lần review đó

## Bàn giao
- [ ] **[BLOCK]** Không còn chữ mẫu template. Mục tuỳ chọn không áp dụng đã xoá
- [ ] **[BLOCK]** Không dấu vết quy trình. Không viết tắt. Dấu `·` giữa mã
- [ ] Profile S: PRD rút gọn đúng danh mục mục
