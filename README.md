# PO-Workflow

PO-Workflow là quy trình phân tích yêu cầu dành cho Product Owner (PO) làm việc cùng AI. Quy trình đi từ yêu cầu ban đầu tới PRD theo template chuẩn, sau đó bàn giao cho Design, Tech và QA theo một bộ quy ước chung. AI đảm nhận việc đọc tài liệu, đặt câu hỏi, soạn bản nháp và tự kiểm tra; PO trả lời câu hỏi, ra quyết định và phê duyệt ở cuối mỗi stage.

Mọi câu trả lời, quyết định và bản đã duyệt được lưu trong repo git của sản phẩm. Nhờ đó, PO và các team tra cứu được người quyết định, nội dung quyết định và thời điểm quyết định của từng yêu cầu.

| Tài liệu | Người đọc | Nội dung |
|---|---|---|
| README.md | Mọi người | Giới thiệu quy trình: phạm vi, nguyên lý, stage, kiểm tra chất lượng, chuẩn đầu ra |
| [USER-GUIDE.md](USER-GUIDE.md) | PO, các PIC, Dev | Thao tác hằng ngày |
| [GLOSSARY.md](GLOSSARY.md) | Mọi người | Thuật ngữ và họ mã |
| [DOMAIN-SETUP.md](DOMAIN-SETUP.md) | Người phụ trách quy trình | Đưa một sản phẩm mới vào quy trình |
| [engine/standards/](engine/standards/) | Design, Tech, QA | Nguyên tắc chia story, quy ước mã, quy ước đặt tên và liên kết, quy tắc bàn giao |
| [AGENTS.md](AGENTS.md) | Công cụ AI | Quy tắc AI phải tuân thủ khi làm việc với PO; `CLAUDE.md` chỉ nạp lại file này |
| [CHANGELOG.md](CHANGELOG.md) | Người phụ trách quy trình | Thay đổi của từng phiên bản và cách nâng cấp |

## Mục lục

1. [Tổng quan](#1-tổng-quan)
2. [Nguyên lý nền](#2-nguyên-lý-nền)
3. [Quy trình](#3-quy-trình)
4. [Từng stage](#4-từng-stage)
5. [Kiểm tra chất lượng](#5-kiểm-tra-chất-lượng)
6. [Đầu ra chuẩn cho các team](#6-đầu-ra-chuẩn-cho-các-team)
7. [Sau PRD](#7-sau-prd)
8. [Cấu trúc repo và nâng cấp](#8-cấu-trúc-repo-và-nâng-cấp)
9. [Cơ sở phương pháp](#9-cơ-sở-phương-pháp)

## 1. Tổng quan

### 1.1 Phạm vi

Mỗi yêu cầu là một intent, lưu tại `intents/<YYMMDD-slug>/`. Intent đi qua tối đa 10 stage thuộc hai phase. Ideation xác định vấn đề và phạm vi. Inception chuyển phạm vi thành yêu cầu, phân tích ảnh hưởng lên hệ thống đang vận hành, so sánh phương án giải pháp, chia user story và viết PRD; sau đó Design, Tech, QA thiết kế dựa trên PRD và thống nhất các điểm còn vướng mắc trên Decision Brief. Mỗi stage tạo ra một artifact và kết thúc bằng một gate do PO phê duyệt.

Quy trình dành cho sản phẩm đã có người dùng và dữ liệu. Trọng tâm của quy trình là xác định tác động của tính năng mới lên hệ thống đang vận hành trước khi viết chi tiết.

| Áp dụng cho | Không áp dụng cho |
|---|---|
| Tính năng mới hoặc thay đổi tính năng của sản phẩm | Thay PO ra quyết định về phạm vi, nghiệp vụ và mức ưu tiên |
| Yêu cầu từ một màn hình tới nhiều module; mức độ được xác định bằng profile | Thiết kế kỹ thuật chi tiết: cơ sở dữ liệu, API, thuật toán |
| Từ yêu cầu ban đầu tới PRD và Decision Brief | Xây dựng, kiểm thử, phát hành và vận hành phần mềm |
| Story List; User Guide sau khi Dev hoàn thành | Quản lý tiến độ thay cho Jira |
| Change request; đánh giá sau phát hành | Bàn giao tài liệu chưa được duyệt |

Điều kiện bắt đầu: sản phẩm đã có knowledge base, theo hướng dẫn trong [DOMAIN-SETUP.md](DOMAIN-SETUP.md).

### 1.2 Vai trò

| Vai | Trách nhiệm |
|---|---|
| AI | Đọc knowledge base, schema, đặc tả API trước khi đặt câu hỏi; đặt câu hỏi có lựa chọn, kèm đề xuất và nguồn; soạn artifact theo template, ghi nguồn cho mọi khẳng định; tự kiểm tra bằng script và checklist; chỉ ra trùng lặp, xung đột và phần còn thiếu; đánh dấu `❓PO` ở phần chưa rõ thay vì suy đoán |
| PO | Cung cấp yêu cầu gốc và bối cảnh trong `inputs/`; trả lời câu hỏi; quyết định phạm vi, nghiệp vụ và mức ưu tiên; phê duyệt hoặc yêu cầu chỉnh sửa tại mỗi gate; quyết định bỏ qua stage, đổi profile, chấp nhận change request; đưa story lên Jira; chọn bài học cần lưu giữ |
| AI Reviewer | Agent độc lập, chỉ đọc artifact, không tiếp cận hội thoại giữa PO và AI; kết luận READY hoặc NOT-READY trước gate |
| Design PIC | Viết `ux-design.md` dựa trên PRD, đặt mã màn hình, ký Decision Brief |
| Tech PIC | Viết `tech-design.md` cho Backend và Frontend, chia story thành Unit of work, ký Decision Brief |
| QA PIC | Viết `test-design.md` bao phủ từng tiêu chí chấp nhận, ký Decision Brief, viết test case gắn mã tiêu chí chấp nhận |
| Người tài trợ | Người có thẩm quyền quyết định cuối cùng về việc tiếp tục hoặc dừng intent, ghi tại `intent.md` |
| Người phụ trách quy trình | Duy trì quy trình và knowledge base của sản phẩm, tổng hợp bài học, hỗ trợ PO |

### 1.3 Đầu ra bàn giao

Quy trình có năm đầu ra bàn giao. Các artifact còn lại là bản phân tích nội bộ của PO.

| Đầu ra | Người nhận | Thời điểm |
|---|---|---|
| Initiative Brief | Người tài trợ | Cuối Ideation, profile L |
| PRD | Design, Tech, QA | Khi stage 2.42 được duyệt |
| Decision Brief | Design PIC, Tech PIC, QA PIC, PO | Sau khi các team viết thiết kế, profile M và L |
| Story List, mỗi user story một story trên Jira | Design, Tech, QA | Sau gate 2.43; với profile S, sau khi PRD được duyệt |
| User Guide | Người dùng cuối | Sau khi Dev hoàn thành |

### 1.4 Đặc điểm chính

| Đặc điểm | Cơ chế |
|---|---|
| PO tập trung vào phân tích và ra quyết định | AI đọc tài liệu, đặt câu hỏi và soạn artifact theo template; PO trả lời và phê duyệt tại gate. Lời duyệt phải có trong lượt nhập của PO, nên AI không thể tự duyệt |
| Phân tích dựa trên hệ thống đang vận hành | AI tra cứu knowledge base trước khi đặt câu hỏi; phân tích ảnh hưởng theo 12 vùng được thực hiện trước khi lựa chọn giải pháp; schema và đặc tả API được đọc lại khi intent liên quan tới vùng tương ứng |
| Quyết định được lưu vết | Câu trả lời, lời duyệt và quyết định được ghi nguyên văn kèm người quyết định và thời điểm; quyết định ngoài gate chỉ ghi được bằng lệnh có lời PO |
| Tính nhất quán từ yêu cầu đến kiểm thử | Mã ổn định cho yêu cầu, user story, business rule và tiêu chí chấp nhận; story trên Jira, test case và commit dẫn chiếu tới mã đầy đủ |
| Các team thống nhất trước khi phát triển | Design, Tech, QA thiết kế dựa trên PRD; AI tổng hợp các điểm cần quyết định vào Decision Brief cho một buổi họp; ba PIC ký trước khi story được tạo |
| Thay đổi yêu cầu được kiểm soát | Change request quay lại đúng stage bị ảnh hưởng; bản đã duyệt được lưu trong `archive/`; Story List mới được đối chiếu với bản trước |
| Chuyển giao người phụ trách không mất bối cảnh | `decisions.md` và `state.md` lưu toàn bộ diễn biến của intent; `/po-replay` tóm lược cho người tiếp nhận |
| Sử dụng chung cho nhiều sản phẩm | Phần quy trình dùng chung tách khỏi knowledge base của từng sản phẩm; có hướng dẫn đưa sản phẩm mới vào, lệnh nâng cấp và bộ kiểm thử đi kèm |

### 1.5 Khác biệt so với việc soạn tài liệu trực tiếp bằng AI hội thoại

| Khía cạnh | Soạn trực tiếp bằng AI hội thoại | PO-Workflow |
|---|---|---|
| Hiểu biết về hệ thống hiện hành | AI suy luận từ kiến thức chung | AI đọc knowledge base của sản phẩm, phân tích ảnh hưởng, đọc lại nguồn sống |
| Thông tin còn thiếu | AI tự bổ sung phần còn thiếu | AI đánh dấu `❓PO` hoặc đặt câu hỏi chặn, tạm dừng cho tới khi PO trả lời |
| Lưu vết quyết định | Phân tán trong lịch sử hội thoại | Ghi nguyên văn, kèm người quyết định và thời điểm |
| Kiểm soát chất lượng | PO tự rà soát thủ công | Script kiểm tra, checklist có mục chặn, AI Reviewer độc lập |
| Truy vết | Cấu trúc tài liệu không thống nhất giữa các lần soạn | Mã ổn định; story đưa thẳng lên Jira; test case gắn mã tiêu chí chấp nhận |
| Thay đổi yêu cầu | Soạn lại hoặc sửa thủ công | Change request quay lại đúng stage liên quan, giữ nguyên bản đã duyệt |
| Chuyển giao người phụ trách | Bối cảnh không được lưu giữ | Hồ sơ đầy đủ cho từng intent, kèm bản tóm lược tự động |

## 2. Nguyên lý nền

Mọi quy tắc của quy trình xuất phát từ bảy nguyên lý dưới đây. Khi một quy tắc chưa rõ lý do, người đọc tra cứu nguyên lý tương ứng.

| Nguyên lý | Nội dung | Áp dụng trong quy trình |
|---|---|---|
| Human-in-the-loop | AI đề xuất, PO quyết định; không bước nào được thực hiện tiếp khi PO chưa phê duyệt | Gate cuối mỗi stage; lời duyệt được ghi nguyên văn vào `decisions.md` |
| Requirements Engineering | Khơi gợi, phân tích, đặc tả, kiểm chứng và xác nhận là các việc tách biệt | Questions file, phân tích yêu cầu và ảnh hưởng, PRD, checklist, AI Reviewer |
| Context Engineering | AI được cung cấp đúng và đủ thông tin cho công việc đang thực hiện | Bước Load đầu mỗi stage đọc knowledge base của sản phẩm, nhật ký quyết định và bài học |
| Quality Gate | Mỗi đầu ra được kiểm tra trước khi làm nền tảng cho đầu ra tiếp theo | Script kiểm tra, checklist có mục chặn, AI Reviewer, năm lựa chọn tại gate |
| Iterative Refinement | Mức chi tiết tăng theo mức chắc chắn | Profile S, M, L; thẻ user story trước, PRD sau, thiết kế của các team sau PRD |
| Requirement Traceability | Yêu cầu, user story, business rule và tiêu chí chấp nhận truy được về nhau và về nguồn | Mã ổn định, thẻ nguồn, bảng truy vết, mã đầy đủ khi bàn giao |
| Responsible AI | AI không tự điền khi thiếu thông tin; con người chịu trách nhiệm cuối cùng | Ký hiệu `❓PO`, đọc lại nguồn sống, chỉ bàn giao bản đã duyệt |

Từ các nguyên lý trên, quy trình đặt bốn quy tắc làm việc cho mọi stage:

- AI không tự điền dữ kiện. Khi thiếu thông tin nhỏ, AI ghi giả định. Khi thiếu thông tin làm thay đổi phạm vi, rule, dữ liệu hoặc luồng, AI ghi câu hỏi mở và tạm dừng. Nội dung không thể suy ra từ nguồn được đánh dấu `❓PO`.
- AI dừng ở mức phân tích nghiệp vụ. Khi cần xác định sự tồn tại của một cơ chế kỹ thuật, AI đặt câu hỏi cho PO. Một endpoint có trong đặc tả API chưa chứng minh tính năng còn hoạt động.
- Knowledge base là bản chụp tại một thời điểm. Schema dữ liệu, đặc tả API và tài liệu người dùng là nguồn sống; khi yêu cầu liên quan tới vùng nào, AI đọc lại nguồn của vùng đó. Nguồn quá 30 ngày chưa đối chiếu cũng phải được đọc lại.
- Câu trả lời và quyết định của PO được ghi nguyên văn. AI tra cứu nhật ký quyết định trước khi đặt câu hỏi.

## 3. Quy trình

### 3.1 Sơ đồ

```mermaid
flowchart TD
    IN["Yêu cầu ban đầu<br/>inputs/"] --> S11["1.1 Intent Capture & Framing"]
    S11 --> S12["1.2 Market Research<br/>có điều kiện"]
    S11 --> S14["1.4 Scope Definition<br/>Unit U1, U2"]
    S12 --> S14
    S14 ==>|"gate"| S17["1.7 Approval & Handoff<br/>Initiative Brief"]
    S17 ==>|"gate, có Reject Initiative"| S23["2.3 Requirements Analysis<br/>FR, NFR"]
    S23 ==>|"gate"| S231["2.31 Impact Analysis<br/>Impact Matrix"]
    S231 ==>|"gate"| S232["2.32 Solution Options<br/>có điều kiện"]
    S231 --> S24
    S232 ==>|"gate"| S24["2.4 User Stories<br/>thẻ US"]
    S24 ==>|"gate"| S242["2.42 PRD Generation<br/>AC, BR"]
    S242 ==>|"gate"| S243["2.43 Design Alignment<br/>3 file thiết kế, Decision Brief"]
    S243 ==>|"Alignment gate<br/>3 PIC ký"| ST["Story List<br/>đưa lên Jira"]
    ST --> UG["User Guide<br/>sau khi Dev hoàn thành"]
```

### 3.2 10 stage

| Stage | Mục đích | Artifact chính | Profile |
|---|---|---|---|
| 0 Khởi tạo | Dựng thư mục intent, cấp mã tính năng, chọn profile | `intent.md`, `state.md`, `decisions.md` | Mọi profile |
| 1.1 Intent Capture & Framing | Xác định vấn đề, mục tiêu đo được, các bên liên quan; tách giải pháp người yêu cầu đề xuất khỏi vấn đề | `intent-statement.md` | M, L |
| 1.2 Market Research | So sánh với sản phẩm khác theo khía cạnh đã chọn | `competitive-analysis.md` | L, có điều kiện |
| 1.4 Scope Definition | Xác định In, Out, Potential; chia nhu cầu thành Unit có mức ưu tiên | `scope-document.md` | M, L |
| 1.7 Approval & Handoff | Tóm tắt Ideation thành một trang để người tài trợ quyết định tiếp tục hoặc dừng | `initiative-brief.md` | L |
| 2.3 Requirements Analysis | Chuyển phạm vi thành yêu cầu có mã; tra cứu knowledge base để tìm trùng lặp và rule chi phối | `requirements.md` | S, M, L |
| 2.31 Impact Analysis | Xác định phần bị ảnh hưởng của hệ thống đang vận hành; tìm xung đột | `impact-matrix.md` | M, L |
| 2.32 Solution Options | So sánh các hướng giải quyết theo bảy tiêu chí | `solution-options.md` | L, có điều kiện |
| 2.4 User Stories | Chia yêu cầu thành user story; mỗi US một thẻ chín mục đủ để viết PRD | `stories.md` | M, L |
| 2.42 PRD Generation | PRD theo template chuẩn, chi tiết từng US, có tiêu chí chấp nhận, trường hợp ngoại lệ, yêu cầu chuyển đổi và truy vết | `prd.md` | S, M, L |
| 2.43 Design Alignment | Ba team viết thiết kế dựa trên PRD; AI đối chiếu và viết Decision Brief; tổ chức họp, ba PIC ký | `decision-brief.md` | M, L |

Định nghĩa đầy đủ của từng stage nằm trong `engine/stages/`.

### 3.3 Profile và depth

Khi tạo intent, AI rà soát nhanh yêu cầu và knowledge base, đề xuất profile kèm lý do; PO có quyền thay đổi. Khi chưa xác định rõ giữa hai profile, chọn profile lớn hơn.

| Profile | Quy mô và độ phức tạp | Stage thực hiện | AI Reviewer | Số gate |
|---|---|---|---|---|
| S | Một màn hình, không đổi data model, không đổi rule có sẵn, không tác động tới module khác, không liên quan tính năng ẩn, không tích hợp bên ngoài, không chuyển đổi dữ liệu | 2.3 và 2.42, PRD rút gọn | 2.42 | 2 |
| M | Tối đa hai module, thêm field nhưng không đổi quan hệ bảng, không xung đột, hướng giải quyết đã rõ ràng | 1.1 và 1.4 duyệt chung, 2.3, 2.31, 2.4, 2.42, 2.43 | 2.3, 2.4, 2.42 | 6 |
| L | Có ít nhất một yếu tố: từ ba module trở lên, đổi data model, xung đột với rule hiện có, liên quan tính năng ẩn, nhiều hướng giải quyết, tích hợp bên ngoài, chuyển đổi dữ liệu, thao tác không hoàn tác được | Đủ 10 stage; 1.2 và 2.32 khi cần | 1.1, 2.3, 2.4, 2.42 | 8 đến 10 |

Depth quyết định mức chi tiết của artifact. Template đánh dấu mục tuỳ chọn bằng `<!-- tuỳ chọn -->`; mục không có dấu là bắt buộc.

| Depth | Mục bắt buộc | Mục tuỳ chọn |
|---|---|---|
| Minimal | Viết ngắn, chỉ ghi điều đã quyết định | Bỏ qua |
| Standard | Viết đầy đủ | Viết khi có nội dung |
| Comprehensive | Viết đầy đủ | Viết toàn bộ; mục không áp dụng ghi lý do |

### 3.4 Chuỗi đầu ra

Artifact được tạo theo thứ tự: Unit tại 1.4, yêu cầu chức năng tại 2.3, user story tại 2.4, tiêu chí chấp nhận và business rule trong PRD tại 2.42, sau đó ba file thiết kế của các team và Decision Brief tại 2.43. Các team thiết kế dựa trên PRD chi tiết, vì một bản định hướng ngắn không đủ để thực hiện Technical Design, Test Design và UI/UX Design. PRD chỉ chứa yêu cầu; thiết kế được lưu trong file riêng của từng team.

```mermaid
flowchart LR
    subgraph PO["PO-Workflow"]
        direction LR
        S14["1.4 Unit<br/>U1, U2"] --> S23["2.3 Yêu cầu<br/>FR1, NFR1"]
        S23 --> S24["2.4 Thẻ US<br/>gắn Unit, chưa có AC"]
        S24 --> S242["2.42 PRD<br/>AC, BR, truy vết"]
        S242 --> DB["2.43 Decision Brief<br/>3 PIC ký"]
        DB --> ST["Story trên Jira<br/>mã đầy đủ, mã màn"]
    end
    subgraph TEAMS["Các team, tại 2.43"]
        direction LR
        D["ux-design<br/>màn hình SCR"]
        T["tech-design<br/>Backend, Frontend, hợp đồng API"]
        Q["test-design<br/>phủ AC"]
    end
    S242 ==> D
    S242 ==> T
    S242 ==> Q
    D ==> DB
    T ==> DB
    Q ==> DB
```

Unit là nhóm user story theo giá trị và mức ưu tiên. Dev có thể chia việc theo kiến trúc, khác với cách nhóm này.

### 3.5 Bảy bước của một stage

Mọi stage thực hiện cùng bảy bước, định nghĩa trong `engine/protocol/stage-protocol.md`.

| Bước | AI thực hiện | PO thực hiện |
|---|---|---|
| 1. Load | Đọc trạng thái, quyết định trước đó, artifact đầu vào, knowledge base và bài học | |
| 2. Ask | Lập bảng độ phủ các chủ đề của stage, đặt câu hỏi cho mọi chủ đề đầu vào chưa được trả lời; mỗi câu ghi rõ người trả lời, tối đa bốn lựa chọn, đề xuất kèm nguồn và cờ chặn; phân tích câu trả lời mơ hồ, mâu thuẫn và hỏi tiếp | Trả lời câu hỏi |
| 3. Confirm | Tóm tắt câu trả lời | Xác nhận hoặc yêu cầu sửa |
| 4. Generate | Soạn artifact theo template, ghi thẻ nguồn ở mỗi khẳng định; tại 1.1 và 2.3, trình bày giả định để PO chấp nhận hoặc chuyển thành câu hỏi | Xác nhận giả định |
| 5. Verify | Chạy script kiểm tra và checklist, gọi AI Reviewer theo profile | |
| 6. Learn | Ghi quan sát vào `memory.md` của intent | |
| 7. Gate | Trình thông điệp hoàn thành, đề nghị PO chọn bài học và phê duyệt; ghi kết quả bằng script | Chọn bài học; phê duyệt hoặc chọn phương án khác |

Stage tạm dừng khi còn câu hỏi chặn chưa được trả lời. PO chọn một trong ba cách trả lời cho cả intent: Guide me, AI hỏi từng câu qua hộp chọn; Edit file, PO điền trực tiếp vào questions file; Chat, PO trả lời bằng ngôn ngữ tự nhiên và AI tách theo từng câu. Câu trả lời luôn được ghi vào questions file trước khi kết thúc lượt, để không bị mất khi phiên làm việc được nén.

### 3.6 Gate và quyết định

Thông điệp tại gate gồm năm phần: stage đã hoàn thành; bảng artifact, tóm tắt bằng số liệu; kết quả review và finding còn mở; đường dẫn tới artifact; stage kế tiếp và người thực hiện. PO có năm lựa chọn:

| Lựa chọn | Trường hợp áp dụng | Hệ quả |
|---|---|---|
| Approve | Mọi gate | Script ghi phiên bản, lưu bản chụp bản duyệt, ghi quyết định, chuyển sang stage kế tiếp |
| Request Changes | Mọi gate | AI chỉnh sửa theo nội dung PO nêu và trình lại |
| Accept as-is | Từ lần Request Changes thứ ba; tại Alignment gate, có ngay khi PIC quá hạn chưa ký | Chấp nhận bản hiện tại kèm điều kiện và lý do |
| Add stage | Ideation và Inception | Thực hiện thêm một stage ngoài profile |
| Reject Initiative | Chỉ áp dụng tại 1.7 | Dừng intent |

PO phê duyệt bằng ngôn ngữ tự nhiên. Với câu trả lời như "Ok nhưng đổi tên trường X", AI chỉnh sửa trước, xác nhận lại bằng một câu hỏi và chỉ ghi nhận Approve khi PO trả lời. Khi PO yêu cầu thêm một việc mà không nêu lời duyệt, gate vẫn mở.

Quyết định chỉ đến từ PO, được bảo đảm bằng ba lớp:

1. Hook của Claude Code ghi mỗi lượt PO nhập hoặc chọn vào `.po/turns.jsonl`. Lời duyệt chỉ được ghi nhận khi có nguyên văn trong một lượt nhập của PO sau lần sửa artifact cuối cùng.
2. Lời chấp nhận chung chỉ áp dụng cho cảnh báo thông thường của bước kiểm tra bằng máy. Ba loại mục sau phải được sửa, hoặc PO quyết định riêng từng mục bằng một câu nêu rõ mã: câu hỏi chặn chưa được trả lời; liên kết truy vết ở trạng thái GAP hoặc ORPHAN; mã có trong bản duyệt trước nhưng không còn trong bản hiện tại. Ví dụ lời PO: "Hoãn Q3 sang đợt sau, FR4 làm ở intent khác."
3. Năm quyết định ngoài gate, gồm bỏ qua stage, đổi profile, bật hoặc tắt AI Reviewer và các bước tuỳ chọn, quyết định change request, mở lại gate đã ghi nhầm, chỉ được ghi bằng lệnh kèm lời PO trong ba lượt nhập gần nhất. Mỗi quyết định thêm một dòng vào `decisions.md`; hook ngăn AI sửa thủ công các dòng tương ứng trong `state.md`. Danh sách lệnh nằm trong USER-GUIDE.md mục 5.4.

Bản nháp mang phiên bản 0.x. Lần duyệt đầu là 1.0; mỗi lần duyệt lại sau change request tăng số phụ, ví dụ 1.0 thành 1.1. Bản trong `archive/` không bao giờ bị sửa.

## 4. Từng stage

### 0 Khởi tạo, lệnh /new-intent

AI dựng thư mục intent từ template và cấp mã tính năng dạng `<mã sản phẩm>-F<NNN>`; mã sản phẩm lấy từ `domain/domain.md`. Khi chưa có mô tả yêu cầu, AI đặt sẵn mẫu `inputs/request.md` để người yêu cầu điền: hiện trạng, điều cần thay đổi, trong và ngoài phạm vi, điều không được thay đổi, mốc thời gian, câu hỏi mở. AI rà soát nhanh đầu vào và knowledge base để ước lượng vùng bị tác động, đề xuất profile và ghi quyết định chọn profile thành `DEC1`.

### 1.1 Intent Capture & Framing

AI tách giải pháp người yêu cầu nêu sẵn khỏi vấn đề. "Thêm nút export" là một giải pháp; vấn đề có thể là "không lấy được dữ liệu để đối chiếu". Câu hỏi tập trung vào vấn đề theo góc nhìn người dùng, cách xử lý hiện tại, tiêu chí đo lường thành công, lý do thực hiện vào thời điểm này, các bên liên quan và phạm vi loại trừ. Artifact `intent-statement.md` có thẻ nguồn ở mọi khối khẳng định và có mục Giả định và câu hỏi mở.

### 1.2 Market Research

Stage có điều kiện, thực hiện khi PO cần so sánh với sản phẩm khác hoặc khi cách làm phổ biến trên thị trường ảnh hưởng tới phạm vi. Danh sách sản phẩm so sánh mặc định ghi trong `domain.md`. AI trích nguồn kèm link và ngày đọc, không suy diễn tính năng từ tên menu. Artifact gồm bảng so sánh, các điểm nên và không nên áp dụng, và đối chiếu với yêu cầu hiện tại.

### 1.4 Scope Definition

AI phân loại In, Out, Potential và chia nhu cầu thành Unit mã `U1`, `U2`, sắp xếp theo MoSCoW. Bốn quy tắc chia: theo cơ chế thay vì theo màn hình; xác định hạng mục nền; tách riêng hạng mục tác động toàn hệ thống như phân quyền, bật tắt, lịch sử; phụ thuộc chỉ đi một chiều. Hạng mục Won't vẫn được định nghĩa để bước phân tích ảnh hưởng rà soát đúng phạm vi. Profile M duyệt 1.1 và 1.4 chung một gate.

### 1.7 Approval & Handoff

AI tóm tắt phase Ideation thành Initiative Brief một trang gửi người tài trợ: vấn đề và mục tiêu, phạm vi, Unit và mức ưu tiên, rủi ro lớn, quyết định đã đưa ra, khuyến nghị tiếp tục hoặc dừng. Đây là gate duy nhất có lựa chọn Reject Initiative. Trước gate, AI kiểm tra ranh giới phase: mọi mục tiêu có hạng mục phục vụ, mọi Unit truy về một mục tiêu, phạm vi loại trừ không mâu thuẫn với phạm vi thực hiện, câu hỏi chặn đã được đóng.

### 2.3 Requirements Analysis

Với từng hạng mục, AI tra cứu knowledge base trước khi hỏi: tính năng đã tồn tại chưa, rule nào chi phối, tính năng ẩn nào liên quan, thông báo nào liên quan, hạng mục có nằm trong vùng knowledge base chưa bao phủ. Yêu cầu trùng lặp với tính năng đã có được nêu ngay, kèm mã trong knowledge base. Sau đó AI rà soát sáu chiều để tìm phần còn thiếu: hành vi chức năng, yêu cầu phi chức năng đo được, kịch bản người dùng và trường hợp biên, bối cảnh nghiệp vụ, tích hợp và dữ liệu, chất lượng; kèm corner checklist của sản phẩm. Artifact `requirements.md` có yêu cầu chức năng mã `FR1`, `FR1.1` viết theo mẫu câu EARS, kèm mức ưu tiên và cờ Existing, New, Changed; yêu cầu phi chức năng có chỉ số đo; ràng buộc; câu hỏi mở `OQ1`; phạm vi loại trừ; nguồn đã đọc. Yêu cầu mô tả điều phải đúng, không đề cập tới bảng, endpoint hoặc thuật toán.

### 2.31 Impact Analysis

AI lập Related Features Map từ yêu cầu, knowledge base, schema và đặc tả API để PO rà soát; rà soát một bản nháp giúp phát hiện thiếu sót dễ hơn so với liệt kê từ đầu. Sau khi PO xác nhận bản đồ, AI lập Impact Matrix theo năm bước: hiện trạng và phụ thuộc, trạng thái mong muốn, ma trận 12 vùng, chuyển đổi dữ liệu, các câu kiểm riêng của sản phẩm ghi trong `domain.md`. Xung đột theo bốn chiều rule, quy trình, dữ liệu, phân quyền được chuyển cho PO quyết định, mỗi xung đột một dòng quyết định. Ảnh hưởng được xét theo hai chiều: từ tính năng mới sang phần hiện có và ngược lại.

### 2.32 Solution Options

Stage có điều kiện, thực hiện khi có từ hai hướng giải quyết hoặc PO chưa có hướng. AI xây dựng phương án từ các hướng khác nhau: đổi quy trình, cấu hình, mở rộng tính năng có sẵn, làm mới, cắt giảm phạm vi; luôn có phương án giữ nguyên để so sánh. Mọi phương án được chấm theo bảy tiêu chí có trọng số: phù hợp nghiệp vụ, tác động người dùng, tác động hệ thống và dữ liệu, công sức, rủi ro, phụ thuộc, nợ kỹ thuật. Công sức và rủi ro ghi Cao, Trung bình, Thấp kèm lý do, không ước lượng số giờ.

### 2.4 User Stories

AI chia yêu cầu thành user story theo `engine/standards/story-splitting.md`. Mỗi US gắn một Unit, và mỗi yêu cầu chức năng có ít nhất một US bao phủ. Mỗi US có một thẻ chín mục: vai và mục tiêu, bối cảnh, luồng chính, nhánh đáng kể, rule đã biết, dữ liệu và vùng bị tác động, ngoài phạm vi, phụ thuộc, điểm chưa rõ. Thẻ đủ để viết PRD mà không phải mở lại requirements, và chưa có tiêu chí chấp nhận. Các PIC không xem thẻ ở bước này; họ đọc PRD chi tiết một lần tại 2.43. Script truy vết báo yêu cầu chưa có US và US không truy về yêu cầu nào.

### 2.42 PRD Generation

Bước hỏi của stage này là Field Intake. AI tra cứu Impact Matrix, data model, đặc tả API và knowledge base, phân loại mỗi màn hình là màn mới, sửa màn có sẵn hoặc chỉ đọc, sau đó lập một bảng field, rule, validate để PO duyệt. Với field đã có, AI chỉ hỏi phần thay đổi. Field Intake bắt buộc với cả profile S, vì đây là bước dễ phát sinh sai sót nhất.

PRD theo template chuẩn `engine/templates/prd.md`, dùng chung cho mọi sản phẩm; cơ sở của từng mục ghi tại `engine/standards/adr/0004-template-prd-chuan.md`. PRD có 11 mục:

1. Bối cảnh và mục tiêu
2. Tiêu chí thành công đo được, mã `SC<n>`
3. Ngoài phạm vi
4. Giải pháp tổng thể, gồm rule dùng chung, quy tắc tính toán, quyền theo vai, vòng đời trạng thái
5. Units
6. Yêu cầu theo user story
7. Yêu cầu phi chức năng
8. Chuyển đổi và triển khai
9. Giả định
10. Câu hỏi mở
11. Truy vết

Mục 1 đến 5 tóm tắt từ artifact đã duyệt. Mỗi US ở mục 6 có mười mục con: user story kèm mức ưu tiên, tiền điều kiện, luồng chính, business rule, tiêu chí chấp nhận, giao diện và validate, dữ liệu, yêu cầu phi chức năng riêng nếu có, trường hợp ngoại lệ lấy từ Impact Matrix, ngoài phạm vi của US. Business rule mã `BR<US>.<n>` ghi rõ loại định nghĩa hoặc hành vi; rule dùng chung cho nhiều US mang mã `BR0.<n>`. Tiêu chí chấp nhận mã `AC<US>.<n>` viết theo Given/When/Then, xem mục 6.5. Một dữ kiện chỉ được ghi ở một nơi: nội dung thông báo ghi tại bảng giao diện, quy tắc nghiệp vụ ghi tại business rule, tiêu chí chấp nhận dẫn chiếu tới hai nơi trên bằng mã.

Sơ đồ viết bằng Mermaid ngay trong file, theo `engine/standards/diagrams.md`; bảng là nguồn chính, sơ đồ là bản vẽ từ bảng. Tính năng có đối tượng thay đổi trạng thái thì PRD bắt buộc có vòng đời trạng thái: bảng chuyển trạng thái và sơ đồ `stateDiagram-v2`. Script kiểm tra đối chiếu từng chuyển trạng thái giữa bảng và sơ đồ, báo trạng thái không tới được hoặc không có đường ra, và kiểm tra cú pháp của mọi sơ đồ.

PRD được viết trước khi các team thiết kế. Với điểm phụ thuộc thiết kế hoặc kỹ thuật mà artifact đã duyệt chưa đề cập, AI ghi đề xuất có đánh dấu kèm câu hỏi gắn tên PIC; các team trả lời tại 2.43. PRD không có mục Database và API, không thiết kế bảng hoặc thuật toán; hằng số ghi rõ là giá trị cố định hoặc cấu hình; field đã có không được mô tả như field mới.

### 2.43 Design Alignment

Stage thực hiện ở profile M và L, sau khi PRD được duyệt. Design PIC, Tech PIC, QA PIC đọc PRD và mỗi người viết một file trong intent:

| File | Người viết | Nội dung |
|---|---|---|
| `inception/ux-design/ux-design.md` | Design PIC | Danh sách màn hình có mã `SCR`, luồng màn hình, accessibility |
| `inception/tech-design/tech-design.md` | Tech PIC, cùng người phụ trách Backend và Frontend | Thành phần bị tác động ở hai phía, quyết định kỹ thuật, hợp đồng API giữa hai phía, dữ liệu và xử lý ở Backend, màn hình và component ở Frontend, cách đáp ứng BR, NFR, TR, Unit of work và độ lớn |
| `inception/test-design/test-design.md` | QA PIC | Chiến lược kiểm thử, kế hoạch bao phủ từng tiêu chí chấp nhận, vùng hồi quy |

Mỗi file có mục Ý kiến về PRD với lập trường Đồng ý, Đề xuất sửa hoặc Phản đối. AI của PO chỉ tạo khung file, không viết và không sửa nội dung.

Script đối chiếu ba file với PRD: US có giao diện đã có màn hình chưa, tiêu chí chấp nhận đã có trong kế hoạch kiểm thử chưa, US đã có trong thiết kế kỹ thuật chưa, mỗi màn hình đã có ở phần Frontend chưa, file có được lập từ bản PRD hiện tại chưa. AI xét thêm mâu thuẫn giữa các thiết kế, độ lớn so với mốc thời gian và ý kiến của các team. Kết quả là Decision Brief: phần tổng hợp tối đa 1.500 từ, chỉ ghi các điểm cần quyết định, kèm bảng Ký.

Bản Decision Brief gửi cho các PIC được ghi dấu. Chữ ký chỉ được tính khi tên người ký trùng tên PIC tại `intent.md`, cột Bản trùng bản đã gửi, và Decision Brief không bị sửa sau lần gửi đó. Buổi họp diễn ra trên Decision Brief; quyết định làm thay đổi yêu cầu được thực hiện qua change request trên PRD. Gate là Alignment gate: Approve khi cả ba PIC ghi Đồng ý hoặc Có ý kiến; khi PIC quá hạn chưa ký, PO được chọn Accept as-is kèm lý do. Story List chỉ được tạo sau gate này. Lý do lựa chọn cách làm này ghi tại `engine/standards/adr/0003-thiet-ke-cua-team-va-decision-brief.md`.

## 5. Kiểm tra chất lượng

Mỗi gate có hai lớp kiểm tra: lớp do máy thực hiện và lớp cần đánh giá chuyên môn. Hook đứng ngoài hai lớp này và ngăn các thao tác trái quy trình.

| Lớp | Công cụ | Nội dung kiểm tra |
|---|---|---|
| Máy | `po-tools.py check` | Heading bắt buộc theo template; thẻ nguồn; `[Qn]` và `[DECn]` có thật; thẻ US đủ chín mục; chữ mẫu còn sót; mục không được có trong PRD; mã AC không trùng; tiêu chí chấp nhận theo Given/When/Then; vòng đời trạng thái khớp sơ đồ; cú pháp mọi sơ đồ Mermaid; US thiếu dòng Ưu tiên hoặc thiếu AC cho trường hợp lỗi; mã có trong bản duyệt trước nhưng không còn trong bản hiện tại; US giữ mã nhưng đổi hẳn tên. Tại 2.43, kiểm tra thêm độ phủ của ba file thiết kế, giới hạn số từ và chữ ký của Decision Brief |
| Máy | `po-tools.py trace` | Yêu cầu sang US, US sang yêu cầu, BR sang AC, US trong PRD; báo GAP và ORPHAN; dừng với lỗi khi không đọc được mã nào |
| Đánh giá chuyên môn | Checklist trong `engine/verification/` | Các nội dung cần đọc hiểu; gate chỉ mở khi mọi mục có nhãn BLOCK đã đạt |
| Đánh giá chuyên môn | AI Reviewer, định nghĩa trong `engine/agents/ai-reviewer.md` | Mức độ rõ ràng để Dev thực hiện, khả năng QA viết test từ tiêu chí chấp nhận, giả định ngầm chưa được PO xác nhận, nội dung vượt phạm vi, ranh giới trong và ngoài phạm vi; kết luận READY hoặc NOT-READY |
| Ngăn chặn | Hook `engine/scripts/po-hook.py` | AI không tự ghi duyệt, không sửa artifact đã duyệt, không sửa dòng quyết định cũ, không tự bỏ qua stage, đổi profile, tắt bước tuỳ chọn, đổi trạng thái change request hoặc mở lại stage; AI Reviewer chỉ ghi file review của mình |

| Mức finding | Ý nghĩa | Chặn READY |
|---|---|---|
| Critical | Tài liệu thiếu hoặc mâu thuẫn cơ bản, không thể triển khai | Có |
| Major | Tài liệu triển khai được nhưng sẽ phải làm lại hoặc gây hiểu lầm | Có, khi có quá hai Major |
| Minor | Nội dung nên sửa | Không |

AI Reviewer chỉ nhận đường dẫn file và kết quả kiểm tra bằng máy. Trước khi review, phiên bản artifact được ghi dấu; nếu artifact thay đổi sau mốc đó, việc phê duyệt yêu cầu review lại hoặc lời chấp nhận của PO. Kết luận READY khi không có lỗi Critical và có tối đa hai lỗi Major đã có phương án xử lý. Finding dựa trên sở thích chủ quan chỉ được xếp tối đa ở mức Minor. Từ lần review thứ hai, reviewer nhận sổ finding của stage; finding đã được PO chấp nhận rủi ro hoặc bác bỏ không bị đánh giá lại. AI không tự sửa theo finding; PO quyết định chỉnh sửa hoặc ghi nhận Accepted risk.

Phase check thực hiện ở ranh giới phase: Ideation tại 1.7, hoặc tại gate chung của 1.1 và 1.4 với profile M; Inception tại 2.43 với profile M, L và tại 2.42 với profile S. Lệnh `po-tools.py status` phát hiện thêm artifact đã duyệt bị sửa ngoài change request, artifact được lập trên bản cũ của đầu vào, và nguồn knowledge base quá hạn đối chiếu.

Bản thân các script cũng được kiểm tra. Lệnh `po-tools.py selftest` chạy 137 tình huống mẫu trong `engine/tests/fixtures/`; mỗi tình huống là một intent nhỏ dựng sẵn, kèm lệnh cần chạy và kết quả đúng. Selftest còn kiểm tra mọi lệnh đều có tình huống kiểm, tài liệu chỉ nhắc lệnh và đường dẫn có thật; GitHub Actions chạy lại selftest ở mỗi lần đẩy code lên repo. Người sửa quy trình thực hiện theo `AGENTS.md`, mục Sửa engine.

## 6. Đầu ra chuẩn cho các team

Đầu ra của PO là đầu vào của Design, Tech và QA. Mọi team sử dụng chung một cách chia story, một quy ước mã, một Story List và một bộ điều kiện sẵn sàng. Chuẩn đầy đủ nằm trong `engine/standards/`.

### 6.1 Mỗi team nhận gì

| Team | Đầu vào | Nơi nhận | Thời điểm |
|---|---|---|---|
| Design | PRD kèm bảng giao diện để viết `ux-design.md`; Decision Brief; story trên Jira có mã màn hình | `inception/`, Jira | Khi PRD được duyệt |
| Tech, gồm Backend và Frontend | PRD, Impact Matrix, danh sách màn hình của ux-design để viết `tech-design.md`; Decision Brief; story trên Jira để chia Unit of work và sub-task | `inception/`, Jira | Khi PRD được duyệt |
| QA | PRD kèm tiêu chí chấp nhận có mã để viết `test-design.md`; Decision Brief; story trên Jira để gắn test case | `inception/`, Jira | Khi PRD được duyệt |
| Agent AI của Dev | PRD theo tag của bản đã duyệt; ba file thiết kế; bảng chỉ mục; story trên Jira | Repo, `intents/INDEX.md`, Jira | Sau gate 2.43; profile S sau gate 2.42 |

### 6.2 Checkpoint và bàn giao cho Dev

| Mốc | Thời điểm | Đầu vào | Kết quả |
|---|---|---|---|
| Checkpoint | Stage 2.43, sau khi PRD được duyệt | PRD đã duyệt; ba file thiết kế; Decision Brief | Họp trên Decision Brief, ba PIC ký; cỡ story và thay đổi PRD được thống nhất |
| Bàn giao cho Dev | Sau gate 2.43; profile S sau gate 2.42 | Story List trên Jira | Story đạt điều kiện sẵn sàng, xem mục 6.7 |

### 6.3 Nguyên tắc chia story

Story là đơn vị nghiệm thu: một việc người dùng thực hiện trọn vẹn được và kiểm tra được bằng tiêu chí chấp nhận. PO chia story một lần tại 2.4; Story List giữ nguyên cách chia này, mỗi US tương ứng một story, và các team không chia lại story. Nguyên tắc đầy đủ nằm trong `engine/standards/story-splitting.md`:

1. Mỗi story là một mục tiêu hoàn chỉnh của một vai, đi trọn từ giao diện tới rule và dữ liệu, và đạt bộ tiêu chí INVEST.
2. Story được xác định từ bản đồ story theo vai và bước trong hành trình người dùng; mỗi ô "vai và mục tiêu" là một story ứng viên.
3. Dấu hiệu story quá lớn: tên có chữ "và" nối hai việc, nhiều hơn một vai cùng hưởng giá trị, luồng chính hơn bảy bước, gồm cả cấu hình và sử dụng, tác động tới hơn hai module, hơn sáu tiêu chí chấp nhận. Script cảnh báo hai dấu hiệu: chữ "và" trong tên tại 2.4 và hơn sáu AC tại 2.42.
4. Tám cách tách, áp dụng theo thứ tự: theo bước trong luồng, theo vai, theo biến thể nghiệp vụ, theo biến thể dữ liệu, theo thao tác xem, tạo, sửa, xoá, luồng đơn giản trước, đảm bảo đúng trước và tối ưu sau, theo kênh.
5. Không chia theo màn hình, tầng kỹ thuật, từng business rule, việc thuần kỹ thuật hoặc người thực hiện.
6. Mỗi story thuộc đúng một Unit.

Cỡ story được xác nhận tại checkpoint. Tech PIC ghi trong `tech-design.md` story nào quá lớn để hoàn thành trong một sprint; story cần tách được xử lý qua change request trên PRD trước khi tạo Story List, và phần tách ra nhận mã mới.

| Team | Chia việc theo | Quan hệ với story |
|---|---|---|
| Design | Màn hình, mã `SCR` | Một màn hình có thể phục vụ nhiều story |
| Dev | Unit of work, sau đó là sub-task trên Jira | Một Unit of work gồm một hoặc nhiều story |
| QA | Tiêu chí chấp nhận | Mỗi tiêu chí chấp nhận có ít nhất một test case |

### 6.4 Mã chung

PRD và artifact của PO sử dụng mã ngắn để dễ đọc. Khi tạo Story List, script chuyển sang mã đầy đủ có mã tính năng; từ đó mọi team chỉ sử dụng mã đầy đủ.

| Đối tượng | Mã đầy đủ | Ví dụ | Người cấp |
|---|---|---|---|
| Tính năng | `<SP>-F<NNN>` | `APP-F012` | PO, khi tạo intent |
| User story | `US-<tính năng>-<NN>` | `US-APP-F012-01` | PO, tại 2.4 |
| Tiêu chí chấp nhận | `AC-<tính năng>-<NN>.<n>` | `AC-APP-F012-01.1` | PO, tại 2.42 |
| Business rule | `BR-<tính năng>-<NN>.<n>` | `BR-APP-F012-01.2` | PO, tại 2.42 |
| Yêu cầu phi chức năng | `NFR-<tính năng>-<NN>` | `NFR-APP-F012-03` | PO, tại 2.3 |
| Yêu cầu chuyển đổi | `TR-<tính năng>-<NN>` | `TR-APP-F012-01` | PO, tại 2.31 |
| Câu hỏi trên story | `Q-<tính năng>-<NN>.<n>` | `Q-APP-F012-01.3` | Người đặt câu hỏi |
| Màn hình | `SCR-<tính năng>-<NN>` | `SCR-APP-F012-02` | Design PIC |
| Test case | `TC-<tính năng>-<NNN>` | `TC-APP-F012-001` | QA PIC |
| Nhánh code | `<loại>/<key Jira>-<mô tả>` | `feat/APP-123-khoa-tai-khoan` | Dev |
| Commit | Trailer `Refs`, `Feature`, `Story`, `Implements` | `Implements: AC-APP-F012-01.1` | Dev |

Mã đã cấp không thay đổi và không được tái sử dụng. Khi tách một story, phần tách ra nhận số mới; AC chuyển đi nhận mã mới và dòng cũ ghi "chuyển sang", để test case gắn mã cũ vẫn truy được tới mã mới. Script đối chiếu mã của mỗi bản với bản đã duyệt trước và chặn khi một mã bị mất. Chi tiết nằm trong `engine/standards/id-conventions.md`.

Cách mã xuất hiện ở từng nơi nằm trong `engine/standards/naming-conventions.md`: khoá đầu file dùng chung như `feature`, `inputs`, `implements`; tên frame Figma bắt đầu bằng mã màn hình; nhánh mang key Jira; commit có trailer `Implements`; test tự động gắn tag mã AC; đặc tả API có trường `x-requirements`; file truy vết `traceability.json` cho mỗi tính năng. Nhờ đó, agent của từng team tìm được mọi file liên quan tới một mã bằng `git grep`, và liệt kê được các vị trí cần sửa khi PRD thay đổi. Khi team sử dụng công cụ sinh đặc tả có hệ mã riêng, mã riêng của công cụ được ghi kèm mã đầy đủ trong ngoặc trên cùng dòng.

### 6.5 Tiêu chí chấp nhận

Tiêu chí chấp nhận là thoả thuận giữa PO và QA về điều kiện nghiệm thu một story. Business rule định nghĩa quy tắc; bảng giao diện đặc tả màn hình; mỗi tiêu chí chấp nhận viết theo cấu trúc Given/When/Then, có kết quả đạt hoặc không đạt, mô tả hành vi mà người dùng quan sát được, và ghi rõ business rule được kiểm tra. QA chuyển trực tiếp được tiêu chí thành kịch bản kiểm thử.

```
- AC1.1 Khoá tài khoản ở lần nhập sai thứ 5 · Theo BR1.2
  - Given người dùng đã nhập sai mật khẩu 4 lần liên tiếp
  - When người dùng nhập sai lần thứ 5
  - Then hệ thống khoá tài khoản và hiển thị câu thông báo của bảng giao diện
- AC1.2 Bỏ trống field bắt buộc · Theo bảng giao diện màn Đăng nhập
  - Given người dùng đang ở màn Đăng nhập
  - When người dùng bỏ trống một field bắt buộc và bấm Đăng nhập
  - Then hệ thống báo lỗi ở field đó và không gửi yêu cầu
```

Độ phủ bắt buộc: luồng chính và mỗi nhánh đáng kể trong thẻ US có ít nhất một tiêu chí; mỗi US có ít nhất một tiêu chí cho trường hợp lỗi hoặc bị từ chối; mỗi ngưỡng số có tiêu chí tại giá trị biên; mỗi business rule có ít nhất một tiêu chí dẫn chiếu tới. Validate của cùng một màn hình gom thành một tiêu chí dẫn chiếu tới bảng giao diện, để số test case không tăng theo số field. Tại 2.43, QA PIC lập kế hoạch bao phủ từng tiêu chí trong `test-design.md` và ghi tiêu chí không kiểm thử được ở mục Ý kiến về PRD.

### 6.6 Story List

Mỗi US trong PRD tương ứng một story trên Jira. Lệnh `/po-stories` đưa story lên Jira theo một trong hai cách với cùng nội dung: đẩy trực tiếp qua Jira MCP, hoặc nhập file CSV theo mẫu import của Jira. Story List được tạo sau khi PRD được duyệt, và với profile M, L thì sau gate 2.43. Nội dung nghiệp vụ chỉ có một nguồn là PRD.

| Cột | Nội dung |
|---|---|
| Project key, Project name, Project type | Dự án Jira, lấy từ frontmatter `domain/domain.md` |
| Issue Type | `Story`, thay đổi được bằng khoá `jira_story_type` của `domain.md` |
| Summary | Tên user story |
| Priority | Từ dòng Ưu tiên của US: Must chuyển thành Highest, Should thành High, Could thành Medium |
| Description | Mô tả, tiền điều kiện, kịch bản, tiêu chí chấp nhận, giao diện và validate, business rule, dữ liệu, yêu cầu phi chức năng, ngoài phạm vi, tham chiếu tới PRD, tag và mã màn hình lấy từ `ux-design.md`; cú pháp Jira, mã đầy đủ |
| Epic Link | Mã Epic ở dòng Jira Epic của `intent.md`; nhiều Epic thì ghi `U2: <mã Epic>` để gán theo Unit |
| Labels, ba cột | Mã tính năng, mã story, mã tính năng kèm Unit |
| Comment | Nguồn PRD và tag, kết quả điều kiện sẵn sàng, câu hỏi còn mở, nhắc Dev điền story point và thứ tự |

Story chưa đạt điều kiện sẵn sàng vẫn được đưa lên Jira, gắn nhãn `not-ready` kèm lý do. Story không còn trong PRD được gắn nhãn `removed-from-prd`; issue không bị xoá. PO xác nhận trước mỗi lần đưa story lên Jira. Thao tác của hai cách nằm trong USER-GUIDE.md mục 7.1.

Trên Jira, Design gắn mã màn hình và link thiết kế, Tech gom story vào Unit of work, chia sub-task và ước lượng story point, QA viết test case gắn mã AC. Câu hỏi nghiệp vụ được ghi bằng comment trên story; câu trả lời làm thay đổi PRD được xử lý qua change request. Quy tắc đầy đủ nằm trong `engine/standards/handoff-rules.md` và `engine/standards/adr/0002-story-tren-jira.md`.

### 6.7 Điều kiện sẵn sàng

Một story được bàn giao cho Dev khi đạt đủ bảy điều kiện:

1. PRD đã duyệt.
2. Với profile M, L: 2.43 Design Alignment đã duyệt, tức các team đã thiết kế và đã thống nhất trên Decision Brief.
3. US có ít nhất một tiêu chí chấp nhận.
4. Mọi business rule của US đều có ít nhất một tiêu chí chấp nhận dẫn chiếu tới.
5. US không còn `❓PO`, và mục Câu hỏi mở của PRD không còn câu chặn gắn với US đó.
6. US có bảng giao diện thì có màn hình tương ứng trong `ux-design.md`; Story List lấy mã màn hình `SCR` từ đó.
7. Các US mà mục Tiền điều kiện yêu cầu phải hoàn thành trước cũng đạt các điều kiện trên.

Hai điều kiện còn lại của Definition of Ready, thiết kế đã được xem và story đã được ước lượng, do Design và Dev thực hiện trên Jira. Script kiểm tra bảy điều kiện cho từng story và ghi kết quả vào cột Comment của Story List; cách chạy nằm trong USER-GUIDE.md mục 7.3.

### 6.8 Phiên bản, tag và chỉ mục

Mỗi PRD và Decision Brief đã duyệt được gắn tag git dạng `<intent>/prd-v1.0` hoặc `<intent>/decision-brief-v1.0`. Chỉ mục `intents/INDEX.md` gồm mã tính năng, bản PRD đã duyệt, ngày duyệt, service bị tác động, tag, nơi đăng bản đọc nếu có, số story đạt điều kiện sẵn sàng và số story đã đẩy lên Jira. Agent AI của Dev đọc PRD theo tag, nên luôn lấy đúng phiên bản đã duyệt. Thao tác gắn tag và cập nhật chỉ mục nằm trong USER-GUIDE.md mục 7.2.

### 6.9 Thay đổi yêu cầu sau bàn giao

Thay đổi liên quan tới stage đã duyệt được xử lý qua change request, xem mục 7; PRD được duyệt lại thành bản mới, ví dụ 1.1. Story List được tạo lại từ bản PRD mới: story thay đổi được cập nhật, story mới được tạo, story bị loại bỏ được gắn nhãn `removed-from-prd`. PO thông báo cho các PIC cần xem xét lại. Kết quả kiểm thử ghi kèm bản PRD được sử dụng, để xác định kết quả còn hiệu lực với bản PRD hiện tại.

### 6.10 Nơi lưu và quyền truy cập

Story List và `jira-map.json` lưu trong `intents/<intent>/stories/` của repo PO, mỗi phiên bản PRD một file CSV. Việc chia và theo dõi công việc nằm trên Jira. Các PIC cần quyền ghi repo để viết file thiết kế và ký Decision Brief, nên họ cũng đọc được phần làm việc nội bộ của PO. Trước khi cấp quyền, PO rà soát thông tin nhạy cảm như tài khoản môi trường thử nghiệm; workflow gitleaks quét thông tin nhạy cảm ở mỗi lần đẩy code lên repo. AI chỉ đọc nguồn ghi trong `domain.md`; dữ liệu cá nhân của người dùng hoặc khách hàng không được đưa vào `inputs/`.

## 7. Sau PRD

`/change-request` phân loại thay đổi trước. Thay đổi nhỏ trong stage đang mở chỉ cần sửa và trình lại gate. Với thay đổi liên quan tới stage đã duyệt, AI ghi `CR<n>` ở trạng thái chờ PO quyết định, đánh giá các mã bị tác động, mục tiêu bị ảnh hưởng, công sức và độ khẩn; PO quyết định nhận, hoãn hoặc bác. Khi PO nhận, stage thấp nhất bị sai lệch được mở lại; AI lưu bản chụp artifact bị tác động với nhãn pre-CR, sửa phần bị tác động và trình lại gate. Thao tác chi tiết nằm trong USER-GUIDE.md mục 6.

| Loại thay đổi | Quay lại stage |
|---|---|
| Vấn đề, mục tiêu | 1.1 |
| Phạm vi | 1.4 |
| Yêu cầu mới | 2.3 |
| Ảnh hưởng mới | 2.31 |
| Hướng giải quyết | 2.32 |
| Danh sách user story | 2.4 |
| Chi tiết user story | 2.42 |
| Thiết kế của các team, quyết định trong buổi họp | 2.43, PIC ký lại |

`/generate-user-guide` soạn hướng dẫn cho người dùng cuối từ PRD đã duyệt, sau khi Dev hoàn thành, theo `engine/templates/user-guide.md`, lưu tại nơi ghi trong `domain/domain.md`. Sau đó AI cập nhật knowledge base với rule mới và field đã thay đổi, để lần phân tích ảnh hưởng tiếp theo không dựa trên dữ liệu cũ.

`/po-evaluate` thực hiện sau khi tính năng phát hành, theo thời điểm đo ghi ở PRD mục 2. AI hỏi số liệu thực tế của từng tiêu chí thành công, so với giá trị hiện tại và mục tiêu, tìm hạn chế của giải pháp và của tổ chức; PO quyết định giữ nguyên, cải tiến, điều chỉnh vận hành hoặc quay lui.

Bản chính thức của mọi artifact là file trong repo: bản đã duyệt có tag git và bản chụp trong `archive/`. Quy trình không tự đăng tài liệu lên wiki. Khi team cần bản đọc ở nơi khác, người phụ trách quy trình thêm lệnh đăng cho repo của sản phẩm và ghi nơi đăng ở khoá `published` của frontmatter; `po-tools.py status` báo khi bản đăng lệch phiên bản với file. Bản đăng chỉ để đọc, không được chỉnh sửa tại đó.

## 8. Cấu trúc repo và nâng cấp

| Thư mục | Nội dung | Thuộc về |
|---|---|---|
| `engine/` | Stage, lệnh, protocol, template, checklist, agent, script, chuẩn bàn giao, kiến thức vai PO | Quy trình dùng chung |
| `domain/` | Knowledge base của sản phẩm theo `engine/standards/domain-kb.md`, gồm `domain.md`, các file KB, corner checklist | Sản phẩm |
| `intents/` | Hồ sơ từng yêu cầu | Sản phẩm |
| `memory/` | `team.md` bài học dùng chung; `project.md` bài học của sản phẩm | Cả hai |
| `.claude/` | Cấu hình riêng cho Claude Code: lối tắt cho lệnh và cho AI Reviewer trỏ tới file trong `engine/`; quyền và hook trong `settings.json` | Công cụ |
| `.po/` | Sổ ghi các lượt nhập của PO trên thiết bị đang sử dụng, để kiểm tra lời duyệt; không commit | Công cụ |
| `AGENTS.md`, `CLAUDE.md` | Quy tắc cho AI; `CLAUDE.md` nạp lại `AGENTS.md` | Quy trình dùng chung |

Lệnh chính của PO là `/po`; stage không có lệnh riêng. Khi sử dụng công cụ AI khác Claude Code, AI đọc `AGENTS.md` trước, sau đó đọc lệnh hoặc stage cần thực hiện trong `engine/commands/`, `engine/stages/`.

Mỗi intent có cấu trúc:

```
intents/<YYMMDD-slug>/
├── intent.md        bối cảnh, mã tính năng, người phụ trách, liên kết Figma, Jira
├── state.md         trạng thái từng stage, việc kế tiếp, phiên bản, nhật ký
├── decisions.md     quyết định nguyên văn, change request, sổ rủi ro
├── memory.md        quan sát của AI trong quá trình làm việc
├── inputs/          yêu cầu gốc và tài liệu đầu vào
├── ideation/  inception/   artifact theo stage
├── stories/         Story List theo phiên bản PRD; bảng đối chiếu story với issue Jira
├── design/          ảnh thiết kế, mockup PO dùng làm tham chiếu
├── user-guide/      User Guide soạn sau khi Dev hoàn thành
├── evaluation/      đánh giá giải pháp sau phát hành
├── reviews/         review của AI Reviewer, dấu artifact lúc review, dấu bản gửi ký
├── verification/    phase check, kết quả kiểm tra bằng máy
└── archive/         bản đã duyệt và bản trước change request, không chỉnh sửa
```

Khi quy trình có bản mới, người phụ trách quy trình cập nhật repo của sản phẩm theo DOMAIN-SETUP.md mục 2. Script phát hiện file của quy trình bị sửa thủ công, bài học dùng chung được gộp theo dòng, bộ kiểm thử xác nhận script vẫn chạy đúng, và intent tạo từ bản cũ được chuyển đổi mà không chỉnh sửa `archive/` hoặc `reviews/`. Dòng Tương thích của mỗi bản trong CHANGELOG cho biết các intent đang thực hiện có cần chuyển đổi.

## 9. Cơ sở phương pháp

Quy trình được xây dựng trên các phương pháp và chuẩn sau.

| Nguồn | Phần áp dụng trong quy trình |
|---|---|
| [AWS AI-DLC Workflows](https://github.com/awslabs/aidlc-workflows) 2.11, commit `0488aff`, giấy phép MIT-0 | Cấu trúc phase, stage và gate; bảy bước của một stage; vai review độc lập; cách tách phần quy trình dùng chung khỏi công cụ AI; vòng bài học dùng chung và bài học của sản phẩm; gói kiến thức vai Product trong `engine/knowledge/` |
| BABOK v3, IIBA | Sáu nhóm nghiệp vụ phân tích: lập kế hoạch và giám sát (profile, gate, nhật ký quyết định); khơi gợi và cộng tác (questions file, Decision Brief); phân tích chiến lược (phase Ideation); phân tích yêu cầu và định nghĩa thiết kế (2.3 đến 2.42); quản lý vòng đời yêu cầu (mã ổn định, truy vết, change request); đánh giá giải pháp (`/po-evaluate`). Kỹ thuật business rule (10.9) và tiêu chí chấp nhận (10.1) |
| Scrum Guide 2020 | Bốn trách nhiệm của PO với backlog: mục tiêu sản phẩm (1.1, Initiative Brief); hạng mục backlog (PRD, Story List); thứ tự backlog (MoSCoW cho Unit, Priority trên Jira); backlog minh bạch (repo, tag, `intents/INDEX.md`) |
| ISO/IEC/IEEE 29148:2018; EARS, Mavin và cộng sự, RE'09; GitHub Spec Kit | Chất lượng và định danh yêu cầu; mẫu câu yêu cầu chức năng; cấu trúc template PRD, chi tiết tại ADR 0004 |
| Stage-Gate, Robert G. Cooper, 1986 | Gate giữa các stage |
| Bohner và Arnold, 1996 | Phân tích ảnh hưởng trước khi thay đổi, Impact Matrix |
| Architecture Decision Record, Michael Nygard, 2011 | Nhật ký quyết định `decisions.md` |
| NIST AI RMF 1.0, 2023 | Nguyên lý Responsible AI |
| Conventional Commits 1.0.0, Conventional Branch 1.1.0, OpenAPI 3.1.1, MADR 4.0.0 | Quy ước đặt tên và liên kết, chi tiết tại `engine/standards/naming-conventions.md` |

Thay đổi của từng phiên bản nằm trong [CHANGELOG.md](CHANGELOG.md).
