# Decisions: <slug>

Nhật ký quyết định của intent. Mỗi dòng một quyết định, lời PO ghi nguyên văn. AI đọc cột *Read when* để lấy đúng dòng cho stage đang làm, và để không hỏi lại câu đã có đáp án. Không xoá dòng. Quyết định bị thay thì thêm dòng mới và ghi "thay DECn". Cột *Người quyết* ghi tên người thật, lấy từ `git config user.name`, không ghi chung chung là PO; nhiều PO cùng làm một repo thì phải biết ai quyết.

| DEC | Ngày | Stage | Quyết định | Nguyên văn | Người quyết | Read when |
|---|---|---|---|---|---|---|
| DEC1 | <YYYY-MM-DD HH:MM> | 0 | Profile <X> vì <lý do> | "<lời PO>" | <tên trong git config user.name> | profile, phạm vi |

## Accepted risks
| DEC | Finding | Vì sao chấp nhận |
|---|---|---|
