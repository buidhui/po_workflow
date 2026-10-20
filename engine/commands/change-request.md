# /change-request

Dùng khi yêu cầu thay đổi hoặc bổ sung sau khi artifact đã qua gate. Tự kích hoạt khi PO nói *"tôi có thay đổi yêu cầu"*, *"bổ sung"*, *"đổi scope"*, *"thêm một rule"*, *"khách yêu cầu thêm"*.

Xác định intent: ưu tiên tham số lệnh; không có thì suy từ file đang mở; hơn một khả năng thì liệt kê cho chọn, không đoán. Echo và confirm trước khi chạy.

## 1. Phân loại
Thay đổi nhỏ trong stage đang mở (`[-]`, `[?]`, `[R]`): sửa và trình lại gate, không cần CR. Thay đổi chạm stage đã `[x]` mới đi đường CR.

## 2. Điểm re-entry
Hỏi: *thay đổi này làm sai lệch kết luận của stage nào?* Lấy stage thấp nhất bị sai, không lấy stage dễ sửa nhất.

| Loại thay đổi | Re-entry từ stage | Cascade |
|---|---|---|
| Vấn đề, mục tiêu, stakeholder | 1.1 | mọi stage sau |
| Phạm vi, Unit | 1.4 | 2.3 trở đi |
| FR, NFR, rule nghiệp vụ mới | 2.3 | 2.31 trở đi |
| Phát hiện ảnh hưởng mới | 2.31 | 2.32 trở đi |
| Đổi hướng giải | 2.32 | 2.4 trở đi |
| Danh sách US, Unit | 2.4 | 2.42, 2.43 |
| Chi tiết US, field, rule, màn | 2.42 | chỉ US bị chạm; profile M, L sang 2.43: team xem lại phần bị chạm, ký lại |
| Thiết kế của các team, quyết định ở buổi họp trên Decision Brief | 2.43 | Team sửa file của mình. Phải lấy lại chữ ký |
| Chỉ đổi User Guide | user-guide | — |

Ví dụ: một rule mới như "người dùng bị khoá thì không gửi được" là business rule, nhưng nó thêm một nhánh mà Impact Matrix chưa quét, nên re-entry từ 2.3 và chảy qua 2.31; sửa riêng PRD là chưa đủ. Ví dụ của domain ở `domain.md` mục 5.

## 3. Ghi CR và chụp archive
- Thêm `CR<n>` vào bảng Change requests của `decisions.md` kèm một DEC ghi nguyên văn PO. Không có file change-requests riêng; phân tích dài thì viết vào `inputs/change-requests.md` và trỏ từ bảng.
- Trước khi sửa bất kỳ artifact nào: `python3 engine/scripts/po-tools.py archive intents/<intent> <stage-slug> <artifact> --label pre-CR<n>`.

## 4. Impact preview, PO xác nhận
Trình bằng hộp chọn: stage re-entry kèm lý do, artifact sẽ đổi, gate phải duyệt lại. PO xác nhận trước khi chạy. Nếu bảng này đã nằm trong thông điệp gate ngay trước và PO đã trả lời "theo đề xuất", không hỏi lại.

## 5. Chạy lại xuôi, chế độ sửa
- Mỗi stage mở lại: hỏi Giữ, Sửa, hay Làm lại từ đầu. `state.md` đặt stage đó `[R]`, stage sau bị chạm về `[ ]`.
- Chỉ sửa phần bị chạm, không viết lại cả artifact. Thêm dòng ở bảng Lịch sử phiên bản ghi `CR<n>`, PRD theo template cũ dùng bảng Document version; version chính thức tăng khi duyệt lại, theo quy tắc phiên bản ở `gate-protocol.md`: đã duyệt 1.0 thì bản duyệt sau CR là 1.1. Cập nhật `inputs:` ở frontmatter theo bản đầu vào mới. PRD chỉ chạm US bị ảnh hưởng, frontmatter `status` về `draft` cho tới khi duyệt lại.
- Reviewer theo profile ở stage bị chạm; finding đi vào gate, không tự sửa theo finding.
- Trình lại gate theo `gate-protocol.md`. Nhiều stage nhỏ có thể gộp trong một thông điệp nhưng ghi rõ duyệt từng artifact.
- 2.43 bị chạm thì ba PIC ký lại Decision Brief; 2.42 bị chạm thì publish lại PRD sau Approve và báo các team xem lại file thiết kế theo bản PRD mới.

## 6. Tác động ngược
Trước gate 2.42: chạy `po-tools.py trace`; kiểm business rule mồ côi (rule cũ còn US nào dùng không), mã tham chiếu gãy (`BR-2.3` bị xoá mà nơi khác còn trỏ), Out of scope lỗi thời (thứ từng ghi "không làm" nay đã làm, hoặc ngược lại).

## 7. Sau khi duyệt
Duyệt từng artifact bằng `po-tools.py approve`: script chụp archive bản mới, cập nhật Versions và Log trong `state.md`. Đóng CR trong bảng. PRD hoặc Decision Brief duyệt lại thì gắn tag mới sau khi commit. PRD duyệt lại: profile M, L cập nhật Decision Brief nếu thay đổi chạm điểm đã chốt và lấy lại chữ ký; sau đó chạy `/po-stories`, script sinh CSV mới và in story nào đổi, story nào mới để sửa trên Jira; báo các PIC xem lại. Sau đó chạy `po-tools.py index --write`, để agent của Dev lấy đúng bản. Publish lại artifact bàn giao đã lên Lark. Chạy `po-tools.py status` để chắc không còn stage nào dựa trên bản cũ.

## Output
CR đã ghi; stage mở lại; artifact đã sửa và version; gate chờ duyệt lại; tác động ngược phát hiện được. Tự kiểm theo `engine/verification/change-request.md`.
