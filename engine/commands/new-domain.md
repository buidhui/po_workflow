# /new-domain

Dựng phần khung của một domain pack. Phần cần người, như duyệt KB, viết corner checklist, vẫn là người làm; lệnh này chỉ tạo khung, hỏi đúng câu, và ghi đúng nơi. Đọc `DOMAIN-SETUP.md` trước khi chạy.

## 0. Kiểm an toàn
- `intents/` còn intent nào thì dừng: domain mới dựng ở repo mới, không đè lên repo đang có việc. Nói PO clone sang thư mục mới, sau đó chạy lại.
- `domain/domain.md` đang có thì hỏi PO: giữ `templates/` làm điểm xuất phát hay bỏ. Mọi thứ khác trong thư mục domain sẽ bị xoá; chỉ xoá sau khi PO xác nhận.

## 1. Hỏi PO, một lượt
Hộp chọn hoặc chat, ghi nguyên văn:
1. Tên sản phẩm, tên công ty, mã sản phẩm theo danh mục của công ty, dùng trong mã tính năng cho mọi team, ví dụ `APP`, portal hoặc ứng dụng con
2. Một tenant hay đa tenant; hằng số nào phải cấu hình theo tenant
3. Vai người dùng chính; thiết bị hỗ trợ và mức accessibility mặc định, ví dụ web máy tính và điện thoại, WCAG 2.1 AA
4. Nguồn: tài liệu người dùng ở đâu, schema DB ở đâu, API spec ở đâu; nguồn nào còn cập nhật, nguồn nào là bản chốt
5. Thư mục ngoài repo được phép đọc để cập nhật KB
6. Sản phẩm so sánh mặc định cho Market Research, tối đa ba
7. Đích publish tài liệu: Lark, Confluence, Notion, khác; space và node cha nếu có
8. Đích User Guide: GitBook hoặc công cụ khác, repo nào, cho đối tượng nào
9. Công ty có bắt buộc template PRD riêng cho sản phẩm này không. Mặc định là không: PRD theo template chuẩn `engine/templates/prd.md`, cơ sở ở `engine/standards/adr/0004-template-prd-chuan.md`
10. Nếu câu 9 là có: đường dẫn hoặc nội dung template, và tên mục công ty cấm đổi
11. Dự án Jira nhận Story List: project key, project name, project type nếu khác `software`

## 2. Dựng khung
- Xoá `domain/` trừ `templates/` nếu PO giữ; tạo lại thư mục
- Viết `domain.md` theo sáu mục của `DOMAIN-SETUP.md` mục 5, điền từ câu trả lời; frontmatter có `domain`, `product`, `company`, `code`, `names`, và `jira_project_key`, `jira_project_name`, `jira_project_type` từ câu 11; điểm chưa biết ghi `❓PO`, không tự điền. Mục 3 bản đồ KB liệt kê các file sẽ viết với tên và câu hỏi mỗi file trả lời, chưa có nội dung
- Ghi bảng nguồn từ câu 4 vào `domain.md` mục 2, cột đối chiếu lần cuối để trống. Bảng nguồn chỉ có ở đó, không lặp ở file khác
- Viết `00-index.md` khung: danh sách file KB dự kiến, mục Trạng thái tính năng trống, mục câu hỏi để sau trống
- Tạo từng file KB trong bản đồ với frontmatter `status: chưa viết`, một dòng mô tả câu hỏi file sẽ trả lời
- Chép `engine/knowledge/corner-checklist-aws.md` thành `corner-checklist.md`, thêm đầu file dòng "Chưa viết lại cho <sản phẩm>, xem DOMAIN-SETUP.md mục 6"
- `templates/prd.md`: chỉ tạo khi câu 9 là có, từ câu 10; ghi danh sách tên mục bắt buộc giữ vào `domain.md` mục 4 phần 2.42. File này ghi đè template chuẩn, script không kiểm tên mục của nó
- `memory/project.md` về bản trống: giữ đoạn mở đầu, xoá mọi heading và dòng bài học, thêm dòng ghi ngày khởi tạo domain. `memory/team.md` giữ nguyên, vì đó là bài học dùng chung đi theo engine
- `intents/` chỉ còn `.gitkeep`

## 3. Dựng KB cùng PO
Không tự làm cả KB trong một lượt. Theo `DOMAIN-SETUP.md` mục 4: hỏi PO bắt đầu từ nguồn nào, chắt lọc thành một file, trình PO duyệt, ghi ngày đối chiếu vào `domain.md` mục 2, sau đó sang file sau. Mã rule `BR-<MODULE>-NN` cho rule có trong tài liệu chính thức, `KB-<MODULE>-NN` cho rule AI trích. Vùng nguồn không phủ ghi vào `api-surface` mục vùng chưa phủ.

## 4. Kết thúc
Trình PO: thư mục đã tạo, file nào còn `chưa viết`, câu nào trong `domain.md` còn `❓PO`, và ba việc kế tiếp: duyệt KB từng file, viết lại corner checklist, chạy thử một intent profile S. Chạy `python3 engine/scripts/po-tools.py doctor` để chắc engine đọc được domain pack và không còn tên sản phẩm cũ trong engine cây mới. Tự kiểm theo checklist cuối `DOMAIN-SETUP.md`.
