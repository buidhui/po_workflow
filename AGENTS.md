# PO-Workflow

Repo này dùng để nhận yêu cầu, phân tích, viết PRD theo template PRD chuẩn làm đầu vào cho Design, Tech và QA, sinh Story List để import lên Jira, và viết User Guide sau khi Dev làm xong. Repo chỉ phân tích yêu cầu và viết tài liệu. Engine không phụ thuộc sản phẩm; dữ kiện sản phẩm nằm trong domain pack.

File này là luật chung cho mọi công cụ AI làm việc trên repo; `CLAUDE.md` chỉ nhập lại file này cho Claude Code. Quy tắc chi tiết nằm trong `engine/protocol/` và từng file stage, không lặp lại ở đây. Tài liệu liên quan:

- [README.md](README.md): phương pháp, từng stage, chuẩn bàn giao, đối chiếu với AWS AI-DLC
- [USER-GUIDE.md](USER-GUIDE.md): thao tác
- [GLOSSARY.md](GLOSSARY.md): thuật ngữ và họ mã
- [DOMAIN-SETUP.md](DOMAIN-SETUP.md): đưa một sản phẩm mới vào quy trình
- [CHANGELOG.md](CHANGELOG.md): phiên bản engine và cách nâng cấp

## Cấu trúc repo

| Thư mục | Nội dung | Thuộc về |
|---|---|---|
| `engine/` | Stage, lệnh, protocol, template, checklist, agent, script, kiến thức vai PO. Không phụ thuộc sản phẩm, không phụ thuộc công cụ | Engine |
| `engine/standards/` | Chuẩn bàn giao chung với Design, Tech, QA: nguyên tắc chia story, quy ước mã, quy tắc bàn giao, ADR | Engine |
| `domain/` | Domain pack của sản phẩm đang cài | Sản phẩm |
| `intents/` | Hồ sơ từng yêu cầu | Sản phẩm |
| `memory/` | `team.md` bài học dùng chung, gộp theo dòng khi nâng cấp engine; `project.md` bài học của sản phẩm | Cả hai |
| `.claude/` | Phần cấu hình riêng cho Claude Code, chỉ chứa lối tắt: mỗi file trong `commands/` là một lệnh gạch chéo trỏ tới file lệnh trong `engine/commands/`, stage chạy qua `/po` nên không có lệnh riêng; `agents/` trỏ tới `engine/agents/`; `settings.json` là quyền và hook, hook chạy `engine/scripts/po-hook.py` | Công cụ |
| `.po/` | Sổ lượt người `turns.jsonl` và giờ chạy hook trên máy này. Không commit, AI không đọc và không sửa | Công cụ |
| `.mcp.json` | MCP server cho Claude Code, ví dụ trình duyệt để chụp màn hình User Guide. Phải nằm ở gốc repo vì Claude Code chỉ đọc ở đó | Công cụ |

Công cụ AI khác: đọc file này, sau đó chạy lệnh bằng cách đọc `engine/commands/<lệnh>.md` hoặc `engine/stages/<stage>.md` và làm theo. Phần cấu hình riêng cho công cụ khác chỉ dựng khi dùng công cụ đó.

## Luồng làm việc

Một luồng duy nhất theo AWS AI-DLC Workflows, phiên bản ghi trong `engine/knowledge/README.md`. Mỗi yêu cầu là một intent trong `intents/`.

- Lệnh: `/new-intent` tạo intent, `/po` chạy stage kế tiếp, `/po-status` xem trạng thái, `/po-review` review độc lập, `/po-replay` tóm lược diễn biến của intent khi bàn giao cho người khác, `/po-stories` sinh Story List để import lên Jira sau gate 2.43, profile S thì sau gate 2.42.
- Đầu ra của PO là đầu vào của Design, Tech và QA, nên theo chuẩn trong `engine/standards/`: mã tính năng cấp khi tạo intent, tiêu chí chấp nhận có mã trong PRD, mỗi user story một story trên Jira.
- Script: `python3 engine/scripts/po-tools.py` với `next`, `check`, `review-start`, `approve`, `trace`, `status`, `doctor`, `index`, `replay`, `feature-id`, `stories`, `dor`, `migrate`. Số liệu, tiến độ và stage kế lấy từ script, không tự đếm.
- Nghi thức ở `engine/protocol/*.md`, thuật ngữ ở `GLOSSARY.md`, bài học ở `memory/team.md` và `memory/project.md`.
- Tên file artifact ổn định, phiên bản ở frontmatter, bản duyệt chụp vào `archive/` của intent theo `gate-protocol.md`. Không tạo file `v0.x`.
- Intent chuyển từ luồng cũ giữ họ mã cũ trong tài liệu của chúng, ghi ở `intent.md` của từng intent. Luồng cũ nằm ở tag `pre-aidlc`.

## Domain pack

Mọi dữ kiện riêng của sản phẩm nằm trong `domain/`: manifest `domain.md`, KB, corner checklist, template PRD và User Guide của công ty. Đọc `domain.md` ở đầu mỗi phiên và ở bước Load của mọi stage. Engine không ghi cứng dữ kiện sản phẩm, kể cả tên sản phẩm; sản phẩm đang cài ghi ở frontmatter của `domain.md`. Đổi domain theo [DOMAIN-SETUP.md](DOMAIN-SETUP.md).

## Knowledge

| Thư mục | Nội dung |
|---|---|
| `domain/` | Domain pack. `domain.md` là manifest: KB nào trả lời câu gì, nguồn sống và bản chốt, dữ kiện cho từng stage, đích publish |
| `engine/knowledge/` | Kiến thức vai PO chép từ AWS AI-DLC, không phụ thuộc sản phẩm; `corner-checklist-aws.md` là bản gốc để mỗi domain viết lại |
| `memory/team.md` | Bài học dùng chung đã giữ lại tại gate, đi theo engine. Đọc ở bước Load của mọi stage |
| `memory/project.md` | Bài học riêng của sản phẩm đang cài. Đọc ở bước Load của mọi stage, làm mới khi đổi domain |

### Quy ước ký hiệu

| Ký hiệu | Nghĩa |
|---|---|
| `BR-<MODULE>-NN` | Business rule trong KB, có trong tài liệu chính thức, giữ nguyên văn |
| `KB-<MODULE>-NN` | Rule AI trích từ văn xuôi, chưa được duyệt |
| `❓PO` | Chưa rõ, không dùng làm căn cứ |
| `[suy ra]` | AI suy luận ra; nguồn không nói trực tiếp |
| Hidden | Tính năng có code nhưng đang ẩn, vẫn phải xét khi phân tích ảnh hưởng |

### Khi nào đọc lại nguồn

KB là bản chụp. Nguồn sống là nguồn còn bản gốc bên ngoài, như schema DB, API spec, tài liệu người dùng: yêu cầu chạm tới vùng nào thì đọc lại nguồn của vùng đó, và quá 30 ngày kể từ lần đối chiếu cuối thì đọc lại trước khi dùng. Bản chốt là nguồn không còn file gốc: nghi ngờ thì hỏi PO, không tự suy. Danh sách nguồn và vùng KB chưa phủ nằm trong `domain.md` mục 2 và 3. Vùng chưa phủ ghi `❓PO`, không kết luận "không ảnh hưởng". Đọc lại thấy khác KB thì cập nhật KB và ngày đối chiếu ngay.

## Cách làm việc

- Trả lời bằng tiếng Việt. Tên stage, mã và thuật ngữ theo `GLOSSARY.md`.
- Nêu kết luận trước, giải thích sau. Phản biện khi thấy lỗ hổng. Hỏi lại khi thiếu thông tin, không đoán.
- Tách rõ Fact, Assumption, Open Question, Recommendation. Không tự điền dữ kiện: thiếu thông tin nhỏ thì ghi Assumption; thiếu thông tin làm đổi phạm vi, rule, dữ liệu hoặc luồng thì ghi Open Question; ô không suy ra được thì ghi `❓PO`.
- Không tự chốt quyết định thay PO; chỉ gợi ý dưới nhãn Recommendation. Lời duyệt và câu trả lời của PO ghi nguyên văn.
- Gate: đánh `[?]`, trình, kết thúc lượt và chờ PO. Chỉ `po-tools.py approve` được đánh `[x]`, và lệnh này chỉ ghi khi `--words` có nguyên văn trong một lượt PO gõ hoặc chọn sau lần sửa artifact cuối. Không tự duyệt, không chép lời duyệt từ lượt cũ. Công cụ không có hook thì PO tự chạy approve trong terminal.
- Sửa artifact đã duyệt phải qua `/change-request`; `decisions.md` chỉ thêm dòng; file review chỉ AI Reviewer ghi; ba file thiết kế `ux-design.md`, `tech-design.md`, `test-design.md` chỉ các team ghi, AI của PO đọc để đối chiếu và viết Decision Brief. Hook của Claude Code chặn các việc trái quy tắc này, trừ việc sửa ba file thiết kế: hook không phân biệt được phiên của PO với phiên của PIC, nên quy tắc đó AI tự giữ. Hook chỉ chặn lỗi vô ý, nên AI không tìm cách đi vòng qua lệnh shell.
- Không thiết kế kỹ thuật chi tiết. Ghi điều phải đúng, để Dev quyết cách làm. Không hỏi câu kỹ thuật thay Dev; chỉ hỏi câu mà đáp án làm đổi phạm vi hoặc business rule. Cần biết một cơ chế kỹ thuật có tồn tại không thì hỏi PO; có endpoint không có nghĩa là có tính năng.
- Tài liệu bàn giao, gồm Initiative Brief, PRD, Decision Brief, Story List và User Guide: không để lại dấu vết quy trình, không viết tắt, mã nào cũng kèm nội dung, các mã đứng cạnh nhau ngăn bằng dấu `·`. Trạng thái duyệt ghi ai duyệt, không ghi số gate. Giữ `❓PO` và bảng lịch sử phiên bản viết bằng lời.
- Trích mã trong trao đổi thì kèm nội dung một dòng. Một intent profile L sinh hàng trăm mã; buộc người đọc mở file để tra là lỗi của người viết.
- Viết tài liệu bằng văn viết: câu đầy đủ chủ vị, không dùng khẩu ngữ, không in đậm trong đoạn văn, không dùng gạch ngang dài để nối ý.

Các quy tắc rút từ lỗi đã gặp và lý do nằm ở `memory/team.md` và `memory/project.md`. Thêm bài học qua vòng học tại gate, không sửa tay giữa chừng một intent.

## Ranh giới

Repo chỉ làm phân tích yêu cầu và viết tài liệu. Không bàn quy trình vận hành team. Không đọc thư mục ngoài repo, trừ thư mục nguồn ghi trong `domain.md` khi cập nhật KB. Không tự mở rộng phạm vi KB.

Gặp điều đáng chú ý nhưng ngoài phạm vi thì ghi một dòng vào mục "câu hỏi để sau" của KB, sau đó quay lại việc chính.

## Bàn giao

Đích publish tài liệu và đích User Guide ghi trong `domain.md` mục 4. Bản publish dành cho người đọc. Story List để import lên Jira nằm trong `intents/<intent>/stories/`, theo `engine/standards/handoff-rules.md`. Agent của Dev đọc PRD trong repo theo tag đã gắn, qua chỉ mục `intents/INDEX.md` do `po-tools.py index` sinh. Chi tiết ở README mục 6.

## Sửa engine

Phần này cho người giữ engine và AI được giao sửa engine, theo mục Working on This Project trong `AGENTS.md` của AWS. Engine là mọi file trong `engine/`, `.claude/commands/`, `.claude/agents/` và các file tài liệu ở gốc ghi trong `engine/MANIFEST.txt`.

Thứ tự mỗi lần sửa:
1. Sửa lỗi script: thêm ca tái hiện lỗi vào `engine/tests/fixtures/` trước, chạy để xác nhận ca đó hỏng, sau đó mới sửa.
2. Chạy `python3 engine/scripts/po-tools.py selftest`. Phải đạt.
3. Chạy `python3 engine/scripts/po-tools.py manifest --write`.
4. Ghi vào CHANGELOG, dưới bản chưa phát hành. VERSION chỉ tăng khi phát hành: đổi VERSION, đổi tiêu đề mục CHANGELOG, chạy lại `manifest --write`, commit, gắn tag `engine-v<X.Y.Z>`.
5. Push. GitHub Actions chạy `selftest` trên Python 3.9 và bản mới nhất, cùng `engine-check --strict`.

Selftest bắt được và không bắt được:

| Việc | Selftest bắt | Phải tự kiểm |
|---|---|---|
| Thêm lệnh cho `po-tools.py` | Lệnh chưa có ca kiểm; tài liệu nhắc lệnh không có | Câu chữ hướng dẫn trong USER-GUIDE |
| Thêm stage | Bảng metadata thiếu dòng; đường dẫn Template, Checklist không có; README mục 3.2 thiếu dòng stage; reviewer lệch `profiles.md` | Nội dung stage so với AWS; dòng Lệch so với AWS |
| Sửa template | Không bắt, trừ heading bắt buộc khi có fixture dùng template đó | Các stage và checklist nhắc tới mục đã đổi |
| Đổi tên file trong `engine/` | Đường dẫn `engine/...` gãy trong mọi tài liệu | Liên kết ngoài repo, deck |
| Phát hành | VERSION khác mục mới nhất của CHANGELOG hoặc đầu MANIFEST; thiếu mục Nâng cấp hoặc dòng Tương thích | Hướng dẫn nâng cấp đúng với intent đang chạy |

Mỗi bản trong CHANGELOG có dòng `Tương thích:` với một trong ba giá trị: chỉ chép engine; chép engine và chạy migrate; phải sửa intent bằng tay. Repo sản phẩm khác đọc dòng này để biết phải làm gì khi nâng cấp.
