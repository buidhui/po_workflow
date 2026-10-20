# /generate-user-guide

Mắt xích cuối: yêu cầu, PRD, Dev làm xong, User Guide. Mô tả cái đang chạy, không mô tả cái sắp có; tính năng chưa dev xong thì dừng.

Xác định intent từ tham số lệnh; thiếu thì hỏi. Đọc theo thứ tự: `inception/prd/prd.md` bản approved; `domain.md` mục 4 phần User Guide cho đích và template; KB cho cách các module liên quan đang được mô tả; `domain/templates/user-guide.md`.

## Nơi User Guide sống
Đích, repo và đối tượng ghi ở `domain.md` mục 4 phần User Guide. Tính năng chạm nhiều đối tượng thì mỗi đối tượng một bài riêng, hậu tố theo đối tượng; người dùng cuối và vận hành cần thông tin khác nhau.

## Cấu trúc bài viết
Theo template của domain, đúng chuẩn tài liệu công ty đang dùng: I. Thông tin chung với khối `Dành cho`, `Đường dẫn`, `Phạm vi & Module liên quan`, `Điều kiện tiên quyết` · II. Hướng dẫn chi tiết theo `{% stepper %}` · III. Lưu ý và quy tắc nghiệp vụ · IV. Lỗi thường gặp và cách xử lý. Mục `Phạm vi & Module liên quan` bắt buộc: thiếu nó thì KB không dựng được quan hệ chéo và Impact Analysis bỏ sót đúng vùng dày quan hệ nhất.

## Chuyển PRD sang User Guide
| PRD | User Guide |
|---|---|
| Luồng chính, hoặc Scenario ở PRD theo template cũ | §II các bước thao tác |
| Tiền điều kiện, hoặc Pre-Condition | §I Điều kiện tiên quyết |
| Business rule | §III Lưu ý và quy tắc nghiệp vụ |
| Bảng giao diện: validate, disable, tooltip, câu thông báo | §IV Lỗi thường gặp |
| Ngoài phạm vi | Không đưa vào |
| Trường hợp ngoại lệ | §IV nếu là tình huống người dùng gặp thật |
| Chuyển đổi và triển khai: hướng dẫn người dùng, mốc dữ liệu | §III nếu người dùng cần biết, ví dụ báo cáo chỉ có dữ liệu từ ngày bật |

Đổi giọng: PRD viết cho Dev và QA, User Guide viết cho người dùng cuối; ví dụ đổi giọng của domain ở `domain.md` mục 4 phần User Guide. Bỏ hết tên bảng, tên field kỹ thuật, endpoint, mã rule.

## Ảnh màn hình
Có Playwright MCP: chạy headless, viewport 1920×1080, đăng nhập bằng tài khoản test PO cung cấp, chụp theo từng bước của §II, lưu về `user-guide/screenshots/` trong intent với tên `NN-<role>-<mô-tả-ngắn>.png`, kiểm ảnh đạt khoảng 1920px và layout giống desktop thật. Ảnh trong thư mục tạm của Playwright không phải output. Không có Playwright hoặc PO gõ `skip-screenshot`: chèn `<!-- ẢNH: mô tả cảnh cần chụp -->` và liệt kê ảnh còn thiếu vào `user-guide/pending-screenshots.md`.

## Output
`user-guide/<slug>-<role>.md` trong intent. Tự kiểm theo `engine/verification/generate-user-guide.md`.

## Sau khi viết xong
1. Trình PO review. Duyệt xong hỏi có đưa vào repo tài liệu tương ứng không.
2. Cập nhật ngược KB trong `domain/`: business rule mới, field đổi, quan hệ module mới, mã `KB-*` và ghi nguồn là PRD nào. Không làm thì KB đứng yên trong khi sản phẩm chạy tiếp.
3. Ghi dòng Log vào `state.md` của intent.
