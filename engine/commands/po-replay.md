# /po-replay

Tóm lược diễn biến của một intent cho người vắng mặt, ví dụ khi bàn giao intent cho PO khác hoặc khi PIC hỏi intent đang tới đâu. Chỉ đọc, không sửa file nào. Theo skill `aidlc-replay` của AWS: số liệu do script đếm, AI không tự đếm.

1. Xác định intent từ tham số lệnh; thiếu thì liệt kê intent và hỏi.
2. Chạy `python3 engine/scripts/po-tools.py replay intents/<slug>`. Script in: tiêu đề, profile, stage hiện tại, việc kế tiếp; dòng thời gian từ Log; bảng quyết định; change request; kết quả review; câu hỏi chặn còn mở; nơi đăng bản đọc nếu có.
3. Trình lại cho PO, thêm tối đa ba câu tóm tắt bằng lời: intent đang ở đâu, điều gì đang chặn, ai phải làm gì tiếp. Không thêm dữ kiện không có trong file.
4. Không chạy được python thì đọc `state.md`, `decisions.md`, `reviews/` và trình bày theo đúng thứ tự trên.
