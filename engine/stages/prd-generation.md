# 2.42 PRD Generation

| | |
|---|---|
| Stage | 2.42 PRD Generation |
| Slug | prd-generation |
| Thư mục | `inception/prd` |
| Phase | inception |
| Plugin | `po-workflow` |
| Lệch so với AWS | Stage thêm của PO-Workflow, không có trong AWS. Đánh số thập phân để chen giữa stage gốc; cơ chế plugin của AWS chỉ cho đánh số sau stage cuối của phase. Các team đọc PRD và thiết kế ở 2.43; QA góp ý tính kiểm thử được của tiêu chí chấp nhận trong `test-design.md`, thay cho việc quality agent của AWS kiểm ở 2.4 |
| Execution | always |
| Lead | product |
| Produces | `inception/prd/prd.md` · `field-intake-questions.md` · `traceability.md` · `verification/phase-check-inception.md` |
| Consumes | `stories.md` đã approve (M, L bắt buộc) · `intent-statement.md` · `scope-document.md` · `requirements.md` · `impact-matrix.md` · `solution-options.md` · `decisions.md` · `design/` và Figma · KB, API spec và schema theo `domain.md` mục 4 phần 2.42 |
| Requires | user-stories ở M, L. requirements-analysis ở S |
| Profiles | S, M, L |
| Reviewer | ai-reviewer |
| Summary confirmation | Field Intake, bắt buộc ở mọi profile |
| Template | `engine/templates/prd.md` · `engine/templates/traceability.md`. Template PRD chuẩn, cơ sở ở ADR 0004 |
| Checklist | `engine/verification/prd-generation.md` |
| Knowledge | KB theo Impact Matrix · `corner-checklist.md` của domain khi viết business rule, tiêu chí chấp nhận và trường hợp ngoại lệ · product: `requirements-guide.md`, `user-story-patterns.md` §Given/When/Then |

Chạy theo `engine/protocol/stage-protocol.md`.

## Mục đích
Tài liệu yêu cầu chi tiết, đầu vào để Design, Tech, QA thiết kế ở 2.43. Mục 1 tới 5 tóm tắt artifact đã duyệt của Ideation và Inception. Mục 6 viết chi tiết từng US. Mục 7 tới 10 gom yêu cầu phi chức năng, yêu cầu chuyển đổi, giả định và câu hỏi mở. PRD chỉ chứa yêu cầu; thiết kế của các team nằm ở file riêng. Plugin stage; AWS coi PRD là đầu vào, không sinh, nên cấu trúc PRD lấy theo thành phần của các artifact AWS, xem ADR 0004.

## Load
M, L: thiếu stories approved thì dừng. S: dùng requirements và inputs.

## Ask là Field Intake, Consolidated Summary của stage
Tra trước khi hỏi, để phân biệt field đã tồn tại với field thật sự mới:
1. Impact Matrix: entity và màn bị chạm.
2. File data model theo `domain.md`: bảng, khoá ngoại.
3. API spec, nguồn field ghi trong `domain.md` mục 4 phần 2.42: field hiện có, kiểu, required, enum.
4. KB theo module: rule chi phối.
5. Phân loại mỗi màn: A là màn mới hoàn toàn, B là màn có sẵn được sửa, C là màn chỉ đọc.
Một bảng duy nhất trong `field-intake-questions.md`: Màn · Field · Hiện có? · Kiểu · Bắt buộc · Giá trị hợp lệ · Validate · Rule chi phối · Ghi chú. Điền sẵn `[đề xuất]` từ KB và API spec; `❓PO` ở điểm không suy được. Màn danh sách hỏi thêm filter, search, sort, pagination, cột hiển thị. Field hiện có chỉ hỏi delta và migration.
PO duyệt bảng là xác nhận tóm tắt. `❓PO` chưa quyết thành OQ, không tự điền. S cũng phải qua bước này, đây là bước dễ sai nhất kể cả với yêu cầu nhỏ.

## Generate
`prd.md` theo template PRD chuẩn `engine/templates/prd.md`:
- Mục 1 tới 5 tóm tắt từ artifact đã duyệt, không viết nội dung mới: Vấn đề, Bằng chứng, Mục tiêu, Các bên liên quan từ `intent-statement.md`; Tiêu chí thành công từ bảng mục tiêu của `intent-statement.md`, mỗi tiêu chí có mã `SC<n>`, chỉ số và nguồn dữ liệu, giá trị hiện tại, giá trị mục tiêu, thời điểm đo, người đo, mục tiêu nó phục vụ; dữ liệu đo do hệ thống sinh ra thì có FR hoặc NFR tương ứng; Ngoài phạm vi từ `scope-document.md`; Giải pháp tổng thể từ `solution-options.md` nếu có; Units từ `stories.md`. Ràng buộc nghiệp vụ cho cách làm chỉ ghi điều phải đúng; hướng kỹ thuật do Tech PIC viết ở `tech-design.md` tại 2.43. S: viết từ requirements.
- Bảng thông tin: mã tính năng, PO, ba PIC, Epic, Figma, tài liệu liên quan. Trạng thái và người duyệt không ghi trong thân PRD; frontmatter và `state.md` giữ hai thông tin này.
- Mục 6, mỗi US mười mục con theo template: User story kèm dòng Ưu tiên Must, Should hoặc Could lấy từ `stories.md`, thêm lý do khi không phải Must; Tiền điều kiện, nêu US khác phải xong trước bằng mã `US<n>`; Luồng chính; Business rule mã `BR<US>.<n>` theo BABOK 10.9: câu khẳng định về nghiệp vụ, độc lập với cách hệ thống thực hiện, ghi loại Định nghĩa hay Hành vi và mức áp dụng của rule hành vi; rule dùng cho nhiều US đặt ở mục 4 với mã `BR0.<n>`, US chỉ trỏ tới; rule chạm tính năng có sẵn dẫn mã KB; Tiêu chí chấp nhận; Giao diện và validate, dạng A hoặc B, cột Màn hình ghi tên màn, mã màn do Design PIC đặt ở `ux-design.md` tại 2.43, cột Yêu cầu đủ định dạng, placeholder, options, mặc định, disable, tooltip, validate, câu thông báo, hành vi; Dữ liệu; NFR riêng của US nếu có; Trường hợp ngoại lệ; Ngoài phạm vi của US. Viết liên tục, không dừng giữa từng US, trừ US rủi ro cao.
- Một dữ kiện ghi ở một nơi: câu thông báo và validate ở bảng giao diện, luật ở business rule; tiêu chí chấp nhận trỏ về hai nơi đó bằng mã, không chép lại câu chữ.
- Tiêu chí chấp nhận, theo `engine/standards/id-conventions.md` và kỹ thuật Acceptance and Evaluation Criteria của BABOK (10.1): mã `AC<US>.<n>`, ổn định, không đánh lại. Mỗi tiêu chí có một dòng tên tình huống kèm BR mà nó kiểm, sau đó ba dòng con Given, When, Then; thêm điều kiện hay kết quả thì dùng dòng And. Given là tiền điều kiện và dữ liệu ban đầu, When là đúng một hành động hoặc sự kiện, Then là kết quả quan sát được, có đạt hoặc không đạt. Phủ đủ: Luồng chính và mỗi nhánh đáng kể có ít nhất một tiêu chí; mỗi US có ít nhất một tiêu chí cho nhánh lỗi hoặc bị từ chối; mỗi ngưỡng số có tiêu chí ở giá trị biên; mỗi BR có ít nhất một tiêu chí trỏ tới; mỗi chuyển trạng thái của mục 4 có ít nhất một tiêu chí; NFR đo được thì thành tiêu chí. Validate của một màn gom thành một tiêu chí trỏ về bảng giao diện. Không viết tiêu chí cho điều không kiểm được. QA viết test case từ danh sách này, mỗi tiêu chí ít nhất một test case.
- Trường hợp ngoại lệ: đi qua Impact Matrix mục Coverage Gaps và `corner-checklist.md` của domain, gắn mỗi góc vào US nó chạm. Mỗi góc kết thúc bằng một trong ba cách: có luật, ghi mã BR hoặc AC; chuyển thành câu hỏi mở ở mục 10; hoặc ghi vào Ngoài phạm vi của US. US không có góc nào thì ghi "Không có góc nào từ Impact Matrix chạm US này". QA bổ sung góc ở `test-design.md`.
- Mục 7 Yêu cầu phi chức năng: NFR áp cho cả tính năng lấy từ `requirements.md`, giữ mã `NFR<n>`, mỗi NFR có chỉ số đo; NFR riêng của một US ghi trong US và liệt kê mã US ở bảng.
- Mục 8 Chuyển đổi và triển khai, yêu cầu loại transition theo BABOK 2.3: lấy từ Impact Matrix mục Transition và mục Tenant, giữ mã `TR<n>`: dữ liệu hiện có, cách bật, chạy song song, quay lui, tenant và cấu hình, hướng dẫn người dùng và vận hành. Điểm Impact Matrix chỉ đề xuất mà PO chưa quyết ghi `[đề xuất]`.
- Mục 9 Giả định: điều PRD đang coi là đúng mà chưa kiểm chứng, như cách vận hành suy ra chưa khảo sát hay ngưỡng chỉ số chưa có số liệu nền, kèm hệ quả nếu sai.
- Mục 10 Câu hỏi mở: câu chưa có câu trả lời, gắn người trả lời và việc bị chặn. Khi trình duyệt, PRD còn tối đa 3 chỗ `❓PO`.
- Mã tính năng: frontmatter `feature:` và hàng Mã tính năng ở bảng thông tin, lấy từ `intent.md`. PRD dùng mã ngắn `US1`, `AC1.1`, `BR1.1`; story trên Jira dùng mã đầy đủ do script đổi.
- Mục 5 Units lấy từ `stories.md`, có cột Tên, Gồm US, Ưu tiên, Phụ thuộc. Mỗi Unit là một story trên Jira; mỗi US thuộc đúng một Unit. `po-tools.py check` báo US chưa thuộc Unit nào, US nằm trong hai Unit, hoặc Unit ghi US không có trong PRD.
- Điểm chưa chắc, M và L: PRD viết trước khi các team thiết kế, nên điểm phụ thuộc thiết kế hay kỹ thuật mà artifact đã duyệt chưa nói thì viết đề xuất đánh dấu `[đề xuất]` và ghi câu hỏi mở gắn tên PIC tương ứng ở mục 10. Các team trả lời trong file thiết kế ở 2.43; Decision Brief gom lại để quyết. Không tự quyết cách làm kỹ thuật thay Dev.
- Mục 4 có thêm ba phần tuỳ chọn: Quy tắc nghiệp vụ dùng chung `BR0.<n>`; Quy tắc tính toán, mỗi công thức ít nhất ba ví dụ có một ví dụ ở giá trị biên; Quyền theo vai theo BABOK 10.39, bắt buộc khi có từ hai vai hoặc Impact Matrix ghi vùng phân quyền từ Medium, mỗi ô Không mà người dùng chạm được có tiêu chí cho nhánh bị từ chối.
- Vòng đời trạng thái trong mục 4, bắt buộc khi tính năng có đối tượng đổi trạng thái mà người dùng thấy, như đơn, lớp, chứng chỉ, yêu cầu duyệt: mỗi đối tượng một bảng chuyển trạng thái với cột Trạng thái hiện tại, Sự kiện, Ai kích hoạt, Điều kiện, Trạng thái sau, Hệ quả, và một sơ đồ trạng thái vẽ từ bảng theo `engine/standards/diagrams.md` mục 3. Mỗi chuyển trạng thái có ít nhất một tiêu chí chấp nhận ở US liên quan; chuyển trạng thái bị cấm là tiêu chí cho nhánh lỗi. Chỉ mức nghiệp vụ, không thiết kế bảng dữ liệu; lấy phần nghiệp vụ của `functional-design-guide.md` bên AWS.
- Sơ đồ theo `engine/standards/diagrams.md`: sơ đồ trạng thái bắt buộc ở Vòng đời trạng thái; sơ đồ phụ thuộc ở mục 5 khi có từ ba Unit; sơ đồ luồng ở Luồng chính khi có từ hai điểm rẽ nhánh. Bảng là nguồn chính, sơ đồ vẽ từ bảng; sơ đồ trạng thái dùng `stateDiagram-v2`, sơ đồ luồng và phụ thuộc dùng `flowchart`.
- Frontmatter: `inputs:` ghi version của stories, requirements, impact-matrix và artifact khác đã dùng; `services:` liệt kê service hoặc repo code bị chạm theo Impact Matrix; Tech PIC ghi danh sách đúng ở `tech-design.md` mục 1, lệch thì Decision Brief nêu và PO sửa dòng này qua change request. Agent của Dev lọc PRD theo dòng này, xem `po-tools.py index`.
- Mục 11 Truy vết: bảng FR, US, BR trong PRD; `traceability.md` với trạng thái OK, GAP, ORPHAN, Deferred, N/A.
Quy tắc cố định: không có mục Database và API; không sequence diagram, cấu trúc bảng, thuật toán, thư viện; hằng số ghi rõ cứng hay cấu hình; field hiện có không được mô tả như mới; không tự thêm field; mục tuỳ chọn không áp dụng xoá hẳn; không giữ dòng mẫu của template; dọn dấu vết quy trình; không viết tắt; dấu `·` giữa các mã.
Profile S: PRD rút gọn gồm frontmatter, bảng thông tin, Lịch sử phiên bản, mục 1 với Vấn đề và Mục tiêu, mục 3, mục 6 với một US, mục 8 nếu có dữ liệu cũ hoặc cần bật theo đợt, mục 10. Bỏ mục 2, 4, 5, 7, 9, 11.

## Verify
1. Checklist.
2. Truy vết: chạy `python3 engine/scripts/po-tools.py trace intents/<slug> --write`. Script dựng `traceability.md`, gồm cả lớp BR sang AC, và năm dòng đầu của `verification/phase-check-inception.md`; AI kiểm dòng 7 đến 9 theo `engine/templates/phase-check.md`. Dòng 6 về lượt duyệt Decision Brief chỉ áp với profile M, L và điền ở 2.43. Có GAP hoặc ORPHAN thì sửa trước gate. Không chạy được python thì làm tay theo template.
3. Reviewer ai-reviewer.

## Gate
Trình: từng US một dòng kèm ưu tiên; BR mới và rule hiện có bị chạm; field, bảng, mail bị ảnh hưởng; điểm `[đề xuất]` kèm OQ gắn PIC; mục đã xoá và vì sao; kết quả truy vết; finding review; OQ. Request Changes trỏ mã cụ thể, ví dụ `US2 BR2.3`, sửa nhắm đích. Approve bằng `po-tools.py approve`: lần duyệt đầu prd lên 1.0, lần sau tăng số phụ; script chụp archive và in tên tag gợi ý. Sau khi commit thì gắn tag và chạy `po-tools.py index --write` để cập nhật bảng chỉ mục.
Profile M, L: stage kế là 2.43 Design Alignment, giao ba team viết file thiết kế từ PRD vừa duyệt; Story List sinh sau 2.43. Profile S: chạy `/po-stories` để sinh Story List cho Jira; phần PO của intent hoàn tất, `/generate-user-guide` sau khi Dev xong, và cập nhật ngược KB.
