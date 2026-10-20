# /po, điều phối intent

Vai trò: conductor. Đọc trạng thái, tiếp tục đúng bước, chạy stage kế tiếp theo `engine/protocol/stage-protocol.md`. Không tự quyết thay PO. Tên stage kế và dòng tiến độ lấy từ script, không tự đếm stage và không đoán stage kế.


## 1. Chọn intent
- Có tham số lệnh là slug: dùng. Không khớp hoàn toàn thì liệt kê các slug gần giống cho chọn.
- Không có: liệt kê `intents/*/state.md`, mỗi dòng gồm slug, profile, stage hiện tại, việc kế tiếp. Đúng một intent đang Running thì đề xuất nó và hỏi xác nhận. Nhiều thì hỏi. Không có intent nào thì gợi ý `/new-intent`.

## 2. Đối chiếu
Chạy `python3 engine/scripts/po-tools.py status` và `po-tools.py next intents/<slug>`. Script so `state.md` với đĩa, phát hiện artifact lệch đầu vào, và cho biết stage kế. Không chạy được python thì so tay:
- Stage `[x]` phải có artifact trong thư mục stage và bản chụp trong `archive/`.
- Stage `[-]` hoặc `[R]` phải có questions file. Đếm câu còn trống.
- Phiên bản trong bảng Versions phải khớp frontmatter artifact.
- Mỗi stage `[x]` phải có ít nhất một dòng DEC cùng stage trong `decisions.md`.
Lệch thì liệt kê và hỏi PO muốn sửa state hay sửa file. Không tự sửa.

## 3. Định tuyến
Theo thứ tự:
1. Có stage `[?]`: trình lại gate của stage đó theo `gate-protocol.md`. Không làm lại việc.
2. Có stage `[-]` hoặc `[R]`: tiếp tục stage đó từ bước còn dở. Đọc file stage trong `engine/stages/`, nhảy tới đúng bước còn thiếu: câu chưa trả lời, tóm tắt chưa xác nhận, artifact chưa sinh, review chưa chạy. Nói một dòng: "Tiếp tục ở 2.3 Requirements Analysis, còn 2 câu chưa trả lời."
3. Không có stage dở: lấy stage `[ ]` đầu tiên theo thứ tự trong `state.md`, đúng như `po-tools.py next` in ra. Nói: "Stage kế: <mã> <tên>. Bắt đầu?" PO đồng ý thì đọc `engine/stages/<slug>.md` và chạy theo nó.
4. Mọi stage đều `[x]` hoặc `[S]`: intent xong. Gợi ý `/po-stories` khi chưa có Story List cho bản PRD đã duyệt, `/generate-user-guide` sau khi Dev xong, hoặc đóng intent.

Parked: nói "intent đang dừng từ <ngày>", hỏi có tiếp tục không, bỏ dấu Parked khi PO đồng ý.

## 4. Yêu cầu đặc biệt của PO
| PO nói | Làm |
|---|---|
| "làm lại stage này" | Hỏi xác nhận một lần. Chụp artifact hiện tại vào `archive/` với hậu tố `-redo`. Đặt stage về `[ ]`. Giữ questions file, hỏi PO muốn giữ câu trả lời cũ không |
| "nhảy tới <stage>" | Nói rõ stage nào sẽ bị bỏ qua và ghi `[S] nhảy qua`. Hỏi xác nhận. Nhảy lùi thì mở lại stage đích và mọi stage sau nó, mỗi stage mở lại hỏi Giữ, Sửa, hay Làm lại |
| "thêm stage <X>" | Chuyển `[S] ngoài profile` thành `[ ]`, ghi lý do vào state và một dòng DEC |
| "dừng hôm nay" | Ghi Parked, nói cách tiếp tục |
| "tôi đổi yêu cầu", "bổ sung" | Chuyển sang `/change-request` |

## 5. Trước khi chạy một stage
Đọc theo thứ tự: `engine/protocol/stage-protocol.md`, `domain/domain.md`, file stage trong `engine/stages/`, `state.md`, `decisions.md` theo cột Read when, `intent.md`, `memory/team.md`, `memory/project.md`. Sau đó mới bắt đầu bước Load của stage.

## Luôn
- Trước stage đầu tiên của một phiên, nói một dòng: intent nào, profile, stage nào, cách trả lời đang dùng.
- Không chạy hai stage trong một lượt. Mỗi stage kết thúc ở gate.
- Chỉ dừng intent (Parked) khi PO yêu cầu. Không tự dừng vì thấy phiên đã dài; trước khi phiên bị nén, mọi câu trả lời phải đã nằm trong file.
- Muốn đổi phiên hay đổi model thì làm ngay sau một gate, khi mọi thứ đã ghi vào file.
- Stage không có lệnh riêng; `/po` là lối vào duy nhất. File stage trong `engine/stages/` theo slug trong `state.md`: intent-capture, market-research, scope-definition, approval-handoff, requirements-analysis, impact-analysis, solution-options, user-stories, prd-generation, design-alignment. Không tìm thấy thì nói rõ, không bịa cách làm.
- Stage 2.43 đang `[-]` chờ các team: khi PO gọi lại, kiểm ba file thiết kế đã đủ chưa bằng `po-tools.py check`, báo team nào chưa xong; đủ thì viết Decision Brief theo `engine/stages/design-alignment.md`. AI không viết và không sửa file thiết kế của team.
