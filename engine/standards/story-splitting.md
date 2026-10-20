# Nguyên tắc chia story

Áp cho stage 2.4, khi PO chia yêu cầu thành user story. Cỡ story được Tech PIC xác nhận ở 2.43, trong `tech-design.md` mục Unit of work, thứ tự và độ lớn. Sau khi 2.43 được duyệt, Story List giữ nguyên cách chia này: mỗi US một story trên Jira. Phần so sánh với AWS AI-DLC ở mục 10.

## 1. Story là gì

Story là đơn vị nghiệm thu.

- Mỗi story là một mục tiêu hoàn chỉnh của một vai: người dùng làm trọn được và thấy kết quả.
- Story đi trọn từ giao diện tới rule và dữ liệu. Kiểu chia này gọi là lát dọc.
- Story kiểm được bằng tiêu chí chấp nhận: có đạt hoặc không đạt.
- Mỗi story thuộc đúng một Unit. Unit là nhóm story theo giá trị và ưu tiên, dùng để chốt phạm vi và thứ tự.

Mỗi team tự chia việc của mình từ story:

| Team | Chia việc theo | Quan hệ với story |
|---|---|---|
| Design | Màn hình, mã `SCR` | Một màn có thể phục vụ nhiều story |
| Dev | Unit of work, sau đó là sub-task trên Jira | Một Unit of work gồm một hoặc nhiều story; thiết kế kỹ thuật làm theo Unit |
| QA | Tiêu chí chấp nhận | Mỗi tiêu chí chấp nhận có ít nhất một test case |

## 2. Tiêu chí một story đạt

Dùng bộ tiêu chí INVEST. Bảng dưới ghi nơi kiểm từng tiêu chí trong PO-Workflow.

| Tiêu chí | Nghĩa | Kiểm ở đâu |
|---|---|---|
| Độc lập | Làm và giao được mà không chờ story khác, hoặc chỉ phụ thuộc một chiều | Mục Phụ thuộc của thẻ US; bảng Unit trong `stories.md` |
| Còn thương lượng được | Chi tiết còn mở tới khi PO viết PRD và các team chốt ở 2.43 | Thẻ US chưa có tiêu chí chấp nhận; chi tiết viết ở 2.42 |
| Có giá trị | Vai thấy được lợi ích của mình | Mục Vai và mục tiêu của thẻ US có vế "để ..." |
| Ước lượng được | Tech PIC ước được cỡ | 2.43, `tech-design.md` mục 6 |
| Nhỏ | Làm xong trong một sprint | 2.42 có từ 3 tới 6 tiêu chí chấp nhận; 2.43 Tech PIC xác nhận |
| Kiểm được | Có tiêu chí chấp nhận đạt hoặc không đạt | 2.42; script kiểm US có AC và mọi BR có AC |

## 3. Các bước chia ở 2.4

1. Dựng bản đồ story từ FR ở 2.3 và Impact Matrix ở 2.31. Hàng ngang là các bước trong hành trình người dùng; mỗi vai một làn.
2. Mỗi ô "vai và mục tiêu hoàn chỉnh" trên bản đồ là một story ứng viên. Đặt tên theo hành vi người dùng, không theo màn hình.
3. Kiểm từng ứng viên theo dấu hiệu quá lớn ở mục 4 và dấu hiệu quá nhỏ ở mục 6.
4. Ứng viên quá lớn thì tách theo các cách ở mục 5. Thử theo thứ tự trong bảng; dừng ở cách đầu tiên cho ra các story đều có giá trị riêng.
5. Gắn mỗi story vào một Unit, sắp thứ tự theo phụ thuộc và giá trị.
6. Kiểm truy vết: mọi FR có story phủ; story không truy về FR nào thì bỏ, hoặc bổ sung FR qua câu hỏi với PO.

## 4. Dấu hiệu story quá lớn

Các dấu hiệu dưới đây dùng để xem lại. Gặp một dấu hiệu thì cân nhắc tách; không tách thì ghi lý do trong thẻ US.

| Dấu hiệu | Ví dụ | Máy kiểm |
|---|---|---|
| Tên có chữ "và" nối hai việc người dùng làm riêng được | "Tạo và chia sẻ báo cáo" | `po-tools.py check` ở 2.4, cảnh báo |
| Có hơn một vai cùng hưởng giá trị | "Người dùng gửi yêu cầu, quản trị viên duyệt yêu cầu" | Không |
| Luồng chính hơn 7 bước, hoặc hơn 3 nhánh đáng kể | Luồng đặt hàng gồm cả chọn hàng, thanh toán, giao hàng | Không |
| Gồm cả phần cấu hình của quản trị và phần sử dụng của người dùng cuối | "Cấu hình và dùng mã giảm giá" | Không |
| Chạm hơn 2 module | | Không |
| Có hơn 6 tiêu chí chấp nhận | | `po-tools.py check` ở 2.42, cảnh báo |
| Tech PIC ước hơn một sprint | | 2.43 |

## 5. Cách tách

| # | Cách | Khi nào dùng | Ví dụ |
|---|---|---|---|
| 1 | Theo bước trong luồng | Luồng nhiều bước, mỗi bước cho người dùng một kết quả dùng được | "Đặt hàng" thành chọn hàng vào giỏ, thanh toán, theo dõi đơn |
| 2 | Theo vai | Hai vai cùng hưởng giá trị khác nhau từ một nhu cầu | "Khoá tài khoản" thành người dùng bị khoá tạm và tự mở sau một thời gian, quản trị viên mở khoá ngay |
| 3 | Theo biến thể nghiệp vụ | Một mục tiêu có nhiều luật khác nhau, mỗi luật dùng được riêng | "Tính phí vận chuyển" thành phí cố định, phí theo cân nặng, miễn phí theo ngưỡng đơn |
| 4 | Theo biến thể dữ liệu | Nhiều loại đầu vào hoặc nguồn dữ liệu | "Nhập danh sách người dùng" thành nhập từ file, đồng bộ từ hệ thống khác, xử lý bản ghi trùng |
| 5 | Theo thao tác trên một đối tượng | Quản lý một đối tượng có xem, tạo, sửa, xoá | Làm phần xem trước, sau đó tạo, sửa, xoá |
| 6 | Luồng đơn giản trước, ngoại lệ sau | Luồng chính rõ, ngoại lệ nhiều | Luồng chính thành một story; xử lý lỗi và trường hợp đặc biệt thành story sau |
| 7 | Chạy được trước, chạy nhanh sau | Có yêu cầu về hiệu năng hoặc khối lượng lớn | "Tìm kiếm" thành tìm được kết quả, sau đó tìm dưới 1 giây trên dữ liệu lớn |
| 8 | Theo kênh | Mỗi kênh như web, ứng dụng di động, cổng vận hành dùng được riêng | "Xem lịch" thành xem trên web, xem trên ứng dụng |

Cách 3 khác với chia mỗi business rule thành một story. Chỉ tách theo biến thể khi người dùng dùng được riêng từng biến thể. Một rule đơn lẻ được viết trong story chứa nó.

## 6. Dấu hiệu story quá nhỏ

- Không có giá trị riêng: chỉ một field, một nút, một rule, một câu thông báo.
- Không kiểm được độc lập: phải chạy story khác mới thấy kết quả.

Gặp các dấu hiệu này thì gộp vào story có cùng vai và cùng mục tiêu.

## 7. Không chia theo

| Cách chia | Vì sao không | Cách thay thế |
|---|---|---|
| Màn hình | Một mục tiêu đi qua nhiều màn; một màn phục vụ nhiều story. Màn là cách chia của Design | Chia theo mục tiêu của vai |
| Tầng kỹ thuật như frontend, backend | Không phần nào tự giao được giá trị cho người dùng | Dev chia sub-task trên Jira |
| Từng business rule | Story chỉ còn một câu, số story phình theo số rule | Rule nằm trong story, ở PRD |
| Việc kỹ thuật thuần như migration, dựng bảng, cấu hình hạ tầng | Không có vai người dùng; đây là việc của Dev | Dev tạo task kỹ thuật trên Jira, gắn vào Unit of work |
| Người làm hoặc team | Story dùng để nghiệm thu; phân công do từng team tự chia | Mỗi team chia việc từ story |
| Giải pháp giao diện, ví dụ "danh sách thả xuống có ô chọn" | Story mô tả nhu cầu; cách hiển thị do Design quyết | Ghi nhu cầu: "chọn nhiều danh mục để lọc" |

## 8. Xác nhận và thay đổi

- Ở 2.43, Tech PIC ghi trong `tech-design.md` story nào quá lớn để làm trong một sprint; Design PIC báo story nào trải qua nhiều luồng màn tách được. Decision Brief đưa ra họp; tách thì đi change request trên PRD trước khi sinh Story List, và ghi quyết định vào `decisions.md`.
- Sau khi PRD đã duyệt, tách story qua change request. Story cũ giữ mã; phần tách ra nhận số mới; tiêu chí chấp nhận chuyển đi nhận mã mới, theo `id-conventions.md`. Story List được sinh lại.
- Trên Jira, Dev có thể gom nhiều story vào một Unit of work hoặc chia một story thành nhiều sub-task. Việc đó không đổi story và không đổi mã.

## 9. Ví dụ

Yêu cầu: khoá tài khoản khi người dùng đăng nhập sai nhiều lần liên tiếp; quản trị viên mở khoá được; số lần sai và thời gian khoá cấu hình được.

Cách chia sai:

| Chia theo | Kết quả | Lỗi |
|---|---|---|
| Màn hình | Màn đăng nhập; màn quản trị người dùng; màn cấu hình | Mục tiêu "được bảo vệ khỏi đoán mật khẩu" bị cắt qua 3 story, không story nào nghiệm thu riêng được |
| Tầng kỹ thuật | Hàm đếm số lần sai; giao diện báo khoá | Không phần nào giao được giá trị cho người dùng |

Cách chia đúng:

| US | Vai và mục tiêu | Cách tách | Unit |
|---|---|---|---|
| US1 | Người dùng bị khoá tạm sau 5 lần sai liên tiếp, tự mở sau 30 phút, để tài khoản không bị đoán mật khẩu | Story gốc | U1 |
| US2 | Quản trị viên mở khoá ngay một tài khoản, để người dùng không phải chờ | Theo vai | U1 |
| US3 | Quản trị viên đổi số lần sai và thời gian khoá, để hợp với chính sách của tổ chức | Tách phần cấu hình khỏi phần sử dụng | U2 |
| US4 | Người dùng nhận email khi tài khoản bị khoá. PO còn phải quyết có làm không | Theo bước trong luồng | U2 |

## 10. So với AWS AI-DLC

Đối chiếu với AWS AI-DLC Workflows 2.11, `engine/knowledge/user-story-patterns.md` và `product-guide.md`.

| Nội dung | AWS | PO-Workflow | Lý do khác |
|---|---|---|---|
| Ai chia story | Product agent ở 2.4; Design, Dev, QA góp ý cùng lúc khi bật cộng tác | PO chia ở 2.4; 3 PIC xác nhận cỡ và cách chia ở 2.43 sau khi đọc PRD | Các PIC là người thật, nên đọc PRD chi tiết một lần và chốt trong một buổi họp |
| Tiêu chí | INVEST | INVEST, kèm nơi kiểm cụ thể trong quy trình | Không khác |
| Tiêu chí chấp nhận | Viết ngay ở 2.4, mỗi story 3 tới 6 | Viết ở 2.42, trước khi các team thiết kế; con số 3 tới 6 dùng làm dấu hiệu cỡ story | Các team cần AC để thiết kế và lập kế hoạch test |
| Cách tách | 6 cách: bước trong luồng, biến thể rule, biến thể dữ liệu, giao diện, xem tạo sửa xoá, hiệu năng | 8 cách: giữ 6 cách của AWS, thêm theo vai và luồng đơn giản trước; giao diện hiểu là kênh dùng được riêng | Sản phẩm có nhiều vai và nhiều cổng, 2 cách thêm gặp thường xuyên |
| Lỗi thường gặp | Quá lớn, quá kỹ thuật, không có giá trị, tên ghép nhiều việc, mô tả giải pháp | Giữ cả 5; thêm chia theo màn hình, theo tầng kỹ thuật, theo từng rule | 3 lỗi thêm là lỗi thường gặp khi PO viết PRD theo màn hình |
| Bản đồ story | Có, để thấy khoảng trống trong hành trình người dùng | Bước 1 của quy trình chia | Không khác |
| Chia việc kỹ thuật | Unit of work ở 2.7, theo kiến trúc, có bảng ghép Unit với story | Tech PIC chia Unit of work ở `tech-design.md` tại 2.43 với profile M, L; Dev chia việc chi tiết trên Jira | Ngoài phạm vi PO |

Nguồn: AWS AI-DLC Workflows 2.11; INVEST của Bill Wake, 2003; Patterns for Splitting User Stories của Richard Lawrence, 2009, cho cách 6 và cách 7.
