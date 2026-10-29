# 2.43 Design Alignment

| | |
|---|---|
| Stage | 2.43 Design Alignment |
| Slug | design-alignment |
| Thư mục | `inception/decision-brief` |
| Phase | inception |
| Plugin | `po-workflow` |
| Lệch so với AWS | Stage thêm của PO-Workflow. AWS chia thiết kế theo vai thành nhiều stage do agent làm, mỗi stage một gate: 2.5 Refined Mockups, 2.6 Domain Design, 2.8 Contract Design, 3.1 Functional Design theo Unit, 3.6 Build and Test. Ở đây ba team người viết ba file thiết kế từ PRD đã duyệt, AI đối chiếu và viết Decision Brief, một buổi họp chung để quyết định. Test Design viết trước khi code là phần thêm; AWS chỉ kiểm tính kiểm thử được của AC ở 2.4 và viết hướng dẫn test ở 3.6. Cách ghi lập trường đồng ý hoặc phản đối và trích nguyên văn bất đồng ở gate theo `stage-protocol-collaborators.md` của AWS; tên Decision Brief theo decision brief của AWS |
| Execution | always ở M và L |
| Lead | product. Design PIC, Tech PIC, QA PIC viết file thiết kế và duyệt Decision Brief |
| Produces | `inception/decision-brief/decision-brief.md` · `design-alignment-questions.md` |
| Consumes | `prd.md` đã approve (bắt buộc) · `inception/ux-design/ux-design.md`, `inception/tech-design/tech-design.md`, `inception/test-design/test-design.md` do các team viết (bắt buộc) · `scope-document.md` cho mốc cứng, `impact-matrix.md`, `decisions.md` |
| Requires | prd-generation |
| Profiles | M, L |
| Reviewer | none, các PIC là người review |
| Summary confirmation | required |
| Template | `engine/templates/decision-brief.md` · `engine/templates/ux-design.md` · `engine/templates/tech-design.md` · `engine/templates/test-design.md` |
| Checklist | `engine/verification/design-alignment.md` |
| Knowledge | `engine/standards/handoff-rules.md` · `engine/standards/story-splitting.md` mục 4 khi Tech PIC báo story quá lớn, mục 8 khi Tech PIC đề xuất đổi Unit |

Chạy theo `engine/protocol/stage-protocol.md`.

## Mục đích
Các team cần PRD chi tiết để thiết kế. Stage này nhận ba bản thiết kế của Design, Tech, QA viết từ PRD đã duyệt, đối chiếu với PRD, và giải quyết mọi điểm còn vướng trong một buổi họp trên một tài liệu ngắn là Decision Brief. Story List chỉ sinh sau khi stage này được duyệt, lúc yêu cầu và thiết kế đã khớp nhau. Gate là Alignment gate, cần ba PIC duyệt.

## Giao cho các team, ngay sau khi PRD được duyệt
1. Ghi Design PIC, Tech PIC, QA PIC vào `intent.md` nếu còn trống.
2. Tạo ba file từ template, mỗi file trong thư mục của team: `inception/ux-design/ux-design.md`, `inception/tech-design/tech-design.md`, `inception/test-design/test-design.md`. Chỉ điền frontmatter: intent, mã tính năng, owner là tên PIC, `inputs: prd@<version đã duyệt>`. Không điền nội dung.
3. Đánh dấu stage `[-]`. Ghi vào `state.md` mục Current: "Chờ Design PIC, Tech PIC, QA PIC viết file thiết kế, hạn <ngày>".
4. Báo PO gửi ba PIC đường dẫn PRD đã duyệt, đường dẫn file của họ và quy ước dưới đây.

Quy ước cho PIC:
- Mỗi team chỉ sửa file của mình. Pull trước khi sửa, commit với message `design(<intent>): ux`, `tech` hoặc `test`. Sửa trên GitHub web hoặc bằng công cụ AI của team đều được.
- Mọi phần trỏ về mã trong PRD: `U<n>`, `US<n>`, `AC<n>.<m>`, `BR<n>.<m>`. Tech PIC ghi cỡ của từng Unit ở mục 7 của `tech-design.md`: phần việc Backend, Frontend, độ lớn, kết luận Unit có vừa một sprint, đề xuất tách, gộp hoặc chuyển US; mỗi Unit là một story trên Jira. Design PIC đặt mã màn `SCR<n>` ở bảng Danh sách màn, mỗi màn ghi US mà nó phục vụ; Story List lấy mã màn từ bảng này.
- Ý kiến về PRD ghi ở mục Ý kiến về PRD của file mình, mỗi dòng một lập trường: Đồng ý, Đề xuất sửa, Phản đối, kèm mã và lý do. Không sửa PRD.
- PIC không mở được repo: gửi nội dung cho PO; PO dán nguyên văn, mở đầu bằng "(ghi theo <tên>, <ngày>)".

Ngoài khung file và frontmatter tạo ở bước 2, AI của PO không viết và không sửa ba file thiết kế. Thiếu nội dung thì báo PO hỏi PIC.

## Load
Khi PO gọi `/po <intent>` và stage đang `[-]`: đọc PRD đã duyệt, ba file thiết kế, `scope-document.md` để lấy mốc cứng, Impact Matrix để lấy vùng hồi quy, `decisions.md`. File nào còn khung trống thì báo PO team nào chưa xong và dừng. Không viết Decision Brief khi chưa đủ ba file, trừ khi PO quyết đi tiếp; khi đó ghi DEC.

## Ask
Chỉ hỏi PO khi cần:
1. Ngày họp và người dự.
2. Điểm PO muốn đưa thêm vào buổi họp.
3. Với mỗi Đề xuất sửa PRD của các team: PO nhận, không nhận, hay đưa ra họp.

## Generate
1. Chạy `python3 engine/scripts/po-tools.py check intents/<intent> design-alignment` để lấy phần máy đối chiếu được: US có giao diện chưa có màn, AC chưa có trong kế hoạch test, US chưa có trong thiết kế kỹ thuật, màn của ux-design chưa có ở phần Frontend của tech-design, Unit chưa được Tech PIC xác nhận cỡ hoặc được ghi không vừa một sprint, file thiết kế dựng từ bản PRD cũ.
2. Đọc ba file và đối chiếu: mâu thuẫn giữa các thiết kế; hợp đồng API của tech-design đủ cho các màn của ux-design, mã lỗi khớp câu thông báo của PRD; phía Backend hoặc Frontend ghi Không đổi mà PRD có thay đổi chạm tới phía đó; thiết kế trái business rule hoặc tiêu chí chấp nhận; phụ thuộc giữa các team; độ lớn Tech PIC ước lượng so với mốc cứng; Đề xuất sửa và Phản đối của từng team.
3. Viết `decision-brief.md` theo template. Chỉ ghi điểm cần người quyết hoặc cần cả nhóm biết; mỗi điểm có lựa chọn, hệ quả và đề xuất. Ý kiến Phản đối chép nguyên văn kèm tên người nêu. Không chép lại nội dung thiết kế. Phần AI viết, mục 1 đến 9, không quá 1.500 từ, kiểm bằng đếm từ. Văn phong bàn giao: không thẻ nguồn, không từ quy trình, mã kèm nội dung.
4. Frontmatter `inputs:` ghi version của PRD và ba file thiết kế đã dùng. File thiết kế đổi sau đó thì `po-tools.py status` báo.
5. Bảng Duyệt điền tên ba PIC đúng như `intent.md`, cột Bản để trống, trạng thái "Chưa xem".
6. Trước khi gửi cho PIC: chạy `python3 engine/scripts/po-tools.py sign-start intents/<intent>`. Lệnh ghi dấu bản gửi duyệt. Decision Brief sửa sau đó thì tăng version và chạy lại, lượt duyệt cũ không còn tính.

## Verify
1. Checklist.
2. `po-tools.py check` của stage không còn cảnh báo, hoặc cảnh báo còn lại đã nằm trong Decision Brief để họp quyết.

## Họp và sau họp
- Họp trên Decision Brief. Mỗi quyết định ghi một DEC, người quyết là người quyết trong họp, nguyên văn nếu có.
- Quyết định làm đổi PRD: đi `/change-request`, mở lại 2.42, sửa và duyệt lại PRD; sau đó cập nhật `inputs:` và mục liên quan của Decision Brief. Quyết định tách, gộp Unit hoặc chuyển US giữa các Unit cũng đi đường này, sửa PRD mục 5, vì bảng Units ở PRD là bản chốt để sinh story trên Jira. Quyết định làm đổi thiết kế: team sửa file của mình.
- PIC ghi ở bảng Duyệt: tên như ở `intent.md`, cột Bản là version đã đọc, trạng thái Chưa xem, Có ý kiến, Đồng ý hoặc Yêu cầu sửa. Duyệt trên repo, hoặc PO ghi theo tin nhắn xác nhận và lưu nguyên văn vào `decisions.md`. `po-tools.py check` báo lượt duyệt sai người, sai bản, hoặc duyệt trên bản đã đổi.

## Gate, Alignment
Trình: điểm đã thống nhất kèm DEC, điểm còn mở, trạng thái duyệt của từng PIC, ý kiến Phản đối nguyên văn, thay đổi PRD đã làm qua change request. Approve khi ba PIC ghi Đồng ý hoặc Có ý kiến. Một PIC ghi Yêu cầu sửa thì gate là Request Changes. Tới hạn mà còn PIC chưa duyệt thì PO được chọn Accept as-is ngay, không cần chờ lần Request Changes thứ ba; lý do ghi một DEC, lệnh approve chạy với `--accept-warnings` vì script coi thiếu lượt duyệt là cảnh báo.
Trước khi trình gate: điền dòng 6 của `verification/phase-check-inception.md` và cập nhật Kết luận. Với profile M, L, đây là phase check Inception.
Sau Approve: decision-brief lên version 1.0 và được chụp archive. Sau đó chạy `/po-stories` để sinh Story List cho Jira. File thiết kế đổi sau khi duyệt thì team sửa file của mình; thay đổi chạm yêu cầu đi change request.

Phần PO của intent hoàn tất. `/generate-user-guide` sau khi Dev xong, và cập nhật ngược KB.
