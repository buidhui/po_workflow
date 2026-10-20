# /new-domain

Dựng khung knowledge base của một sản phẩm trong `domain/`, theo `engine/standards/domain-kb.md`. Phần cần người, như duyệt từng file KB, viết corner checklist, vẫn là người làm; lệnh này tạo khung từ template, hỏi đúng câu, và ghi đúng nơi. Đọc `DOMAIN-SETUP.md` trước khi chạy.

## 0. Kiểm an toàn
- `intents/` còn intent nào thì dừng: domain mới dựng ở repo mới, không đè lên repo đang có việc. Nói PO clone repo `po-workflow` sang thư mục mới, sau đó chạy lại.
- `domain/domain.md` đang có thì dừng và hỏi PO có muốn xoá domain hiện tại không. Chỉ xoá sau khi PO xác nhận.

## 1. Hỏi PO, một lượt
Hộp chọn hoặc chat, ghi nguyên văn. Danh sách thông tin cần có ở `engine/standards/domain-kb.md` mục 6; câu nào PO chưa trả lời được thì ghi `❓PO` và đưa vào vùng chưa phủ.
1. Tên sản phẩm, tên công ty, mã sản phẩm theo danh mục của công ty, dùng trong mã tính năng cho mọi team, ví dụ `APP`; các ứng dụng hoặc portal
2. Một tổ chức hay nhiều tổ chức dùng chung; hằng số nào phải cấu hình theo tổ chức
3. Vai người dùng chính; thiết bị hỗ trợ và mức accessibility mặc định, ví dụ web máy tính và điện thoại, WCAG 2.1 AA
4. Nguồn theo bảng ở `engine/standards/domain-kb.md` mục 6: tài liệu người dùng, danh sách module, schema dữ liệu, đặc tả API, ma trận phân quyền, danh sách sự kiện, hệ ngoài, số liệu vận hành, định hướng sản phẩm, sự cố từng gặp. Mỗi nguồn ở đâu, còn cập nhật hay là bản chốt
5. Thư mục ngoài repo được phép đọc để cập nhật KB
6. Sản phẩm so sánh mặc định cho Market Research, tối đa ba
7. Nơi lưu tài liệu người dùng của sản phẩm và các đối tượng người dùng, mỗi đối tượng một bài User Guide
8. Dự án Jira nhận Story List: project key, project name, project type nếu khác `software`

## 2. Dựng khung
- Tạo `domain/` và chép mười một file từ `engine/templates/domain/`: `domain.md`, `00-index.md`, `glossary.md`, `concept-model.md`, `data-model.md`, `permissions.md`, `integrations.md`, `events.md`, `nfr-baseline.md`, `product-direction.md`, và `module.md` thành `01-<module>.md` cho từng module PO kể ở câu 4. Bỏ `integrations.md`, `events.md` nếu sản phẩm không có
- Điền `domain.md` từ câu trả lời: frontmatter `domain`, `product`, `company`, `code`, `names`, `jira_project_key`, `jira_project_name`, `jira_project_type`; mục 1 từ câu 1 tới 3; mục 2 là bảng nguồn từ câu 4, cột đối chiếu lần cuối để trống; mục 3 bản đồ KB khớp các file vừa tạo; mục 4 phần 1.2 từ câu 6 và phần User Guide từ câu 7. Điểm chưa biết ghi `❓PO`, không tự điền
- Mỗi file KB chưa có nội dung thì thêm dòng `status: chưa viết` ở đầu file; `doctor` cảnh báo cho tới khi viết xong
- Chép `engine/knowledge/corner-checklist-aws.md` thành `corner-checklist.md`, thêm đầu file dòng "Chưa viết lại cho <sản phẩm>, xem DOMAIN-SETUP.md mục 6"
- `memory/project.md` giữ bản trống của repo engine, thêm dòng ghi ngày khởi tạo domain. `memory/team.md` giữ nguyên, vì đó là bài học dùng chung đi theo engine
- `intents/` chỉ còn `.gitkeep`

## 3. Dựng KB cùng PO
Không tự làm cả KB trong một lượt. Theo `DOMAIN-SETUP.md` mục 4: hỏi PO bắt đầu từ nguồn nào, chắt lọc thành một file theo template, trình PO duyệt, ghi ngày đối chiếu vào `domain.md` mục 2, sau đó sang file sau. Mã rule và loại rule theo `engine/standards/domain-kb.md` mục 4. Vùng nguồn không phủ ghi vào `00-index.md` mục Vùng chưa phủ.

## 4. Kết thúc
Trình PO: file đã tạo, file nào còn `chưa viết`, câu nào trong `domain.md` còn `❓PO`, thông tin nào ở bảng mục 6 của chuẩn KB còn thiếu, và ba việc kế tiếp: duyệt KB từng file, viết lại corner checklist, chạy thử một intent profile S. Chạy `python3 engine/scripts/po-tools.py doctor`: KB tối thiểu, bản đồ KB, nguồn và tên sản phẩm trong engine. Tự kiểm theo checklist cuối `DOMAIN-SETUP.md`.
