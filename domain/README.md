# Knowledge base của sản phẩm

Thư mục này chứa knowledge base của sản phẩm mà PO đang làm: `domain.md` mô tả sản phẩm, phạm vi, nguồn sống và bản đồ KB; các file KB về thuật ngữ, mô hình khái niệm, mô hình dữ liệu, phân quyền, module, sự kiện, tích hợp, định hướng sản phẩm; corner checklist của sản phẩm. AI đọc thư mục này ở bước Load của mỗi stage để không hỏi lại điều đã có, và tra ở đây trước khi đặt câu hỏi cho PO. Cấu trúc theo `engine/standards/domain-kb.md`. Repo PO-Workflow gốc để trống thư mục này.

Đưa một sản phẩm vào quy trình: tạo repo riêng cho sản phẩm từ repo này, chạy `/new-domain` và làm theo `DOMAIN-SETUP.md`. Lệnh dựng khung từ `engine/templates/domain/`; người phụ trách cung cấp thông tin theo bảng ở `engine/standards/domain-kb.md` mục 6, sau đó PO cùng AI viết nội dung từng file.
