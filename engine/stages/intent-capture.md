# 1.1 Intent Capture & Framing

| | |
|---|---|
| Stage | 1.1 Intent Capture & Framing |
| Slug | intent-capture |
| Thư mục | `ideation/intent-capture` |
| Phase | ideation |
| Plugin | (stage gốc AWS) |
| Lệch so với AWS | AWS sinh hai file intent-statement và stakeholder-map; ở đây stakeholder map là một mục của intent-statement. AWS chạy reviewer ở mọi scope; ở đây chỉ profile L |
| Execution | always ở M và L |
| Lead | product |
| Produces | `ideation/intent-capture/intent-statement.md` · `intent-capture-questions.md` |
| Consumes | `inputs/*` (bắt buộc) · `intent.md` · KB định hướng sản phẩm và nguyên tắc mô hình hoá theo `domain.md` mục 4 phần 1.1 |
| Requires | không |
| Profiles | M, L |
| Reviewer | ai-reviewer ở L. M: none |
| Summary confirmation | required |
| Template | `engine/templates/intent-statement.md` |
| Checklist | `engine/verification/intent-capture.md` |
| Knowledge | `domain/domain.md` mục 1 và mục 4 phần 1.1, cùng các file KB nó trỏ tới · product: `product-guide.md` §Persona Development, `requirements-elicitation.md` §Stakeholder Interviews |

Chạy theo `engine/protocol/stage-protocol.md`. Dưới đây chỉ là phần riêng của stage.

## Mục đích
Khung vấn đề trước khi bàn giải pháp: ai gặp vấn đề gì, vì sao bây giờ, đo thành công bằng gì, ai liên quan và ai quyết. AWS: stage 1.1 do Product Agent dẫn.

## Load
- Đọc nguyên văn `inputs/`. Tách giải pháp người yêu cầu đã nghĩ sẵn ra khỏi vấn đề. "Thêm nút export" là giải pháp; vấn đề có thể là "không lấy được dữ liệu ra để đối chiếu". Giải pháp đó là Recommendation, chưa phải yêu cầu.
- KB định hướng và nguyên tắc mô hình hoá theo `domain.md`: yêu cầu thuộc tầng nào của sản phẩm, phục vụ một tenant hay mọi tenant, có đụng nguyên tắc mô hình hoá nào.
- `intent.md` mục Related intents: trùng hay phụ thuộc intent khác không.

## Ask
Đây là gợi ý, không bắt hỏi đủ hay đúng thứ tự. Bỏ câu đã có đáp án trong inputs.
1. Vấn đề nghiệp vụ, theo góc nhìn người dùng: ai gặp, khi nào, hậu quả.
2. Người dùng đang xoay xở thế nào khi chưa có tính năng: làm gì, theo thứ tự nào, dựa vào tiêu chí gì, mất bao lâu, hay sai ở đâu.
3. Thành công trông như thế nào, đo bằng chỉ số nào, lấy số ở đâu.
4. Vì sao làm lúc này: áp lực, cơ hội, hay nợ cũ.
5. Stakeholder: ai quan tâm điều gì, ai quyết phạm vi và ưu tiên, ai chỉ cần được báo.
6. Bản đầu tiên không làm gì. Hỏi về sản phẩm, không hỏi lại profile.
7. Portal nào, theo danh sách portal trong `domain.md` mục 1. Hằng số nào phải cấu hình theo tenant.
Mỗi câu có lựa chọn "Chưa xác định" khi PO có thể chưa biết. Không tự thêm stakeholder.

## Generate
`intent-statement.md` theo template. Thẻ nguồn ở mọi khối: `[desc]`, `[Q3]`, `[KB-<file> §<mục>]`, `[assumption]`. Stakeholder map có cột Nguồn. Mục Assumptions & Open Questions bắt buộc.
Success metrics: mỗi objective theo SMART của BABOK 6.2, có chỉ số, giá trị hiện tại hoặc "chưa đo", giá trị mục tiêu, thời điểm đo; tự đề xuất ít nhất một cách đo, chỉ giữ cái đo được từ dữ liệu hệ thống sẽ có. Không có số thì mô tả cách làm hiện tại đủ rõ, không bỏ trống. Stakeholder map theo BABOK 3.2: mức ảnh hưởng, thái độ với thay đổi, và ai là người tài trợ, người quyết cuối việc làm hay dừng; người này ghi cả vào `intent.md`.

## Xác nhận giả định
Theo `stage-protocol.md` bước 4b: liệt kê giả định trong intent-statement, PO chọn chấp nhận hay chuyển thành câu hỏi, trước khi gọi reviewer.

## Verify
`po-tools.py check`, sau đó checklist của stage. Reviewer ai-reviewer ở L.

## Gate
- Profile L: gate riêng. Trình: vấn đề một đoạn, objective kèm cách đo, stakeholder, ràng buộc, assumption đáng chú ý, OQ còn chặn.
- Profile M: không mở gate tại stage này. Đánh dấu 1.1 `[?]`, chạy tiếp 1.4 trong cùng lượt, gate chung ở cuối 1.4 theo `gate-protocol.md`.

Stage kế: 1.2 nếu PO muốn so với sản phẩm khác, không thì 1.4.
