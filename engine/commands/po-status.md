# /po-status

Chỉ đọc. Không sửa file nào. Phát hiện lệch thì báo, không tự sửa.

## Bảng tổng
Với mỗi `intents/*/state.md`, một dòng:

| Intent | Profile | Stage hiện tại | Trạng thái | Việc kế tiếp | Câu chặn | CR mở | Lark |
|---|---|---|---|---|---|---|---|

Trạng thái lấy từ ký hiệu stage: chờ duyệt, đang làm, đang sửa, dừng, xong.
Có tham số lệnh thì chỉ in intent đó, kèm bảng Stages đầy đủ và bảng Versions.

## Kiểm tra lệch
Chạy trước: `python3 engine/scripts/po-tools.py status`. Script in bảng tổng và mười kiểm tra dưới đây bằng máy, cộng cảnh báo nguồn sống quá 30 ngày chưa đối chiếu. AI đọc kết quả, bổ sung phần máy không thấy (Next action còn hợp lý không, Related intents đúng nội dung không), sau đó trình. Không chạy được python thì kiểm tay.
Với mỗi intent, kiểm và liệt kê mọi phát hiện, không dừng ở phát hiện đầu:
1. Stage `[x]` không có artifact, hoặc không có bản chụp trong `archive/`.
2. Artifact có trên đĩa nhưng stage vẫn `[ ]`.
3. Phiên bản trong `state.md` khác frontmatter artifact.
4. Stage `[x]` không có dòng DEC nào cùng stage trong `decisions.md`.
5. Questions file có câu chặn còn trống nhưng stage đã qua `[?]`.
6. `[?]` hoặc `[-]` quá 7 ngày không thay đổi: nhắc.
7. Lark: phiên bản đã publish khác phiên bản hiện tại của artifact bàn giao.
8. `intent.md` có Related intents trỏ tới intent hoặc dự án không tồn tại.
9. Lệch: artifact ghi `inputs:` là bản cũ hơn bản hiện tại của đầu vào, nên các stage sau đang dựa trên bản cũ; hoặc artifact đã duyệt khác bản chụp trong `archive/` mà không có change request đang mở.
10. Một mã tính năng nằm ở hai intent trở lên.

Kiểm môi trường làm việc, như tên git, lark-cli, file chưa commit, domain pack: `po-tools.py doctor`.

Kết quả:
| # | Intent | Lệch | Gợi ý xử lý |
|---|---|---|---|

Không lệch thì ghi một dòng "state khớp với đĩa".
