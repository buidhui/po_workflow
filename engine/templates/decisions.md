# Decisions: <slug>

Nhật ký quyết định của intent. Mỗi dòng một quyết định, lời PO ghi nguyên văn. AI đọc cột *Read when* để lấy đúng dòng cho stage đang làm, và để không hỏi lại câu đã có đáp án. Không xoá dòng. Quyết định bị thay thì thêm dòng mới và ghi "thay DECn". Cột *Người quyết* ghi tên người thật, lấy từ `git config user.name`, không ghi chung chung là PO; nhiều PO cùng làm một repo thì phải biết ai quyết.

| DEC | Ngày | Stage | Quyết định | Nguyên văn | Người quyết | Read when |
|---|---|---|---|---|---|---|
| DEC1 | <YYYY-MM-DD HH:MM> | 0 | Profile <X> vì <lý do> | "<lời PO>" | <tên trong git config user.name> | profile, phạm vi |

## Change requests
Theo BABOK 5.4 Assess Requirements Changes và 5.5 Approve Requirements. Mỗi thay đổi sau gate là một dòng; PO quyết Nhận, Hoãn hoặc Bác trước khi sửa artifact nào.

| CR | Ngày | Người yêu cầu | Thay đổi | Lý do | Mã bị chạm | Lợi ích, mục tiêu bị ảnh hưởng | Effort, mốc | Độ khẩn | Stage mở lại | DEC | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|---|---|

Trạng thái: Đề xuất, Nhận, Hoãn, Bác, Xong.

## Rủi ro
Sổ rủi ro của intent, theo BABOK 6.3 Assess Risks và 10.38 Risk Analysis and Management. Rủi ro nêu ở artifact nào cũng ghi vào đây một lần, artifact chỉ trỏ mã `RK<n>`.

| RK | Rủi ro | Khả năng | Tác động | Mức | Cách xử lý | Owner | Stage phát hiện | Trạng thái |
|---|---|---|---|---|---|---|---|---|

Cách xử lý: tránh, giảm, chuyển, chấp nhận. Trạng thái: mở, đang xử lý, đã chấp nhận, đã đóng.

## Accepted risks
| DEC | Finding hoặc RK | Vì sao chấp nhận, lời PO |
|---|---|---|
