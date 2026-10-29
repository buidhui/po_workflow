# Hướng dẫn sử dụng PO-Workflow

Tài liệu này mô tả thao tác. Phương pháp và lý do của từng stage ở [README.md](README.md); thuật ngữ và họ mã ở [GLOSSARY.md](GLOSSARY.md).

| Người đọc | Mục cần đọc |
|---|---|
| PO | 1 tới 7, 10 tới 12 |
| Design PIC, Tech PIC, QA PIC | 1, 8 |
| Dev và agent AI của Dev | 9 |
| Người phụ trách quy trình | 2, 11 và [DOMAIN-SETUP.md](DOMAIN-SETUP.md) |

## Mục lục

1. [Quy trình tóm tắt](#1-quy-trình-tóm-tắt)
2. [Cài đặt](#2-cài-đặt)
3. [Cấu trúc thư mục](#3-cấu-trúc-thư-mục)
4. [Chạy một intent tới PRD](#4-chạy-một-intent-tới-prd)
5. [Trả lời AI và duyệt](#5-trả-lời-ai-và-duyệt)
6. [Thay đổi yêu cầu sau khi duyệt](#6-thay-đổi-yêu-cầu-sau-khi-duyệt)
7. [Bàn giao sau khi duyệt](#7-bàn-giao-sau-khi-duyệt)
8. [Dành cho Design PIC, Tech PIC, QA PIC](#8-dành-cho-design-pic-tech-pic-qa-pic)
9. [Dành cho Dev](#9-dành-cho-dev)
10. [Lệnh](#10-lệnh)
11. [Knowledge base của sản phẩm](#11-knowledge-base-của-sản-phẩm)
12. [Xử lý tình huống](#12-xử-lý-tình-huống)

## 1. Quy trình tóm tắt

Mỗi yêu cầu là một intent. Intent đi qua hai phase: Ideation xác định vấn đề và phạm vi; Inception chuyển phạm vi thành yêu cầu, phân tích ảnh hưởng, so sánh phương án, chia user story, viết PRD chi tiết, sau đó các team thiết kế từ PRD và thống nhất trên Decision Brief. Mỗi stage tạo một artifact và dừng ở một gate cho tới khi PO duyệt.

| Stage | Artifact | Gate | Thư mục trong intent |
|---|---|---|---|
| 1.1 Intent Capture & Framing | `intent-statement.md` | Profile L: gate riêng. Profile M: duyệt chung với 1.4 | `ideation/intent-capture/` |
| 1.2 Market Research | `competitive-analysis.md` | Chỉ khi cần so sánh với sản phẩm khác | `ideation/market-research/` |
| 1.4 Scope Definition | `scope-document.md`, danh sách Unit | Có | `ideation/scope-definition/` |
| 1.7 Approval & Handoff | Initiative Brief một trang | Có, kèm lựa chọn dừng intent | `ideation/approval-handoff/` |
| 2.3 Requirements Analysis | `requirements.md`, mã `FR1`, `NFR1` | Có | `inception/requirements-analysis/` |
| 2.31 Impact Analysis | `related-features-map.md`, `impact-matrix.md` | Có | `inception/impact-analysis/` |
| 2.32 Solution Options | `solution-options.md` | Chỉ khi có nhiều hướng giải | `inception/solution-options/` |
| 2.4 User Stories | `stories.md`, mã `US1` | Có | `inception/user-stories/` |
| 2.42 PRD Generation | PRD, `traceability.md` | Có | `inception/prd/` |
| 2.43 Design Alignment, profile M và L | Ba file thiết kế do các team viết, Decision Brief | Alignment gate, 3 PIC ký | `inception/ux-design/`, `tech-design/`, `test-design/`, `decision-brief/` |
| Sau gate 2.43, hoặc sau PRD với profile S | Story trên Jira, đẩy qua MCP hoặc import Story List | Không | `stories/` |
| Sau khi Dev hoàn thành | User Guide | Không | `user-guide/` |

Profile quyết định số stage. Khi tạo intent, AI đề xuất profile kèm lý do; PO có quyền đổi. Khi phân vân giữa hai profile, chọn profile lớn hơn.

| Profile | Khi nào | Stage chạy | Số gate |
|---|---|---|---|
| S | Một màn, không đổi data model, không đổi rule có sẵn, không chạm module khác | 2.3 và 2.42, PRD rút gọn | 2 |
| M | Tối đa hai module, thêm field nhưng không đổi quan hệ bảng, không xung đột, hướng giải đã rõ | 1.1 và 1.4 duyệt chung, 2.3, 2.31, 2.4, 2.42, 2.43 | 6 |
| L | Từ ba module, đổi data model, có xung đột, nhiều hướng giải, tích hợp ngoài hoặc chuyển đổi dữ liệu | Đủ 10 stage; 1.2 và 2.32 khi cần | 8 tới 10 |

Gate là điểm dừng bắt buộc. AI không chuyển sang stage tiếp theo khi chưa có lời duyệt rõ ràng, vì mỗi artifact là nền cho artifact sau: lỗi ở requirements không được phát hiện sẽ đi thẳng vào Impact Matrix và PRD.

Đầu ra cho các team gồm PRD, Decision Brief và Story List. Chuẩn chung về cách chia story, mã, tiêu chí chấp nhận và điều kiện sẵn sàng ở README mục 6 và trong `engine/standards/`.

## 2. Cài đặt

### 2.1 Công cụ AI

PO dùng được nhiều công cụ AI, vì quy trình nằm trong `engine/` và `AGENTS.md`. Với Claude Code, bản terminal, ứng dụng desktop hoặc extension cho IDE đều dùng được; các lệnh như `/po`, `/new-intent` có sẵn trong `.claude/commands/`. Với công cụ khác, yêu cầu AI đọc `AGENTS.md`, sau đó đọc `engine/commands/<lệnh>.md` hoặc `engine/stages/<stage>.md` và làm theo.

### 2.2 Mở đúng thư mục gốc

Claude Code phải mở đúng thư mục gốc của repo, nơi có `AGENTS.md`, `engine/` và `.claude/`. Trong VS Code, chọn File, Open Folder, mở thư mục repo, sau đó mở một phiên Claude Code mới. Ở terminal, chuyển vào thư mục repo bằng `cd`, sau đó chạy `claude`.

Nếu Claude Code mở ở thư mục cha, hoặc repo chỉ được thêm như một thư mục phụ của phiên khác, Claude Code không nạp `.claude/settings.json` và `AGENTS.md` của repo. Khi đó hook không chạy và không có sổ ghi lời PO, nên lệnh duyệt và các lệnh quyết định đều từ chối và yêu cầu PO tự chạy trong terminal.

### 2.3 Git

Trên Windows, tải Git tại https://git-scm.com/download/win và giữ cài đặt mặc định. Trên Mac, Git có sẵn, hoặc chạy `xcode-select --install`.

Cấu hình một lần. Tên này được ghi vào cột Người quyết của mọi quyết định, nên dùng tên thật:

```bash
git config --global user.name "Họ Tên"
git config --global user.email "email@congty.vn"
```

### 2.4 Python và hook

Script `engine/scripts/po-tools.py` và hook `engine/scripts/po-hook.py` cần Python 3.9 trở lên. Không có Python thì quy trình vẫn chạy, nhưng AI phải kiểm thủ công thay cho bước kiểm bằng máy, và hook không ngăn được AI tự ghi duyệt.

Hook ghi mỗi câu PO gõ và mỗi lựa chọn PO bấm vào `.po/turns.jsonl` trên máy; file này không được commit. Lệnh duyệt và các lệnh quyết định dựa vào sổ này để xác nhận lời đó là của PO.

Kiểm tra môi trường sau khi cài đặt và mỗi khi thấy bất thường:

```bash
python3 engine/scripts/po-tools.py doctor
```

Lệnh kiểm tên git, Python, thư mục đang mở, hook ghi lượt PO đã chạy chưa, file chưa commit, nguồn knowledge base quá hạn đối chiếu, knowledge base của sản phẩm, mã tính năng trùng, và tên sản phẩm lọt vào phần quy trình dùng chung. Mỗi dòng không đạt có gợi ý cách sửa. Dòng "Hook ghi lượt PO" chuyển sang Đạt sau khi PO gõ câu đầu tiên trong một phiên mở đúng thư mục gốc.

### 2.5 Chụp màn hình cho User Guide

`.mcp.json` cấu hình sẵn Playwright để chụp màn hình. Lần đầu mở repo, Claude Code hỏi có cho phép MCP server này không; chọn đồng ý. Không dùng Playwright thì gõ `skip-screenshot` khi viết User Guide.

## 3. Cấu trúc thư mục

```
po-workflow/
├── AGENTS.md                  quy tắc cho mọi công cụ AI
├── CLAUDE.md                  một dòng, nạp AGENTS.md cho Claude Code
├── README.md                  phương pháp, chuẩn bàn giao, mức độ sẵn sàng áp dụng
├── USER-GUIDE.md              file này
├── DOMAIN-SETUP.md            đưa một sản phẩm mới vào quy trình
├── GLOSSARY.md                thuật ngữ, tên stage, họ mã
├── CHANGELOG.md · VERSION     phiên bản quy trình và cách nâng cấp
├── engine/                    quy trình dùng chung cho mọi sản phẩm
│   ├── stages/                mỗi stage một file
│   ├── commands/              lệnh: po, new-intent, po-status, po-review, po-replay, po-stories, po-evaluate, change-request, generate-user-guide, new-domain
│   ├── protocol/              quy định chung: stage, gate, review, câu hỏi, profile
│   ├── templates/             mẫu artifact, mẫu domain, mẫu yêu cầu
│   ├── verification/          checklist của từng stage và từng lệnh
│   ├── agents/ai-reviewer.md  reviewer độc lập
│   ├── standards/             quy ước mã, quy ước đặt tên, quy tắc bàn giao, sơ đồ, chuẩn knowledge base, ADR
│   ├── knowledge/             kiến thức vai PO lấy từ AWS
│   ├── scripts/               po-tools.py: kiểm tra, truy vết, duyệt, quyết định, Story List, chỉ mục; po-hook.py: hook của Claude Code
│   └── tests/                 dữ liệu kiểm thử của script, dành cho người sửa quy trình
├── domain/                    knowledge base của sản phẩm: domain.md, các file KB, corner checklist
├── memory/
│   ├── team.md                bài học dùng chung, đi theo quy trình
│   └── project.md             bài học của sản phẩm đang cài
├── .claude/                   cấu hình riêng cho Claude Code: lối tắt cho lệnh, quyền, hook
├── .po/                       sổ lượt người trên máy này, không commit
└── intents/
    ├── INDEX.md               chỉ mục PRD đã duyệt cho Dev
    └── 261009-ten-intent/
        ├── intent.md          bối cảnh, mã tính năng, người phụ trách, Figma, Jira
        ├── state.md           đang ở stage nào, việc kế tiếp
        ├── decisions.md       quyết định nguyên văn, change request, sổ rủi ro
        ├── memory.md          quan sát của AI, PO đọc tại gate
        ├── inputs/            tài liệu đầu vào
        ├── ideation/  inception/
        ├── stories/           Story List, bảng ghép story với issue Jira
        └── reviews/  verification/  archive/  design/  user-guide/  evaluation/
```

`state.md` cho biết intent đang ở đâu và ai làm gì tiếp. `decisions.md` là bộ nhớ của intent; AI tra file này để không hỏi lại câu đã có đáp án. Không xoá hai file này. `archive/` chứa bản đã duyệt và không được sửa.

## 4. Chạy một intent tới PRD

### 4.1 Tạo intent

```
/new-intent Báo cáo giai đoạn 1
```

AI tạo thư mục `intents/<YYMMDD>-bao-cao-giai-doan-1/`, cấp mã tính năng, đọc nhanh knowledge base để ước lượng vùng bị chạm, sau đó hỏi một câu để xác nhận profile, ví dụ "Profile M: 7 stage, 6 gate. Đồng ý, đổi profile hoặc đổi depth?".

Đặt tài liệu đầu vào như mô tả yêu cầu, email, biên bản họp, ảnh vào `inputs/`. Khi chưa có mô tả, AI chép mẫu `inputs/request.md` gồm hiện trạng, điều muốn thay đổi, trong và ngoài phạm vi, điều không được thay đổi, mốc thời gian, câu hỏi mở; PO gửi mẫu cho người yêu cầu điền. Mục "Điều không được thay đổi" có tác động lớn nhất tới phân tích ảnh hưởng. Ghi link Figma, Jira và tên các PIC vào `intent.md`.

### 4.2 Gọi /po

```
/po 261009-bao-cao-giai-doan-1
```

Mỗi lần gọi, AI đọc `state.md` và chạy stage kế tiếp hoặc tiếp tục stage đang làm dở. Khi làm nhiều intent song song, luôn ghi tên intent trong lệnh. Không có lệnh riêng cho từng stage; muốn chạy một stage cụ thể thì yêu cầu "chạy 2.3".

Mỗi stage đi qua bảy bước: AI đọc thông tin nền, hỏi, tóm tắt để PO xác nhận, viết artifact, tự kiểm tra, ghi quan sát, trình gate. Cách trả lời ở mục 5.

### 4.3 Ideation, profile M và L

Ở 1.1 và 1.4, AI hỏi về vấn đề, cách người dùng xử lý hiện tại, mục tiêu đo được, các bên liên quan, sau đó hỏi về phạm vi In, Out, Potential và cách chia nhu cầu thành Unit. Profile M duyệt hai artifact này chung một gate.

Stage 1.2 chỉ chạy khi PO muốn so sánh với sản phẩm khác; danh sách sản phẩm so sánh mặc định ghi trong `domain/domain.md`.

Stage 1.7 chỉ có ở profile L. AI tóm tắt phase thành Initiative Brief một trang; gate này có thêm lựa chọn Reject Initiative để dừng intent.

### 4.4 Inception

Ở 2.3 Requirements Analysis, AI tra knowledge base trước, chỉ hỏi phần còn thiếu, sau đó viết yêu cầu có mã `FR1`, `FR1.1`, `NFR1`. Yêu cầu trùng tính năng đã có được nêu ngay, kèm mã trong knowledge base. Profile S bắt đầu từ stage này.

Ở 2.31 Impact Analysis, AI trình Related Features Map gồm module, màn, bảng, endpoint, thông báo, rule liên quan. PO rà soát và bổ sung phần thiếu; nhận ra phần thiếu trong một bản nháp nhanh hơn tự liệt kê từ đầu. Sau đó AI dựng Impact Matrix 12 vùng và chuyển mọi xung đột cho PO quyết định.

Stage 2.32 Solution Options chỉ chạy khi có nhiều hướng giải. PO đã có định hướng thì AI nhận xét và đề xuất thêm; chưa có thì AI dựng hai tới ba phương án cùng phương án giữ nguyên, chấm theo bảy tiêu chí có trọng số và đưa khuyến nghị. Duyệt gate nghĩa là chọn phương án.

Ở 2.4 User Stories, AI chia story theo `engine/standards/story-splitting.md`: xây dựng bản đồ story theo vai và bước trong hành trình, xét dấu hiệu story quá lớn, đề xuất cách tách. Mỗi US gắn một Unit, mỗi yêu cầu chức năng có US phủ. Mỗi Unit sẽ là một story trên Jira, nên AI đề xuất tách hoặc gộp Unit khi một Unit không độc lập hoặc rõ ràng lớn hơn một sprint. Mỗi US có một thẻ chín mục: vai và mục tiêu, bối cảnh, luồng chính, nhánh đáng kể, rule đã biết, dữ liệu và vùng bị tác động, ngoài phạm vi, phụ thuộc, điểm chưa rõ. Thẻ chưa có tiêu chí chấp nhận. PO duyệt cả danh sách lẫn từng thẻ.

Ở 2.42 PRD Generation, AI tra Impact Matrix, data model, đặc tả API, knowledge base, sau đó lập bảng Field Intake về field, rule, validate cho từng màn để PO điền và duyệt. Tiếp theo, AI viết PRD theo template chuẩn `engine/templates/prd.md`:

- mục 1 tới 5 tóm tắt từ artifact đã duyệt, gồm tiêu chí thành công đo được và giải pháp tổng thể;
- mục 6 viết từng US với mười mục con: dòng Ưu tiên, business rule theo BABOK 10.9, tiêu chí chấp nhận theo Given/When/Then có ghi business rule mà nó kiểm, trường hợp ngoại lệ lấy từ Impact Matrix;
- mục 7 tới 10 gom yêu cầu phi chức năng, yêu cầu chuyển đổi, giả định và câu hỏi mở.

Đối tượng đổi trạng thái có bảng chuyển trạng thái và sơ đồ trạng thái ở mục 4; script kiểm hai bên khớp nhau và kiểm cú pháp mọi sơ đồ Mermaid, để sơ đồ hiển thị được trên GitHub. Với điểm phụ thuộc thiết kế hoặc kỹ thuật chưa rõ, AI ghi đề xuất kèm câu hỏi gắn tên PIC để các team trả lời ở 2.43. Trước gate, AI chạy kiểm truy vết FR, US, BR, AC và sửa phần thiếu.

Stage 2.43 Design Alignment chạy với profile M và L, theo bốn bước:

1. Sau khi PRD được duyệt, AI tạo ba file thiết kế từ template và chỉ điền phần đầu file. PO gửi ba PIC đường dẫn PRD và file của họ, kèm hạn; cách viết của PIC ở mục 8.
2. Khi các team viết xong, PO gọi lại `/po`. AI đối chiếu ba file với PRD, báo phần còn thiếu, viết Decision Brief chỉ gồm điểm cần quyết định, sau đó chạy `po-tools.py sign-start` để ghi lại bản gửi ký.
3. Các bên họp trên Decision Brief. Quyết định làm đổi yêu cầu được xử lý qua change request. Tech PIC đã ghi cỡ của từng Unit ở `tech-design.md` mục 7; quyết định tách, gộp Unit hoặc chuyển US giữa các Unit cũng sửa PRD mục 5 qua change request trước khi ký.
4. Gate duyệt khi cả ba PIC ghi Đồng ý hoặc Có ý kiến ở bảng Ký, đúng tên ở `intent.md` và đúng bản đã gửi. PIC quá hạn chưa ký thì PO được chọn Accept as-is kèm lý do. Story List chỉ sinh sau khi gate này được duyệt.

## 5. Trả lời AI và duyệt

### 5.1 Questions file

Mỗi stage có một file câu hỏi, ví dụ `requirements-analysis-questions.md`. Mỗi câu gồm:

- nhãn người trả lời: `[PO]`, `[Người yêu cầu]`, `[Design]`, `[Tech]`, `[QA]`, hoặc vai khác ghi trong `domain.md`;
- tối đa bốn lựa chọn và `X. Khác`; lựa chọn AI đề xuất có ghi nguồn;
- dòng `Chặn: có` khi AI không viết tiếp được nếu thiếu đáp án;
- dòng `[Answer]:` để ghi câu trả lời.

Lần đầu, AI hỏi PO muốn trả lời theo cách nào và dùng cách đó cho cả intent:

| Cách | PO làm gì |
|---|---|
| Guide me | AI hỏi từng câu trong cửa sổ hội thoại, PO chọn, AI ghi vào file |
| Edit file | PO mở file, điền sau `[Answer]:`, báo đã điền xong |
| Chat | PO viết tự nhiên trong một lượt, AI tách ra từng câu |

AI coi người trả lời là người có đủ thông tin, nên đặt đủ câu hỏi để lấy thông tin đó. Đầu file câu hỏi có bảng Độ phủ: mỗi chủ đề của stage hoặc đã có câu trả lời trong đầu vào, hoặc có câu hỏi. Số câu tăng theo depth và theo mức mơ hồ của đầu vào; mỗi câu có lựa chọn "Chưa xác định" để người trả lời không phải chọn bừa.

AI ghi câu trả lời nguyên văn và phân tích lại toàn bộ trước khi viết artifact. Câu còn trống, câu trả lời mơ hồ như "tuỳ", "chắc là", "như cũ", hoặc hai câu mâu thuẫn nhau thì AI hỏi tiếp; AI không viết artifact khi còn câu chưa trả lời. Các câu cùng nhãn đứng cạnh nhau, để PO chuyển cả nhóm cho đúng người hoặc họp theo nhóm, sau đó điền theo cách Edit file.

PO có thể giao cho AI chọn theo đề xuất ở một câu hỏi. AI ghi `[uỷ quyền]` kèm nguyên văn và báo đã chọn gì. Uỷ quyền chỉ áp cho câu hỏi của stage đang chạy, không áp cho bước xác nhận tóm tắt, xác nhận giả định hoặc gate.

### 5.2 Tóm tắt và giả định

Trước khi viết artifact, AI tóm tắt mọi câu trả lời và hỏi Looks correct hoặc Request changes. Ở 1.1 và 2.3, AI liệt kê thêm các giả định để PO chấp nhận hoặc chuyển thành câu hỏi. Đây là bước phát hiện hiểu nhầm với chi phí thấp nhất.

### 5.3 Gate

AI trình thông điệp hoàn thành gồm tiêu đề, bảng artifact tóm tắt bằng số, kết quả review và finding còn mở, đường dẫn để mở, stage kế tiếp và việc của từng người. Trước khi hỏi duyệt, AI hỏi PO có bài học nào cần giữ. PO chọn một trong năm lựa chọn:

| Lựa chọn | Kết quả |
|---|---|
| Approve | Đi tiếp. Script đặt phiên bản, chụp bản duyệt vào `archive/`, ghi quyết định |
| Request Changes | AI sửa theo nội dung PO nêu và trình lại |
| Accept as-is | Từ lần Request Changes thứ ba, nhận bản hiện tại kèm điều kiện và lý do |
| Add stage | Chạy thêm một stage ngoài profile, ví dụ 2.32 |
| Reject Initiative | Chỉ ở 1.7, dừng intent |

AI hiểu lời duyệt viết bằng câu tự nhiên. Câu "Ok nhưng đổi tên trường X" là duyệt kèm chỉ thị: AI sửa, báo một dòng, hỏi lại "Duyệt bản đã sửa?", và chỉ ghi duyệt sau khi PO trả lời. Câu trả lời không rõ thì AI hỏi lại và không coi đó là lời duyệt.

AI không tự duyệt được. Lệnh duyệt chỉ ghi khi lời duyệt có nguyên văn trong một lượt của PO sau lần sửa artifact cuối. Khi script từ chối, AI nêu lý do và hỏi lại PO. PO được hỏi thêm trong bốn trường hợp:

| Trường hợp | PO làm gì |
|---|---|
| Bước kiểm bằng máy còn cảnh báo thông thường | Yêu cầu sửa, hoặc trả lời chấp nhận kèm lý do |
| Còn câu chặn chưa trả lời, GAP hoặc ORPHAN của truy vết, hoặc mã có ở bản duyệt trước mà bản này không còn | AI liệt kê từng mục kèm mã. PO yêu cầu sửa, hoặc quyết định riêng từng mục bằng một câu có nêu đúng mã, ví dụ "Hoãn Q3 sang đợt sau, FR4 làm ở intent khác" |
| Artifact đổi sau lần AI Reviewer xem | Chạy review lại, hoặc xác nhận duyệt mà không review lại |
| Dùng công cụ AI không có hook | Tự chạy lệnh duyệt trong terminal theo lệnh AI đưa |

Bản nháp mang phiên bản 0.x. Lần duyệt đầu là 1.0; mỗi lần duyệt lại sau change request tăng số phụ.

### 5.4 Quyết định ngoài gate

Năm quyết định dưới đây đổi trạng thái của intent, nên chỉ được ghi khi PO nói rõ. AI hỏi, chờ PO trả lời, sau đó chạy lệnh với lời PO; lời đó phải nằm trong ba lượt gần nhất của PO. Hook không cho AI sửa tay các dòng tương ứng.

| Quyết định | PO nói, ví dụ | Lệnh AI chạy |
|---|---|---|
| Bỏ qua một stage | "Bỏ qua impact analysis vì chỉ đổi nhãn" | `po-tools.py skip` |
| Đổi profile | "Nâng lên profile L vì có chuyển đổi dữ liệu" | `po-tools.py profile` |
| Bật, tắt AI Reviewer, bước tóm tắt, câu hỏi bài học | "Tắt reviewer cho intent này" | `po-tools.py switch` |
| Nhận, hoãn, bác hoặc đóng một change request | "Nhận CR2, mở lại PRD" | `po-tools.py cr` |
| Mở lại gate đã ghi nhầm Approve | "Ghi nhầm duyệt 1.4, mở lại gate" | `po-tools.py reopen` |

Stage 1.2 và 2.32 là stage có điều kiện. Khi điều kiện không xảy ra, AI tự ghi bỏ qua kèm lý do và báo một dòng; PO muốn chạy thì chọn Add stage.

### 5.5 Bài học

Tại gate, AI nêu một số quan sát và hỏi PO điều gì cần giữ cho lần sau. Dòng PO chọn được ghi vào `memory/project.md`. AI hỏi thêm một câu: bài học có đúng cho mọi sản phẩm không; nếu có, AI chuyển bài học sang `memory/team.md`, file đi theo engine. Bài học có hiệu lực từ stage kế tiếp và không áp ngược cho stage đã duyệt.

## 6. Thay đổi yêu cầu sau khi duyệt

Thay đổi nhỏ trong stage đang mở chỉ cần sửa và trình lại gate. Mọi thay đổi chạm stage đã duyệt đi qua `/change-request`; lệnh cũng tự kích hoạt khi PO nói "đổi yêu cầu" hoặc "bổ sung". Thứ tự xử lý:

1. AI ghi `CR<n>` vào bảng Change requests của `decisions.md` với trạng thái Chờ quyết.
2. AI đánh giá: mã bị chạm, story đã lên Jira hay chưa, mục tiêu bị ảnh hưởng, công sức, độ khẩn, rủi ro mới. AI đề xuất stage phải quay lại.
3. PO quyết định Nhận, Hoãn hoặc Bác. AI ghi quyết định bằng `po-tools.py cr`; với Nhận, lệnh mở lại các stage đã duyệt bị chạm.
4. AI chụp artifact bị chạm vào `archive/` với nhãn pre-CR, chạy xuôi từ stage đó và chỉ sửa phần bị chạm.
5. Mỗi artifact sửa xong được trình lại gate. Khi mọi stage mở lại đã được duyệt lại, AI đóng CR bằng `po-tools.py cr` với lời PO.

Khi duyệt lại, script so mã với bản đã duyệt trước. Mã nào bị bỏ phải được giữ dòng kèm chữ "bỏ", "chuyển sang" hoặc "gộp vào"; mã biến mất không có ghi chú thì lệnh duyệt từ chối. Khi Decision Brief đổi, các PIC ký lại. Khi PRD đổi, phiên bản tăng, các team xem lại file thiết kế theo bản mới, và Story List được sinh lại sau khi duyệt.

## 7. Bàn giao sau khi duyệt

### 7.1 Sinh Story List

```
/po-stories <intent>
```

AI trình bản xem trước: mỗi Unit ở PRD mục 5 một story, mã như `APP-F012-U1`, kèm tên Unit, ưu tiên, các US, Epic và kết quả điều kiện sẵn sàng. Description của story gồm khối của từng US trong Unit. Bảng Units không khớp các khối US, như US chưa thuộc Unit nào hoặc US nằm trong hai Unit, làm lệnh dừng và báo lý do. Khi PO đồng ý, AI ghi `intents/<intent>/stories/story-list-prd-v<phiên bản>.csv`. AI chỉ ghi file khi PRD đã duyệt; với profile M, L, chỉ ghi sau gate 2.43. Mã màn của từng story lấy từ `ux-design.md`. File có 12 cột theo mẫu import CSV của Jira, thêm cột Labels khi Unit có từ hai US. Cột Priority lấy từ cột Ưu tiên của bảng Units, hoặc mức cao nhất trong dòng Ưu tiên của các US: Must thành Highest, Should thành High, Could thành Medium. PO import lên Jira bằng chức năng import CSV.

Phiên Claude Code đã nối Jira MCP thì AI đẩy story thẳng lên Jira, không cần import:

1. AI chạy `po-tools.py jira-sync intents/<intent>` và trình bảng kế hoạch: story nào tạo, cập nhật, giữ nguyên, gắn nhãn `removed-from-prd` hoặc `merged-into-story`. Story chưa đạt điều kiện sẵn sàng vẫn được đẩy, mang nhãn `not-ready`. Issue không bao giờ bị xoá; Unit được phụ thuộc, theo cột Phụ thuộc của bảng Units hoặc mục Tiền điều kiện của US, trở thành liên kết "is blocked by". Intent từng đẩy story theo từng US: issue của US đầu tiên trong Unit được chuyển thành story của Unit, issue của các US còn lại mang nhãn `merged-into-story`.
2. Story đã đẩy trước đó mà bị sửa tay trên Jira thì AI báo; PO chọn giữ bản trên Jira hoặc ghi đè.
3. PO đồng ý, ví dụ "đồng ý đẩy lên Jira". AI tạo, cập nhật issue qua MCP, sau đó ghi kết quả bằng `jira-sync --record`. Script chỉ ghi khi lời đồng ý có trong 3 lượt gần nhất của PO.
4. PO commit `stories/jira-map.json` và `decisions.md`.

Khi PRD đổi qua change request, chạy lại `/po-stories`; chỉ story đổi được cập nhật, kèm comment ghi bản PRD mới.

Trước lần sinh Story List đầu tiên, kiểm hai điểm:

- `domain/domain.md` có `jira_project_key` và `jira_project_name` ở frontmatter. Hai khoá này được khai báo khi dựng knowledge base của sản phẩm, theo DOMAIN-SETUP.md mục 5.
- Dòng Jira Epic trong `intent.md` có mã Epic. Intent có nhiều Epic thì ghi thêm `U2: <mã Epic>` để story của Unit đó gắn đúng Epic.

### 7.2 Gắn tag và cập nhật chỉ mục

Mỗi lần duyệt PRD hoặc Decision Brief, script in tên tag gợi ý: `<intent>/prd-v1.0` hoặc `<intent>/decision-brief-v1.0`. PO commit artifact vừa duyệt, gắn tag và đẩy tag lên. File CSV được commit cùng PRD với profile S, cùng Decision Brief với profile M, L. Ví dụ với PRD:

```bash
git tag <intent>/prd-v1.0
git push origin <intent>/prd-v1.0
python3 engine/scripts/po-tools.py index --write
```

Lệnh cuối cập nhật `intents/INDEX.md` với mã tính năng, bản PRD đã duyệt, ngày duyệt, service bị chạm, tag, nơi đăng bản đọc nếu có, và số story đạt điều kiện sẵn sàng. Commit file này.

### 7.3 Trước khi bàn giao cho Dev

```bash
python3 engine/scripts/po-tools.py dor intents/<intent>
```

Script in story nào đạt, story nào chưa và lý do kèm mã US, theo bảy điều kiện ở README mục 6.7; story đạt khi mọi US của Unit đạt. Kết quả cũng ghi ở cột Comment của file CSV. Chỉ bàn giao cho Dev các story đạt. Độ phủ test case do QA theo dõi trên Jira.

### 7.4 Trước khi mở quyền repo cho các team

Các PIC cần quyền ghi repo của PO để viết file thiết kế và ký Decision Brief, nên họ cũng đọc được `decisions.md`, `memory.md` và questions file. Rà thông tin nhạy cảm như tài khoản môi trường thử nghiệm trước khi mở quyền. Workflow gitleaks trong `.github/` quét mỗi lần đẩy lên.

## 8. Dành cho Design PIC, Tech PIC, QA PIC

PIC làm việc ở hai nơi: file thiết kế của mình trên repo của PO sau khi PRD được duyệt, và story trên Jira sau gate 2.43. PIC có thể sửa repo bằng Claude Code, công cụ AI khác hoặc giao diện web của GitHub, và không cần chạy quy trình của PO.

### 8.1 Viết file thiết kế và ký Decision Brief, stage 2.43

PIC đọc PRD đã duyệt một lần, viết thiết kế của mình vào file riêng, sau đó cùng thống nhất trên Decision Brief.

1. Pull repo, đọc `intents/<intent>/inception/prd/prd.md`. Mở file của mình: Design PIC mở `inception/ux-design/ux-design.md`, Tech PIC mở `inception/tech-design/tech-design.md`, QA PIC mở `inception/test-design/test-design.md`. Template ở `engine/templates/`.
2. Chỉ sửa file của mình. Mọi phần trỏ về mã trong PRD: `US<n>`, `AC<n>.<m>`, `BR<n>.<m>`. Ghi `inputs: prd@<version>` đúng bản PRD đã đọc.
3. Viết phần việc của mình:
   - Design PIC đặt mã màn `SCR<n>` ở bảng Danh sách màn, mỗi màn ghi US mà nó phục vụ; Story List lấy mã màn từ bảng này.
   - Tech PIC viết cùng người phụ trách Backend và Frontend: service, ứng dụng hoặc repo bị tác động ghi đúng tên Dev sử dụng; hợp đồng API giữa hai phía; mỗi màn `SCR` của ux-design có route và component ở phần Frontend. Mục 7 có một dòng cho mỗi Unit ở PRD mục 5: phần việc Backend, Frontend, độ lớn, kết luận Unit có vừa một sprint, và đề xuất tách, gộp hoặc chuyển US khi Unit không vừa. Mỗi Unit là một story trên Jira.
   - QA PIC ghi cách kiểm cho từng AC.
4. Ghi ý kiến ở mục Ý kiến về PRD trong file của mình: Đồng ý, Đề xuất sửa hoặc Phản đối, kèm mã và lý do. Không sửa PRD. Câu hỏi cho PO hoặc team khác ghi ở mục Rủi ro và câu hỏi cần trả lời.
5. Commit với message `design(<intent>): ux`, `tech` hoặc `test`, sau đó push.
6. Sau khi nhận Decision Brief, dự họp và ký ở bảng Ký của `inception/decision-brief/decision-brief.md`: ghi tên đúng như `intent.md`; cột Bản là version ở đầu file Decision Brief đã đọc; trạng thái là Chưa xem, Có ý kiến, Đồng ý hoặc Yêu cầu sửa. Chọn Yêu cầu sửa thì ghi rõ nội dung cần sửa. Decision Brief đổi sau khi gửi ký thì PO gửi bản mới và PIC ký lại.

PIC không mở được repo thì gửi nội dung cho PO. PO dán nguyên văn, mở đầu bằng "(ghi theo <tên>, <ngày>)", và lưu tin nhắn xác nhận vào `decisions.md`.

### 8.2 Làm việc trên story Jira

Sau gate 2.43, hoặc sau gate 2.42 với profile S, PO đẩy story lên Jira qua MCP hoặc import Story List. Mỗi Unit ở PRD mục 5 là một story; phần Description lấy từ PRD, gồm khối của từng US với tiêu chí chấp nhận và business rule có mã đầy đủ.

| Người | Việc trên story |
|---|---|
| Design PIC | Gắn mã màn `SCR` và link thiết kế; frame Figma đặt tên bắt đầu bằng mã màn đầy đủ |
| Tech PIC | Chia story thành sub-task Backend, Frontend, ước lượng story point, ghi nhánh code |
| QA PIC | Viết test case mã `TC`, mỗi test case ghi mã AC mà nó kiểm và bản PRD đã dùng khi chạy; test tự động gắn tag mã AC |

Quy tắc:

1. Không sửa phần Description. Nội dung nghiệp vụ chỉ đổi khi PRD đổi qua change request; khi đó PO cập nhật story, kèm comment ghi bản PRD mới. Description bị sửa trên Jira sẽ được báo cho PO ở lần đẩy sau.
2. Câu hỏi nghiệp vụ ghi bằng comment trên story, gắn người phải trả lời. Câu trả lời làm đổi PRD thì PO đi qua change request.
3. Story chưa đạt điều kiện sẵn sàng mang nhãn `not-ready`, comment ghi lý do. Chờ PO xử lý các lý do đó trước khi nhận việc; nhãn được bỏ khi story đạt.
4. Story mang nhãn `removed-from-prd` không còn trong PRD. Story mang nhãn `merged-into-story` đã được gộp vào story của Unit ghi ở comment. Không làm tiếp hai loại story này; đóng hoặc huỷ theo quy trình của team.

### 8.3 Mã và cách trỏ

Từ story trên Jira trở đi, mọi team chỉ dùng mã đầy đủ. Design cấp `SCR-<tính năng>-<NN>`. QA cấp `TC-<tính năng>-<NNN>`; mỗi test case ghi tiêu chí chấp nhận `AC-<tính năng>-<NN>.<n>` mà nó kiểm. Mã đã cấp không đổi và không dùng lại. Bảng mã ở `engine/standards/id-conventions.md`; cách đặt tên frame Figma, nhánh, commit, tag test, đặc tả API ở `engine/standards/naming-conventions.md`; quy tắc bàn giao ở `engine/standards/handoff-rules.md`.

## 9. Dành cho Dev

Bản chính thức của PRD là file trong repo theo tag của bản đã duyệt. Việc được giao qua story trên Jira. Agent AI của Dev đọc PRD theo tag, nên luôn lấy đúng bản đã duyệt.

1. Đọc `intents/INDEX.md` để biết tính năng nào đã có PRD duyệt, tag nào, service nào bị chạm, bao nhiêu story đạt điều kiện sẵn sàng.
2. Lấy đúng bản theo tag, bằng `git show <tag>:<đường dẫn>` hoặc qua GitHub MCP server của công cụ đang dùng.
3. Đặt tên nhánh `<loại>/<key Jira>-<mô tả>`, ví dụ `feat/APP-123-lam-lai-bai-kiem-tra`. Key Jira viết hoa để Jira tự liên kết nhánh với story.
4. Viết commit theo Conventional Commits và thêm trailer ở cuối thông điệp:

```
feat(quiz): cho phép làm lại bài kiểm tra

Refs: APP-123
Feature: APP-F012
Story: US-APP-F012-01
Implements: AC-APP-F012-01.1, BR-APP-F012-01.2
```

5. Code kiểm một business rule thì ghi mã BR đầy đủ ở chú thích tại chỗ kiểm, để khi rule đổi, `git grep` tìm ra đúng chỗ phải sửa. Chi tiết ở `engine/standards/naming-conventions.md`.

Unit trong PRD là nhóm user story độc lập, có giá trị và mức ưu tiên riêng, được Tech PIC xác nhận vừa một sprint; mỗi Unit là một story trên Jira. Dev chia story thành sub-task theo kiến trúc. Thiết kế kỹ thuật nằm ở `tech-design.md` và tài liệu riêng của Dev; PRD không chứa thiết kế kỹ thuật.

## 10. Lệnh

| Lệnh | Dùng khi |
|---|---|
| `/new-intent <tên>` | Tạo intent, cấp mã tính năng, chọn profile |
| `/po <intent>` | Chạy stage kế tiếp hoặc tiếp tục stage đang làm dở |
| `/po-status [intent]` | Xem trạng thái mọi intent, phát hiện lệch giữa `state.md` và file |
| `/po-review <file>` | Review độc lập bằng AI Reviewer; thêm `--shadow` cho tài liệu người khác viết |
| `/po-replay <intent>` | Tóm lược diễn biến của intent theo dòng thời gian: quyết định, review, việc còn chặn. Dùng khi chuyển intent cho PO khác |
| `/po-stories <intent>` | Đẩy story lên Jira qua MCP hoặc sinh Story List để import, từ PRD đã duyệt; profile M, L chạy sau gate 2.43 |
| `/change-request <intent>` | Đổi hoặc bổ sung yêu cầu sau khi đã duyệt; PO quyết định Nhận, Hoãn hoặc Bác trước khi sửa |
| `/po-evaluate <intent>` | Đánh giá giải pháp sau phát hành theo tiêu chí thành công của PRD |
| `/generate-user-guide <intent>` | Viết User Guide sau khi Dev hoàn thành |
| `/new-domain <sản phẩm>` | Dựng khung knowledge base trong repo của sản phẩm mới |

Lệnh của script, chạy từ thư mục gốc. Phần lớn lệnh do AI chạy; PO chạy trực tiếp khi dùng công cụ không có hook.

| Lệnh | Việc |
|---|---|
| `po-tools.py doctor` | Kiểm môi trường và knowledge base của sản phẩm |
| `po-tools.py status` | Trạng thái mọi intent, artifact bị sửa ngoài change request, mã tính năng trùng, nguồn quá hạn |
| `po-tools.py next <intent>` | Stage cần làm tiếp và số câu hỏi còn trống |
| `po-tools.py check <intent> <stage>` | Kiểm bằng máy trước gate |
| `po-tools.py trace <intent>` | Truy vết FR, US, BR, AC |
| `po-tools.py review-start <intent> <stage>` | Ghi dấu artifact trước khi gọi AI Reviewer |
| `po-tools.py approve <intent> <stage> --words "<lời PO>"` | Ghi kết quả duyệt. Câu chặn, GAP, ORPHAN, mã biến mất phải được sửa, hoặc PO quyết định từng mục qua `--accept-items` và `--item-words` |
| `po-tools.py skip`, `profile`, `switch`, `cr`, `reopen` | Ghi quyết định của PO ngoài gate, theo mục 5.4 |
| `po-tools.py sign-start <intent>` | Ghi dấu bản Decision Brief gửi PIC ký |
| `po-tools.py replay <intent>` | Tóm lược diễn biến của intent cho người tiếp nhận |
| `po-tools.py stories <intent> [--write]` | Xem trước hoặc ghi Story List cho Jira, mỗi Unit một story |
| `po-tools.py jira-sync <intent>` | Lập kế hoạch đẩy story lên Jira qua MCP; `--remote` đối chiếu bản trên Jira, `--record` ghi kết quả |
| `po-tools.py dor <intent>` | Kiểm điều kiện sẵn sàng |
| `po-tools.py index --write` | Cập nhật `intents/INDEX.md` |
| `po-tools.py migrate <intent> [--feature <mã>] [--write]` | Chuyển intent tạo từ bản quy trình cũ |
| `po-tools.py engine-check` | Liệt kê file của quy trình đã bị sửa tay, trước khi nâng cấp |
| `po-tools.py selftest` | Chạy dữ liệu kiểm thử của script sau khi nâng cấp hoặc sửa quy trình |

## 11. Knowledge base của sản phẩm

Mọi dữ kiện riêng của sản phẩm nằm trong `domain/`. AI đọc `domain/domain.md` ở đầu mỗi phiên. File này có sáu mục:

| Mục | Nội dung |
|---|---|
| 1. Sản phẩm và phạm vi | Sản phẩm là gì, phần nào ngoài phạm vi |
| 2. Nguồn sống và bản chốt | Nguồn nào còn cập nhật, đọc ở đâu, đối chiếu lần cuối ngày nào |
| 3. Bản đồ KB | File KB nào trả lời câu gì, stage nào dùng |
| 4. Dữ kiện cho từng stage | Sản phẩm so sánh, thực thể dùng chung, nguồn field, đích User Guide |
| 5. Ví dụ dùng trong engine | Ví dụ thật của sản phẩm để AI hiểu đúng quy tắc |
| 6. Thành phần của domain pack | Danh sách file |

Cùng thư mục có các file KB theo `engine/standards/domain-kb.md`: mục lục, glossary, mô hình khái niệm, mỗi module một file, mô hình dữ liệu, phân quyền, tích hợp, sự kiện, số liệu phi chức năng, định hướng sản phẩm, và `corner-checklist.md` liệt kê corner case thường bị bỏ sót. Domain không chứa template; template của mọi artifact, kể cả PRD và User Guide, nằm trong `engine/templates/`. Kiến thức vai PO không phụ thuộc sản phẩm nằm ở `engine/knowledge/`.

Knowledge base có ba giới hạn:

- Knowledge base thường không phủ toàn hệ thống. Vùng chưa phủ được ghi trong bản đồ KB; trước khi kết luận một vùng không bị ảnh hưởng, AI đối chiếu với danh sách này.
- Rule do AI trích từ văn xuôi chưa được duyệt. PO xác nhận trước khi dùng làm ràng buộc trong PRD.
- Knowledge base là bản chụp. Yêu cầu chạm vùng nào thì AI đọc lại nguồn sống của vùng đó. Bản chốt không còn nguồn gốc thì AI hỏi PO thay vì suy đoán. `doctor` cảnh báo nguồn quá 30 ngày chưa đối chiếu.

Ký hiệu chung trong artifact:

| Ký hiệu | Nghĩa |
|---|---|
| `❓PO` | Chưa rõ, không dùng làm căn cứ |
| `[suy ra]` | AI suy luận; nguồn không nói trực tiếp |
| `[Q3]`, `[DEC5]`, `[KB-04 §3]` | Thẻ nguồn: câu trả lời, quyết định, đoạn knowledge base |
| Hidden | Tính năng có code nhưng đang ẩn, vẫn phải xét khi phân tích ảnh hưởng |

Để đưa một sản phẩm khác vào quy trình, đọc [DOMAIN-SETUP.md](DOMAIN-SETUP.md), sau đó chạy `/new-domain` trong repo mới. Phần quy trình dùng chung giữ nguyên; chỉ knowledge base trong `domain/` và `memory/project.md` thay đổi.

## 12. Xử lý tình huống

| Tình huống | Cách xử lý |
|---|---|
| AI chọn nhầm intent | Báo intent đúng; AI chuyển ngay |
| AI hỏi lại câu đã trả lời | Kiểm `decisions.md` và questions file; câu trả lời có thể chưa được ghi |
| Không biết intent đang ở đâu | Chạy `/po-status` |
| AI viết dài hoặc mở rộng phạm vi | Yêu cầu AI quay về phạm vi đã duyệt |
| Phiên làm việc dài, AI bắt đầu bỏ sót | Nén phiên, sau đó gọi lại `/po`. Trạng thái và câu trả lời đã ghi vào file thì không mất; thời điểm an toàn nhất để nén là ngay sau một gate |
| Xung đột git ở `state.md`, `decisions.md` hoặc `memory/` | Với `decisions.md`, giữ dòng của cả hai bên và đánh lại số DEC trùng; với `state.md`, lấy trạng thái mới hơn, sau đó chạy `/po-status`. Gỡ xung đột trong trình soạn thảo, vì hook chặn AI sửa dòng DEC cũ |
| Lệnh duyệt hoặc lệnh quyết định từ chối vì không thấy lời PO | Kiểm Claude Code có mở đúng thư mục gốc của repo không, theo mục 2.2. Chạy `po-tools.py doctor` và xem dòng Hook ghi lượt PO. Không mở lại được thì tự chạy lệnh trong terminal |
| Hook chặn AI sửa một file | Đọc lý do AI báo lại. Artifact đã duyệt thì chạy `/change-request`; quyết định đổi thì thêm dòng DEC mới; bỏ qua stage, đổi profile, tắt reviewer thì trả lời câu hỏi của AI để AI chạy lệnh tương ứng |
| Vô tình sửa tay artifact đã duyệt | `/po-status` báo lệch. Thay đổi có chủ đích thì chạy `/change-request`; nếu không, lấy lại bản trong `archive/` |
| Chọn nhầm tại gate | Báo ngay. Ghi nhầm Request Changes thì AI trình lại gate; ghi nhầm Approve thì AI chạy `po-tools.py reopen` với lời PO |
| Reviewer báo NOT-READY nhưng PO chấp nhận | Nêu finding nào được chấp nhận; AI ghi Accepted risk vào `decisions.md` |
| PIC chưa viết file thiết kế hoặc chưa ký Decision Brief | Chờ tới hạn. Quá hạn mà thiếu file: PO quyết định viết Decision Brief với phần đã có, ghi DEC. Quá hạn mà thiếu chữ ký: PO chọn Accept as-is tại gate, lý do ghi DEC |
| Chữ ký của PIC không được tính | Xem lý do trong kết quả `po-tools.py check`: sai tên so với `intent.md`, cột Bản khác bản đã gửi, hoặc Decision Brief đã đổi sau khi gửi |
| Story không đạt điều kiện sẵn sàng | Chạy `po-tools.py dor`, xử lý theo lý do script in ra |
| Không chụp được màn hình | Gõ `skip-screenshot`; AI để trống vị trí ảnh và liệt kê ảnh còn thiếu |

Các hành vi sau là đúng thiết kế:

| Hiện tượng | Nguyên nhân |
|---|---|
| AI dừng, không sang stage sau | Đang chờ PO duyệt gate |
| AI không ghi duyệt khi đã sửa thêm sau câu duyệt của PO | Lời duyệt phải đến sau lần sửa cuối; AI hỏi lại một câu |
| AI hỏi PO trước khi bỏ qua một stage hoặc tắt reviewer | Các quyết định này cần lời PO, theo mục 5.4 |
| AI hỏi nhiều câu `Chặn: có` | Thiếu thông tin làm đổi phạm vi, rule, dữ liệu hoặc luồng |
| Artifact có nhiều `❓PO` | Knowledge base chưa phủ vùng đó và AI không được đoán |
| AI không tự sửa theo finding của reviewer | PO quyết định sửa hoặc chấp nhận rủi ro |

Người mới nên chạy trước một intent profile S với một yêu cầu nhỏ có thật, thử Request Changes ở một gate, đọc lại `decisions.md` và `state.md`, sau đó mới chạy intent profile M có 2.43 với các PIC.
