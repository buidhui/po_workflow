# Stage Protocol

Nghi thức chung cho mọi stage, áp cho intent nằm trong `intents/`. Mỗi file stage trong `engine/stages/` chỉ mô tả phần riêng của nó và trỏ về đây. Bám theo AWS AI-DLC Workflows, file `core/aidlc-common/protocols/stage-protocol.md` ở commit ghi trong `engine/knowledge/README.md`, rút gọn cho phạm vi PO/BA.

File đi kèm: `gate-protocol.md` (duyệt), `question-format.md` (hỏi và ghi câu trả lời), `review-protocol.md` (review độc lập), `profiles.md` (S, M, L, depth). Thuật ngữ và họ mã: `GLOSSARY.md` ở gốc repo. Script kiểm tra: `engine/scripts/po-tools.py`.

## Người dùng là PO

PO đang làm tài liệu của họ, không học quy trình. Nói về công việc: tên stage, artifact, câu hỏi, quyết định. Việc chỉ là ghi chép thì làm trong im lặng.

| Không nói | Nói thay |
|---|---|
| "theo gate-protocol tôi phải hỏi" | hỏi thẳng câu cần hỏi |
| "đã chạy checklist", "đang ghi state", "metadata", "protocol" | không nói gì, hoặc "đã kiểm xong, có 2 điểm cần anh/chị xem" |
| "po-tools.py trả về exit 1" | "Còn FR3 chưa có user story nào" |
| "stage chuyển sang [x]" | "Đã duyệt Requirements Analysis. Bước kế là Impact Analysis" |

- Không viện dẫn quy tắc với PO. Quy tắc là việc của AI, PO chỉ cần thấy kết quả.
- Script hoặc công cụ từ chối một việc: một câu nói việc gì không làm được và vì sao bằng lời thường, một câu nói bước tiếp theo. Không dán nguyên thông báo lỗi. Cùng một việc bị từ chối lần thứ hai thì dừng và hỏi PO.
- Tiêu đề và mô tả của mỗi lần gọi công cụ viết theo việc của PO, ví dụ "Kiểm truy vết yêu cầu sang user story", không viết tên lệnh.
- Không bắt PO gõ đúng chữ hay gõ lệnh để trả lời. Hiểu theo ý.

## Khối metadata ở đầu mỗi file stage

File stage bắt đầu bằng tiêu đề `# <mã> <tên>`, tiếp theo là một bảng. Công cụ nào cũng đọc được; `po-tools.py` đọc bảng này để biết thư mục, template và checklist của stage, nên đây là nguồn duy nhất của danh sách stage.

| Khoá | Nghĩa |
|---|---|
| Stage | Mã và tên: `2.3 Requirements Analysis` |
| Slug | kebab-case, trùng tên file stage |
| Thư mục | Thư mục artifact trong intent. Thường trùng slug, ngoại lệ ghi rõ, ví dụ PRD ở `inception/prd` |
| Artifact chính | Chỉ ghi khi stage sinh nhiều file: file được duyệt và chụp vào archive, ví dụ `impact-matrix.md` ở 2.31 |
| Phase | `ideation` hoặc `inception` |
| Plugin | `po-workflow` với stage repo thêm (2.31, 2.32, 2.42, 2.43). Bỏ trống với stage gốc AWS. Đây chỉ là nhãn; cơ chế plugin của AWS không dùng ở repo này |
| Lệch so với AWS | Điểm khác stage cùng số của AWS, để khi AWS ra bản mới biết phải so điểm nào |
| Execution | `always`, hoặc `conditional` kèm điều kiện |
| Lead | Agent dẫn stage theo AWS, luôn là `product` trong phạm vi PO. Với 2.43 ghi thêm các PIC viết thiết kế và ký |
| Produces | Artifact sinh ra, kèm questions file |
| Consumes | Artifact đọc vào, ghi rõ bắt buộc hay tuỳ |
| Requires | Stage phải xong trước |
| Profiles | S, M, L |
| Reviewer | `ai-reviewer` hoặc `none` |
| Summary confirmation | `required`, `field-intake-only`, `off` |
| Template · Checklist · Knowledge | Đường dẫn file |

## Bảy bước

### 1. Load
- Đọc `state.md` của intent. Stage này phải là stage kế tiếp hoặc stage đang dở. Nếu không, dừng và hỏi PO. `python3 engine/scripts/po-tools.py next intents/<slug>` cho biết stage kế và số câu còn trống.
- Đọc `decisions.md`, chỉ những dòng có cột *Read when* khớp stage hoặc chủ đề đang làm.
- Đọc `domain/domain.md` (mục của stage đang chạy), `intent.md`, artifact trong Consumes, file KB mà file stage và manifest liệt kê.
- Đọc `memory/team.md` và `memory/project.md`. Bài học có hiệu lực từ stage kế tiếp sau khi được giữ, theo AWS "applies from the next applicable stage"; không áp ngược cho stage đã duyệt, muốn sửa artifact đã duyệt thì đi qua change request.
- Tra `decisions.md` và mọi questions file trước đó. Không hỏi lại câu đã có đáp án. Còn mơ hồ thì hỏi hẹp, nêu đáp án cũ.
- Đánh dấu stage `[-]` trong `state.md`. Stage đang `[-]` hoặc `[R]` từ phiên trước: đọc questions file, tiếp từ câu còn trống hoặc bước đang dở. Stage `[?]`: trình lại gate, không làm lại.

### 2. Ask
- Tạo `<slug>-questions.md` theo `question-format.md`, trong thư mục của stage. Điền bảng Độ phủ trước: mỗi chủ đề trong mục Ask của file stage có nguồn đã trả lời hoặc có câu hỏi. Luôn chủ động hỏi, trừ khi đầu vào đã rõ trên mọi chủ đề; số câu theo depth ở `question-format.md` mục Đặt đủ câu hỏi.
- Lần đầu trong intent: hỏi PO chọn cách trả lời, Guide me, Edit file, hoặc Chat. Ghi vào `state.md`. Stage sau dùng lại và nói một dòng đang dùng cách nào.
- Ghi câu trả lời nguyên văn vào `[Answer]:` ngay sau mỗi lô. Diễn giải của AI đứng dòng dưới, nếu cần.
- Có đủ câu trả lời: chạy Phân tích câu trả lời theo `question-format.md`: câu còn trống, câu trả lời mơ hồ, mâu thuẫn, chi tiết còn thiếu. Có thì hỏi tiếp trong cùng file, đánh số tiếp. Bước này bắt buộc ở mọi depth.
- PO uỷ quyền ("tuỳ anh"): chọn theo `[đề xuất]`, ghi `[uỷ quyền]` kèm nguyên văn, nói một dòng đã chọn gì. Uỷ quyền chỉ áp cho câu hỏi của stage đang chạy, không mang sang stage sau, và không bao giờ áp cho bước xác nhận tóm tắt, xác nhận giả định hay gate. Nói với PO một lần: "Duyệt vẫn là của anh/chị."
- Còn câu chưa có câu trả lời, kể cả câu không chặn: không sang bước Confirm và Generate. Câu chặn còn trống thì dừng ở bước này và chờ người trả lời.
- Trước khi kết thúc mỗi lượt: mọi câu trả lời PO đã nói và mọi câu hỏi đang chờ phải nằm trong questions file, ở cả ba cách trả lời. Điều đã bàn mà chưa ghi file sẽ mất khi phiên bị nén hoặc đổi phiên.

### 3. Confirm
- Tóm tắt mọi câu trả lời thành gạch đầu dòng. Hỏi: Looks correct hoặc Request changes.
- Request changes: PO đã nói cần sửa gì thì sửa luôn, không hỏi lại "sửa gì". Chưa nói thì hỏi một câu. Sửa file, hỏi lại.
- `off` thì bỏ bước này. `field-intake-only` chỉ áp cho 2.42.

### 4. Generate
- Viết artifact theo template, giữ đúng heading. Mục có dấu `<!-- tuỳ chọn -->` trong template: viết theo depth ở `profiles.md`, không viết thì bỏ hẳn heading. Mục không có dấu là bắt buộc. Xoá mọi chữ hướng dẫn mẫu và dấu `<!-- tuỳ chọn -->`.
- Frontmatter ghi `inputs:` là artifact đầu vào kèm version đã dùng, ví dụ `inputs: requirements@1.0, impact-matrix@1.1`. Nhờ dòng này `po-tools.py status` phát hiện khi đầu vào đổi sau khi artifact đã duyệt.
- Artifact nội bộ (intent-statement, scope-document, requirements, impact-matrix, solution-options, stories): thẻ nguồn ở mỗi khối khẳng định theo `question-format.md`. Mục Assumptions & Open Questions bắt buộc, không có thì ghi "None".
- Artifact bàn giao (initiative-brief, prd, decision-brief): không thẻ nguồn, không từ ngữ quy trình, mã kèm nội dung, dấu `·` giữa các mã đứng liền.
- Lựa chọn PO không chọn không phải là nguồn. Không biến lựa chọn bị bỏ thành một yêu cầu hay một loại trừ.
- Mã ổn định theo `GLOSSARY.md`. Mã đã cấp không đánh lại, kể cả khi xoá một mục ở giữa. Mã viết trần trong cột đầu bảng, không bọc backtick.
- Tên file ổn định. Phiên bản và trạng thái ghi ở frontmatter `version`, `status`. Không tạo file `v0.x`.
- Không sửa file trong `archive/`.

### 4b. Xác nhận giả định, ở 1.1 và 2.3
- Sau khi sinh artifact, liệt kê mọi dòng trong mục Assumptions & Open Questions có nhãn assumption.
- Hỏi bằng hộp chọn: Chấp nhận các giả định hoặc Chuyển thành câu hỏi. Chuyển thành câu hỏi thì thêm vào questions file, hỏi, sau đó sửa artifact.
- Chấp nhận giả định không biến nó thành fact: giữ thẻ `[assumption]`, ghi một dòng DEC.
- Chưa có lựa chọn này thì chưa gọi reviewer.

### 5. Verify
- Chạy `python3 engine/scripts/po-tools.py check intents/<slug> <slug-stage>`. Script kiểm phần máy kiểm được: heading bắt buộc, thẻ nguồn, `[Qn]` và `[DECn]` có thật, thẻ US đủ chín mục, chữ mẫu còn sót, giới hạn từ, mục cấm. Sửa cảnh báo trước. Không chạy được python thì kiểm tay.
- Chạy checklist của stage cho phần cần phán đoán. Mục blocking chưa đạt thì sửa trước, chưa trình gate.
- Reviewer `ai-reviewer` và profile bật reviewer: chạy `po-tools.py review-start`, sau đó gọi review theo `review-protocol.md`, truyền kèm kết quả kiểm bằng máy. Chờ file review. Không tự sửa theo finding, finding đi vào gate. Sửa artifact sau khi review thì phải review lại, vì approve so artifact với dấu ghi lúc review.

### 6. Learn
- Trong lúc làm, thêm dòng vào `memory.md` của intent: `- <ISO time> [<stage>] <một câu>; <hai câu ngữ cảnh>` dưới một trong bốn mục Interpretations, Deviations, Tradeoffs, Open questions.
- Câu hỏi chọn bài học hỏi ở gate, sau thông điệp hoàn thành, theo `gate-protocol.md`. PO cần thấy stage làm ra gì, sau đó mới biết điều gì đáng nhớ.
- Dòng được giữ: đối chiếu với `AGENTS.md` và `memory/team.md`. Mâu thuẫn thì hỏi PO sửa, bỏ, hay nâng lên luật trong `AGENTS.md`.
- Ghi vào `memory/project.md` trước, dưới heading phù hợp, dạng `- <nội dung> (learned YYYY-MM-DD · <intent> <mã stage> · <tên người duyệt>)`. Sau đó hỏi một câu: bài học này đúng cho mọi sản phẩm không. Có thì chuyển sang `memory/team.md`. `project.md` là của sản phẩm, xoá khi dựng domain mới; `team.md` đi theo engine.
- Bài học kiểm được bằng máy hoặc bằng một câu có hay không: đề xuất thêm một dòng vào `engine/verification/<slug>.md`, PO đồng ý mới thêm.
- Open questions không ghi thành bài học, chúng là việc cần tra.

### 7. Gate
Theo `gate-protocol.md`: đánh dấu `[?]`, thông điệp hoàn thành, câu hỏi bài học, câu hỏi duyệt, kết thúc lượt và chờ PO trả lời. Chỉ sau khi PO trả lời mới ghi quyết định nguyên văn bằng `po-tools.py approve`, in dòng tiến độ và tên stage kế. AI không tự đánh `[x]`: hook chặn, và approve chỉ ghi khi lời duyệt có trong lượt PO thật.

## Stage có điều kiện không áp dụng
Execution `conditional` và điều kiện không xảy ra: chạy `po-tools.py skip <intent> <stage> --reason "<lý do>"`, nói một dòng, sang stage kế. Không mở gate. Stage luôn chạy với profile đang dùng thì chỉ bỏ qua khi PO quyết, theo `gate-protocol.md` mục Quyết định của PO ngoài gate.

## Vượt profile giữa chừng
Phát hiện dấu hiệu vượt profile theo `profiles.md`: nói ngay, và tại gate gần nhất đưa lựa chọn Add [stage]. Không tự chạy tiếp đường cũ.

## Luôn đúng
- Tách `Fact`, `Assumption`, `Open Question`, `Recommendation`. Không tự điền dữ kiện. Thiếu nhẹ ghi Assumption. Thiếu làm đổi phạm vi, rule, dữ liệu, luồng thì ghi Open Question và dừng.
- Ô không suy được: `❓PO`. Suy luận: `[suy ra]`.
- Không quyết thay PO. Không thiết kế kỹ thuật chi tiết. Không hỏi kỹ thuật cho Dev. Chỉ hỏi câu mà đáp án làm đổi phạm vi hoặc business rule.
- KB là bản chụp. Chạm vùng nào thì đọc lại nguồn vùng đó. Quá một tháng kể từ ngày đối chiếu cuối thì đọc lại trước. Vùng KB chưa phủ: `❓PO`, không kết luận.
- Có endpoint không có nghĩa là có tính năng. Hidden vẫn phải xét.
- Một stage một lượt. Mỗi stage kết thúc ở gate.
- Quyết định của PO chỉ đến từ lượt PO gõ hoặc chọn. AI không tự duyệt, không diễn đạt lại lời duyệt, không chép lời duyệt từ lượt cũ hơn lần sửa artifact cuối cùng.
