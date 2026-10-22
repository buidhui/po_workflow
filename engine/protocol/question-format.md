# Question Format

Cách hỏi và ghi câu trả lời của PO. Bám theo AWS AI-DLC `stage-protocol.md` mục 3. File câu hỏi là nguồn sự thật: mọi câu trả lời, dù PO nói trong chat hay sửa file, cuối cùng đều nằm trong file.

## File
`<thư mục stage>/<slug>-questions.md`, tạo từ `engine/templates/questions.md`.

```markdown
# <Tên stage>, câu hỏi
Intent: <slug> · Cách trả lời: <Guide me | Edit file | Chat> · Đã trả lời: 2/6

## Q1. [PO] <Câu hỏi, một câu, tự giải thích>
Vì sao hỏi: <một dòng: điều gì phụ thuộc vào câu trả lời>
A. <lựa chọn>  [đề xuất, theo KB-<file> §<mục>]
B. <lựa chọn>
C. <lựa chọn>
X. Khác, xin nói rõ
Chặn: có | không
[Answer]:
```

## Quy tắc đặt câu hỏi
- Chỉ hỏi câu mà đáp án làm đổi phạm vi, business rule, dữ liệu, luồng, hoặc quyền. Không hỏi kỹ thuật cho Dev.
- Tra KB, API spec, schema và `decisions.md` trước. Đã có đáp án thì không hỏi. Còn mơ hồ thì hỏi hẹp, nêu đáp án cũ: "Trước đã quyết A ở DEC5, giờ có áp cho trường hợp B không?"
- Mỗi câu tự giải thích. Mã nào xuất hiện thì kèm nội dung: "yêu cầu xuất báo cáo theo nhóm (FR3)", không viết "FR3 còn đúng không?".
- Một dòng *Vì sao hỏi* khi lý do không hiển nhiên.
- Lựa chọn A đến D, tối đa bốn, để vừa hộp chọn; trong file luôn có thêm dòng X. Khi không chắc có lựa chọn nào hợp, dùng một trong bốn ô cho "Chưa xác định" để PO không bị ép chọn bừa. Câu thật sự cần năm lựa chọn thì không đưa vào hộp chọn: trình dạng chữ, PO gõ chữ cái.
- `[đề xuất]` là đáp án AI thấy hợp lý nhất, kèm nguồn. PO chỉ cần nói "đồng ý hết trừ Q3".
- *Chặn: có* khi thiếu đáp án thì không viết được artifact đúng. Câu chặn còn trống thì stage không đi tiếp.
- Hỏi theo lô tối đa bốn câu. Câu chặn hỏi trước. Câu là tiền đề của câu khác thì hỏi trước câu phụ thuộc vào nó.
- Mỗi câu gắn nhãn người trả lời ngay sau số câu: `[PO]`, `[Người yêu cầu]`, `[Design]`, `[Tech]`, `[QA]`, hoặc vai khác ghi trong `domain.md`. Câu cùng nhãn đứng cạnh nhau, để PO chuyển cả nhóm cho đúng người hoặc họp theo nhóm, sau đó điền theo cách Edit file. Câu kỹ thuật vẫn không hỏi; nhãn `[Tech]` chỉ dùng cho câu mà đáp án làm đổi phạm vi, như "có giữ được dữ liệu cũ không".
- Chọn nhiều được: ghi "chọn nhiều" trong câu hỏi, PO trả lời "A, C".

## Ba cách trả lời
| Cách | PO làm gì | AI làm gì |
|---|---|---|
| Guide me | Trả lời từng lô qua hộp chọn AskUserQuestion, mỗi câu có lối "Khác" để nói bằng lời | Ghi vào file ngay sau mỗi lô |
| Edit file | Mở file, điền `[Answer]:`, nói "xong" | Đọc file, liệt kê câu còn trống, hỏi tiếp |
| Chat | Nói tự nhiên, nhiều câu một lúc | Trích quyết định, ghi vào đúng câu, trình lại danh sách để PO xác nhận |

Hộp chọn của Claude Code nhận tối đa bốn câu mỗi lần và từ hai tới bốn lựa chọn mỗi câu, và tự có sẵn ô gõ chữ. Vì vậy dòng X không đưa vào hộp; nói với PO một lần trước lô đầu: "Muốn trả lời khác các lựa chọn thì gõ vào ô cuối." Công cụ khác không có hộp chọn thì trình câu hỏi dạng chữ.

Hỏi cách trả lời một lần cho cả intent, ghi vào `state.md`. Stage sau nói một dòng: "Đang hỏi theo cách anh/chị chọn: Guide me. Muốn đổi thì nói." PO đổi giữa chừng thì ghi lại.

## Ghi câu trả lời
- Nguyên văn lời PO sau `[Answer]:`, kể cả khi chọn bằng chữ cái: `A, "<lời PO nói thêm>"`; ví dụ ở `domain.md` mục 5.
- Diễn giải của AI, nếu cần, dòng dưới: `Hiểu là: ...`.
- PO uỷ quyền: `[Answer]: [uỷ quyền] "tuỳ anh", chọn A theo đề xuất`. Nói với PO một dòng: "Anh/chị để tôi chọn Q2, tôi chọn A. Muốn khác thì nói." Uỷ quyền chỉ áp cho câu của stage đang chạy, không áp cho xác nhận tóm tắt, xác nhận giả định hay gate.
- Cách Chat: trước khi kết thúc lượt, ghi mọi câu trả lời vừa nghe vào đúng câu trong file. Câu trả lời chỉ nằm trong hội thoại sẽ mất khi phiên bị nén.
- Không bao giờ tự điền `[Answer]:` khi PO chưa nói.

## Soát sau khi có câu trả lời
- Từ mơ hồ: "tuỳ", "chắc là", "có thể", "cả hai". Hỏi lại cho tới khi rõ.
- Mâu thuẫn giữa các câu, hoặc với `decisions.md`: trình hai câu cạnh nhau, giải thích vì sao vênh, hỏi một câu để PO quyết. Không tự chọn một bên.
- Thiếu dữ kiện để sinh artifact: hỏi tiếp, đánh số tiếp.
- Đáp án không khớp lựa chọn nào và không phải "Khác" có lời: hỏi PO muốn chọn gì.

## Xác nhận tóm tắt
Khi mọi câu đã trả lời và stage có summary confirmation:
- Thêm mục `## Consolidated Summary` vào cuối file: gạch đầu dòng, mỗi câu một dòng, nội dung đã thống nhất.
- Hỏi bằng hộp chọn: Looks correct, sinh artifact từ những điều này. Request changes, sửa một vài câu trước.
- Request changes: PO đã nói cần sửa gì thì sửa luôn; chưa nói thì hỏi "sửa gì". Sửa file, xoá tóm tắt cũ, hỏi lại.
- Chỉ sinh artifact sau Looks correct.

## Thẻ nguồn trong artifact nội bộ
| Thẻ | Nghĩa |
|---|---|
| `[desc]` | Lời yêu cầu gốc trong `inputs/` |
| `[Q3]` | Câu trả lời số 3 của stage này. Stage khác ghi `[2.3 Q3]` |
| `[KB-<file> §<mục>]` | Nguồn trong KB |
| `[DEC5]` | Quyết định đã ghi |
| `[assumption]` | Giả định, chưa xác nhận |
| `[suy ra]` | AI suy luận từ nguồn; nguồn không nói thẳng |

Mỗi khối khẳng định trong artifact nội bộ có ít nhất một thẻ. Nội dung không có nguồn thì bỏ, hoặc hỏi, hoặc đưa vào Assumptions & Open Questions với `[assumption]`. Không nâng assumption thành fact ở stage sau khi PO chưa xác nhận.
