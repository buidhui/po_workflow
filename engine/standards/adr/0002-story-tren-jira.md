# ADR 0002: Giao việc theo story trên Jira

| | |
|---|---|
| Trạng thái | Đã quyết định, thay ADR 0001. Phần checkpoint trên HLD Brief và thời điểm sinh Story List với profile M, L đã thay bằng ADR 0003. Bổ sung ngày 2026-10-23: đẩy story qua Jira MCP. Bổ sung ngày 2026-10-29: mỗi Unit là một story trên Jira. Xem hai mục cuối |
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
- Điều kiện sẵn sàng chỉ kiểm phía PO: PRD đã duyệt, US có AC, mọi BR có AC, không còn `❓PO` và câu chặn. Độ phủ test case do QA theo dõi trên Jira.
- Khi PRD đổi, script in story nào đổi so với bản CSV trước để PO sửa trên Jira.

## Bổ sung ngày 2026-10-23: đẩy story qua Jira MCP

### Bối cảnh

Phiên Claude Code của PO nay nối được Jira qua MCP và tạo issue trực tiếp. Import CSV có ba điểm yếu: PO phải tự import, khi PRD đổi thì phải sửa tay từng story theo danh sách đổi, và repo không biết story nào ứng với issue nào.

Đã tham khảo ba nguồn:

- AWS AI-DLC 2.11 không có tích hợp Jira; story nằm trong `stories.md` của repo.
- Spec Kit có lệnh `taskstoissues`, nay chuyển sang extension `github`: dùng GitHub MCP để tạo issue từ task, chống trùng bằng mã task trong tiêu đề, tìm cả issue đã đóng, kiểm remote trước khi tạo, không hỏi xác nhận.
- BABOK v3 mục 5.1 Trace Requirements và 4.4 Communicate Business Analysis Information: yêu cầu cần liên kết được hai chiều với nơi triển khai, và thông tin gửi đi phải được người nhận xác nhận.

### Các lựa chọn đã xét

| Lựa chọn | Được | Mất |
|---|---|---|
| Chỉ giữ CSV | Không phụ thuộc công cụ | Ba điểm yếu ở trên còn nguyên |
| Đẩy qua MCP, bỏ CSV | Một đường duy nhất | Engine phụ thuộc MCP; công ty không có MCP thì không bàn giao được |
| Giữ CSV, thêm đường đẩy qua MCP | Có MCP thì đẩy và cập nhật được; không có thì vẫn import CSV | Hai đường phải giữ cùng nội dung story |

### Quyết định

Giữ CSV làm đầu ra trung lập với công cụ và thêm đường đẩy qua Jira MCP bằng lệnh `po-tools.py jira-sync`. Script lập kế hoạch và ghi kết quả; AI gọi công cụ của MCP. Engine không phụ thuộc MCP.

- Ánh xạ mã story sang mã issue lưu ở `stories/jira-map.json`, commit cùng repo, kèm bản PRD đã đẩy và mã băm nội dung. Chống trùng bằng file này; mất file thì tìm theo nhãn mã story bằng JQL trước khi tạo, như cách Spec Kit tìm theo mã task.
- Mỗi lần chạy xếp story vào một việc: tạo, cập nhật, giữ nguyên, hoặc gắn nhãn `removed-from-prd` cho story không còn trong PRD. Không xoá issue.
- Đẩy cả story chưa đạt điều kiện sẵn sàng, mang nhãn `not-ready` và comment ghi lý do, để các team thấy sớm phạm vi; story đạt thì nhãn được bỏ. Nhãn dùng tiếng Anh vì nhãn Jira không chứa dấu cách và dùng chung giữa các team.
- Cập nhật chỉ thay mô tả kèm comment ghi bản PRD mới và các mã thêm, bỏ. Trước khi cập nhật, AI lấy bản trên Jira để script so với bản đẩy lần trước; issue đã bị sửa tay thì PO quyết định giữ hoặc ghi đè. Khác Spec Kit, PO phải đồng ý bằng lời trước khi đẩy, và script đối chiếu lời đó với sổ lượt người như ở gate.
- Sau khi tạo, story nêu ở Tiền điều kiện thành liên kết "is blocked by".
- Mã issue không ghi vào PRD. Bảng của lệnh `stories` và `intents/INDEX.md` đọc từ `jira-map.json`.
- `domain.md` có thêm `jira_story_type` và `jira_epic_mode` (`parent` hoặc `epic-link`); `doctor` kiểm giá trị.
- Chưa làm: đọc trạng thái story từ Jira về repo.

### Hệ quả

- `stories/` chứa thêm `jira-map.json` và `jira-plan.json`. Hook chặn sửa tay hai file này.
- PRD đổi qua change request thì lần đẩy sau tự cập nhật đúng các story đổi; PO không phải sửa tay trên Jira.
- Kết quả mỗi lần đẩy có một DEC trong `decisions.md`.

## Bổ sung ngày 2026-10-29: mỗi Unit là một story trên Jira

### Bối cảnh

Quyết định gốc đặt mỗi US là một story trên Jira. Trên thực tế, story trên Jira là đơn vị Dev ước lượng, đưa vào sprint và chia sub-task. Nhiều US nhỏ được Dev làm và QA nghiệm thu cùng lúc; theo dõi riêng từng US tạo nhiều issue nhỏ, và team thường gộp tay trên Jira, làm mất liên kết giữa issue và mã US. Đồng thời, bảng Unit of work trong `tech-design.md` có cột Phía: một Unit of work có thể chỉ gồm phần Backend, nên không làm story được, và trùng vai với sub-task.

Unit đã có hai tính chất của một story trên Jira: độc lập, theo quy tắc phụ thuộc một chiều ở 1.4, và có giá trị cùng mức ưu tiên riêng. Unit chỉ thiếu điều kiện về cỡ, và cỡ chỉ xác định được sau khi Tech PIC viết thiết kế ở 2.43.

Đã đối chiếu ba nguồn:

- AWS AI-DLC 2.11: proto-Unit ở 1.4 là bản nháp trong intent backlog; Unit of work ở 2.7 được xác định lại khi đã có story, mỗi Unit gồm nhiều story. AWS không quy định story trên công cụ quản lý việc tương ứng với cấp nào.
- Scrum Guide 2020: hạng mục Product Backlog được tinh chỉnh tới khi đủ nhỏ để hoàn thành trong một sprint.
- BABOK v3 mục 5.1 Trace Requirements: yêu cầu truy được tới nơi triển khai. Truy vết dựa trên mã của từng yêu cầu, không phụ thuộc số issue.

### Các lựa chọn đã xét

| Lựa chọn | Được | Mất |
|---|---|---|
| Giữ mỗi US một story | Truy vết đơn giản, điều kiện sẵn sàng theo từng US | Nhiều issue nhỏ; team gộp tay trên Jira và mất liên kết với mã US |
| Mỗi US một story, cho phép gộp các US cùng Unit bằng một dòng khai báo riêng | Giữ mặc định cũ | Thêm một cách nhóm thứ hai bên cạnh Unit; mặc định vẫn sinh nhiều issue nhỏ |
| Mỗi Unit là một story; Unit được xác nhận cỡ tại 2.43 | Một quy tắc duy nhất; story trên Jira giữ giá trị và thứ tự ưu tiên của PO; US vẫn là đơn vị nghiệm thu | Thay đổi Unit sau khi PRD được duyệt cần change request; một US chưa sẵn sàng giữ lại cả story |

### Quyết định

Chọn lựa chọn thứ ba.

- Unit lập ở 1.4 là bản nháp; ở 2.4 PO gắn mỗi US vào một Unit; ở 2.43 Tech PIC xác nhận mỗi Unit độc lập và vừa một sprint trong `tech-design.md` mục 7, đề xuất tách, gộp hoặc chuyển US.
- Thay đổi Unit quyết định trong buổi họp đi change request trên PRD mục 5 trước Alignment gate, như mọi quyết định làm đổi PRD.
- Bảng Units ở PRD mục 5 là bản chốt. Mỗi Unit là một story trên Jira, mã `<tính năng>-U<n>`; mỗi US thuộc đúng một Unit. Unit quá một sprint được tách thành hai Unit, không chia một Unit thành nhiều story.
- Story mang nhãn mã tính năng, mã story và mã của từng US; Description gồm khối của từng US. PRD giữ nguyên mã US, AC, BR, nên test case và commit vẫn dẫn chiếu tới từng US.
- Story đạt điều kiện sẵn sàng khi mọi US của Unit đạt; Unit ở cột Phụ thuộc thành liên kết "is blocked by".
- Khi PRD không có mục Units, như với profile S, cả PRD là một story `<tính năng>-U1`.
- `tech-design.md` bỏ bảng Unit of work, thay bằng bảng cỡ Unit và kế hoạch thực hiện; Dev chia sub-task trên Jira.

### Hệ quả

- `stories`, `dor`, `jira-sync`, `index` tính theo Unit. `check` của 2.42 báo khi bảng Units không khớp các khối US; `check` của 2.43 báo Unit chưa được Tech PIC xác nhận cỡ hoặc được ghi không vừa một sprint.
- Intent đã đẩy story theo từng US: lần đẩy sau, issue của US đầu tiên trong Unit trở thành story của Unit; issue riêng của các US còn lại mang nhãn `merged-into-story`, không bị xoá. Unit ghi "gộp vào U<n>" cũng mang nhãn này.
- Câu JQL chống trùng loại các issue đã có trong `jira-map.json`.
