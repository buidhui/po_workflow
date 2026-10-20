# /generate-user-guide

Mắt xích cuối: yêu cầu, PRD, Dev làm xong, User Guide. Mô tả cái đang chạy, không mô tả cái sắp có; tính năng chưa dev xong thì dừng.

Xác định intent từ tham số lệnh; thiếu thì hỏi. Đọc theo thứ tự: `inception/prd/prd.md` bản approved; template `engine/templates/user-guide.md`; KB cho cách các module liên quan đang được mô tả; `domain.md` mục 4 phần User Guide cho nơi lưu tài liệu người dùng của sản phẩm và các đối tượng người dùng.

## Nơi User Guide sống
Bản chính thức nằm trong intent, ở `user-guide/`. Nơi lưu tài liệu người dùng của sản phẩm và các đối tượng người dùng ghi ở `domain.md` mục 4 phần User Guide; chép sang đó và đổi sang cú pháp của công cụ tài liệu là việc của repo sản phẩm. Tính năng chạm nhiều đối tượng thì mỗi đối tượng một bài riêng, hậu tố theo đối tượng; người dùng cuối và người vận hành cần thông tin khác nhau.

## Cấu trúc bài viết
Theo template `engine/templates/user-guide.md`, Markdown thuần, không gắn với công cụ tài liệu nào: 1. Thông tin chung gồm Dành cho, Đường dẫn, Module chính, Module liên quan, điều kiện trước khi bắt đầu · 2. Các bước thực hiện, một hành động mỗi bước · 3. Lưu ý và quy tắc nghiệp vụ · 4. Lỗi thường gặp và cách xử lý. Module liên quan bắt buộc: thiếu nó thì KB không dựng được quan hệ chéo và Impact Analysis bỏ sót đúng vùng dày quan hệ nhất. Mỗi bài trả lời một việc người dùng cần làm, theo cách viết hướng dẫn tác vụ của ISO/IEC/IEEE 26514.

## Chuyển PRD sang User Guide
| PRD | User Guide |
|---|---|
| Luồng chính, hoặc Scenario ở PRD theo template cũ | Mục 2, các bước thực hiện |
| Tiền điều kiện, hoặc Pre-Condition | Mục 1, điều kiện trước khi bắt đầu |
| Business rule | Mục 3, lưu ý và quy tắc nghiệp vụ |
| Bảng giao diện: validate, disable, tooltip, câu thông báo | Mục 4, lỗi thường gặp |
| Tiêu chí chấp nhận: phần Then | Mục 2, kết quả của từng thao tác |
| Ngoài phạm vi | Không đưa vào |
| Trường hợp ngoại lệ | Mục 4 nếu là tình huống người dùng gặp thật |
| Chuyển đổi và triển khai: hướng dẫn người dùng, mốc dữ liệu | Mục 3 nếu người dùng cần biết, ví dụ báo cáo chỉ có dữ liệu từ ngày bật |

Đổi giọng: PRD viết cho Dev và QA, User Guide viết cho người dùng cuối; ví dụ đổi giọng của domain ở `domain.md` mục 4 phần User Guide. Bỏ hết tên bảng, tên field kỹ thuật, endpoint, mã rule.

## Ảnh màn hình
Có Playwright MCP: chạy headless, viewport 1920×1080, đăng nhập bằng tài khoản test PO cung cấp, chụp theo từng bước của mục 2, lưu về `user-guide/screenshots/` trong intent với tên `NN-<role>-<mô-tả-ngắn>.png`, kiểm ảnh đạt khoảng 1920px và layout giống desktop thật. Ảnh trong thư mục tạm của Playwright không phải output. Không có Playwright hoặc PO gõ `skip-screenshot`: chèn `<!-- ẢNH: mô tả cảnh cần chụp -->` và liệt kê ảnh còn thiếu vào `user-guide/pending-screenshots.md`.

## Output
`user-guide/<slug>-<role>.md` trong intent. Tự kiểm theo `engine/verification/generate-user-guide.md`.

## Sau khi viết xong
1. Trình PO review. Duyệt xong hỏi có đưa vào repo tài liệu tương ứng không.
2. Cập nhật KB trong `domain/` theo `engine/standards/domain-kb.md` mục 5: phần tính năng ghi Planned từ lúc duyệt PRD đổi sang Active, đối chiếu lại business rule, field, quan hệ module với sản phẩm thật, ghi nguồn là PRD nào. Không làm thì KB đứng yên trong khi sản phẩm chạy tiếp.
3. Ghi dòng Log vào `state.md` của intent.
