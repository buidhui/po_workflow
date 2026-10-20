# ADR 0002: Giao việc theo story trên Jira

| | |
|---|---|
| Trạng thái | Đã quyết, thay ADR 0001. Phần checkpoint trên HLD Brief và thời điểm sinh Story List với profile M, L đã thay bằng ADR 0003 |
| Ngày | 2026-10-19 |
| Người quyết định | PO phụ trách PO-Workflow |

## Bối cảnh

ADR 0001 chọn file story Markdown trong repo của PO: mỗi user story một file, mục 1 chép từ PRD, mục 2 tới 4 do Design, Tech, QA viết. Khi rà lại luồng làm việc thật:

- Checkpoint của các team là buổi làm việc trên HLD Brief, trước khi có PRD. Sau PRD, story chỉ còn dùng để chia việc.
- Mục 1 của file story là bản chép từ PRD, phải đồng bộ mỗi khi PRD đổi.
- Các team đã chia việc và theo dõi trên Jira, và đã có mẫu import CSV cho Jira.

## Các lựa chọn đã xét

| Lựa chọn | Được | Mất |
|---|---|---|
| Giữ file story trong repo | Mọi thứ của một story nằm trong một file; máy kiểm được độ phủ test case | Bản chép nghiệp vụ phải đồng bộ; các team làm việc ở 2 nơi, repo và Jira |
| File story bỏ mục chép từ PRD | Không còn bản chép | File chỉ còn là phiếu giao việc, trùng vai với story trên Jira |
| Story List dạng CSV import lên Jira | Nghiệp vụ chỉ ở PRD; việc chia và theo dõi ở đúng công cụ các team đang dùng; import một lần cho cả intent | Story đã import phải sửa tay trên Jira khi PRD đổi; script không kiểm được độ phủ test case |

## Quyết định

Sau khi PRD được duyệt, `/po-stories` sinh một file CSV theo mẫu import của Jira, mỗi US một dòng. Các team làm việc trên story Jira. PRD là nguồn duy nhất của nghiệp vụ. Quy ước mã giữ nguyên.

## Hệ quả

- Không còn thư mục file story Markdown; `intents/<intent>/stories/` chỉ chứa các bản CSV theo phiên bản PRD.
- Các PIC vẫn cần quyền ghi repo cho HLD Brief, không cần cho phần giao việc.
- Điều kiện giao Dev chỉ kiểm phía PO: PRD đã duyệt, US có AC, mọi BR có AC, không còn `❓PO` và câu chặn. Độ phủ test case do QA theo dõi trên Jira.
- Khi PRD đổi, script in story nào đổi so với bản CSV trước để PO sửa trên Jira.
