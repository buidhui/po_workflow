# Glossary

Thuật ngữ và họ mã của PO-Workflow, theo AWS AI-DLC Workflows 2.11, file `docs/guide/glossary.md` của repo `awslabs/aidlc-workflows`. Phần do PO-Workflow thêm ngoài AWS gắn nhãn `po-workflow`; đây là nhãn, PO-Workflow không đóng gói theo cơ chế plugin của AWS. Intent chuyển từ luồng cũ giữ họ mã cũ trong tài liệu của chúng.

## Khung
| Thuật ngữ | Nghĩa trong PO-Workflow | Nguồn |
|---|---|---|
| AI-DLC | AI-Driven Development Life Cycle, phương pháp của AWS. PO-Workflow theo phase Ideation và phần Inception do Product Agent dẫn | AWS |
| Space | Toàn bộ repo, một team. Mỗi domain một space, xem DOMAIN-SETUP.md | AWS |
| Intent | Một yêu cầu đi trọn vòng phân tích, có thư mục riêng | AWS. Thay "project" |
| Phase | Ideation, Inception. Construction và Operation ngoài phạm vi | AWS |
| Stage | Một bước có artifact và approval gate riêng, đánh số theo AWS: `1.1`, `2.3`. Stage do PO-Workflow thêm mang số thập phân `2.31`, `2.32`, `2.42`, `2.43`, là quy ước riêng của PO-Workflow để chèn vào giữa các stage gốc, không đánh lại số stage gốc. Cơ chế plugin của AWS chỉ đánh số sau stage cuối của phase và chưa cho chèn trước stage gốc | AWS, số thập phân là của PO-Workflow |
| Plugin stage | Stage do PO-Workflow thêm: 2.31, 2.32, 2.42, 2.43. Ghi `po-workflow` ở hàng Plugin trong bảng metadata | Chỉ là nhãn. Plugin thật của AWS là một repo riêng có manifest, chỉ được cộng thêm vào stage gốc; PO-Workflow không đóng gói như vậy, và còn chỉnh hai stage gốc 1.4, 2.4, ghi ở hàng Lệch so với AWS |
| Workflow profile | `S`, `M`, `L`. Tập stage, công tắc nghi thức, depth | AWS gọi là scope trong engine. Không dùng chữ Scope vì đã dùng cho phạm vi tính năng |
| Depth | Minimal, Standard, Comprehensive. Mức chi tiết artifact | AWS |
| Approval gate | Điểm duyệt cuối mỗi stage | AWS. Thay "Gate 1 đến 4" và "điểm dừng" |
| Alignment gate | Gate của 2.43, cần chữ ký của 3 PIC ở bảng Ký của Decision Brief. PIC quá hạn chưa ký thì PO được chọn Accept as-is kèm lý do | PO-Workflow |
| Summary confirmation | Xác nhận tóm tắt câu trả lời trước khi sinh artifact | AWS |
| Field Intake | Summary confirmation riêng của 2.42 về field, rule, validate | Repo |
| Questions file | `<stage>-questions.md`, nguồn sự thật của câu trả lời | AWS |
| Answer mode | Guide me, Edit file, Chat | AWS |
| Record dir | `intents/<slug>/` | AWS |
| State file | `state.md` | AWS |
| Decision Log | `decisions.md` | AWS |
| Memory | `memory.md` của intent; `memory/team.md` bài học dùng chung, đi theo engine; `memory/project.md` bài học của sản phẩm đang cài | AWS, cùng cách chia team và project |
| Learnings | Vòng học tại gate | AWS |
| Knowledge | Domain pack ở `domain/` và kiến thức vai PO ở `engine/knowledge/` | AWS |
| Engine | Phần không phụ thuộc sản phẩm: protocol, lệnh, template chung, checklist, agent, script, chuẩn bàn giao | PO-Workflow |
| Domain pack | Knowledge base của một sản phẩm trong `domain/`: manifest `domain.md`, các file KB, corner checklist, theo `engine/standards/domain-kb.md`. Không chứa template. Đổi sản phẩm là thay thư mục này, engine giữ nguyên | PO-Workflow; BABOK 9.3 Business Knowledge |
| Live source · Pinned record · Last verified | Nguồn sống, bản chốt, ngày đối chiếu của KB | Repo |
| AI Reviewer | Agent `ai-reviewer` review độc lập, không thấy hội thoại, kết luận READY hoặc NOT-READY | AWS gọi vai này là Product Lead |
| Sổ finding | `reviews/findings-<slug>.md`, danh sách finding của một stage và quyết định của PO; finding đã quyết không bị chấm lại | AWS, engine giữ danh sách finding |
| Mã tính năng | `<mã sản phẩm>-F<NNN>`, ví dụ `APP-F012`. Cấp khi tạo intent, đi theo tính năng tới PRD, story trên Jira, test case, nhánh code | Quy ước chung các team, `engine/standards/id-conventions.md` |
| Mã đầy đủ | Mã có mã tính năng, như `AC-APP-F012-01.1`, duy nhất trong toàn công ty. Dùng ở mọi nơi ngoài repo PO: Jira, Figma, nhánh, commit, test, đặc tả API | `engine/standards/naming-conventions.md` mục 3 |
| Trailer của commit | Dòng `Khoá: giá trị` ở cuối thông điệp commit, như `Implements: AC-APP-F012-01.1`; git đọc lại được bằng `git log --format='%(trailers:key=Implements,valueonly)'` | Conventional Commits 1.0.0; `git interpret-trailers` |
| Story List | `intents/<intent>/stories/story-list-prd-v<phiên bản>.csv`, mỗi US trong PRD một dòng theo mẫu import CSV của Jira. Sinh bằng `/po-stories` sau gate 2.43, profile S thì sau gate 2.42; có Jira MCP thì đẩy thẳng lên Jira thay cho import. Các team làm việc trên story Jira |
| `jira-map.json` | `intents/<intent>/stories/jira-map.json`: mã story ứng với mã issue Jira, bản PRD đã đẩy, nội dung đã đẩy. Do `po-tools.py jira-sync --record` ghi, không sửa tay | ADR 0002, mục bổ sung |
| `not-ready`, `removed-from-prd` | Hai nhãn Jira do engine gắn: story chưa đạt điều kiện sẵn sàng; story không còn trong PRD. Issue không bị xoá | `engine/standards/handoff-rules.md` | Quy ước chung các team, `engine/standards/handoff-rules.md`, ADR 0002 |
| Checkpoint | Buổi PO họp với Design PIC, Tech PIC, QA PIC trên Decision Brief ở 2.43, sau khi các team thiết kế từ PRD | Quy ước chung các team |
| Điều kiện sẵn sàng, DoR | Điều kiện để giao một story cho Dev: PRD đã duyệt, với profile M, L thì 2.43 đã duyệt, US có AC, mọi BR có AC, không còn `❓PO` và câu chặn, giao diện có màn trong `ux-design.md`, story phụ thuộc đã đạt. Kiểm bằng `po-tools.py dor` | Quy ước chung các team. Bản hẹp phía PO của Definition of Ready của AWS; hai mục thiết kế đã xem và đã ước lượng do Design, Dev làm trên Jira |
| Nguyên tắc chia story | Định nghĩa story, tiêu chí INVEST, dấu hiệu quá lớn, 8 cách tách, các cách không chia, ở `engine/standards/story-splitting.md` | PO-Workflow, theo AWS user-story-patterns |
| Tiêu chí chấp nhận, AC | Điều kiện kiểm được, đạt hoặc không đạt, theo cấu trúc Given/When/Then: tiền điều kiện, hành động, kết quả quan sát được; ghi rõ BR mà nó kiểm. Viết trong PRD ở 2.42, trước khi các team thiết kế | BABOK v3 10.1 Acceptance and Evaluation Criteria; AWS `user-story-patterns.md` |
| Template PRD chuẩn | `engine/templates/prd.md`, dùng chung cho mọi sản phẩm: 11 mục, mỗi US mười mục con. Cơ sở của từng mục ở ADR 0004 | PO-Workflow |
| EARS | Easy Approach to Requirements Syntax: năm mẫu câu cho một yêu cầu hệ thống, gồm luôn đúng, theo sự kiện "Khi…", theo trạng thái "Trong khi…", hành vi không mong muốn "Nếu…", tuỳ chọn "Với … đang bật". Yêu cầu chức năng ở `requirements.md` viết theo mẫu này; business rule thì không | Mavin và cộng sự, Rolls-Royce, RE'09; Kiro của AWS |
| Tiêu chí thành công, SC | Chỉ số đo sau phát hành cho từng mục tiêu `O<n>` của PRD, mã `SC<n>`, có cách đo và ngưỡng | GitHub Spec Kit; Success Metrics của AWS |
| Sơ đồ trạng thái | Sơ đồ vòng đời của một đối tượng đổi trạng thái, vẽ bằng `stateDiagram-v2` từ bảng chuyển trạng thái; bắt buộc trong PRD khi tính năng có đối tượng như vậy. Quy ước ở `engine/standards/diagrams.md` | AWS: máy trạng thái trong functional design |
| Phân loại yêu cầu | Bốn loại theo BABOK 2.3: yêu cầu nghiệp vụ, là mục tiêu `O` và tiêu chí thành công `SC`; yêu cầu của các bên, là user story `US`; yêu cầu giải pháp, gồm chức năng `FR`, `BR`, `AC` và phi chức năng `NFR`; yêu cầu chuyển đổi `TR`, chỉ cần khi đưa giải pháp vào dùng | BABOK v3 2.3 |
| Kiểm chứng và xác nhận | Kiểm chứng (verify) là xét yêu cầu có đạt chất lượng không: đơn nhất, đầy đủ, nhất quán, ngắn gọn, khả thi, không mơ hồ, kiểm được, có ưu tiên, dễ hiểu. Xác nhận (validate) là xét yêu cầu có phục vụ mục tiêu nghiệp vụ không, qua cột Phục vụ và truy vết về `O` | BABOK v3 7.2, 7.3 |
| Business rule, loại | Định nghĩa: ràng buộc dữ liệu, cách phân loại, cách tính. Hành vi: điều được phép, bắt buộc, bị cấm, có mức áp dụng bắt buộc, vượt được khi có người duyệt, hoặc hướng dẫn. Rule viết độc lập với cách hệ thống thực hiện. Rule dùng cho nhiều US mã `BR0.<n>` | BABOK v3 10.9 |
| Tiêu chí chấp nhận và tiêu chí đánh giá | Tiêu chí chấp nhận là điều kiện để nhận một story, viết Given/When/Then. Tiêu chí đánh giá là thước đo để so phương án hoặc đo kết quả sau phát hành, như bảy tiêu chí ở 2.32 và tiêu chí thành công `SC` | BABOK v3 10.1 |
| Quan hệ truy vết | Dẫn xuất: FR dẫn xuất từ mục tiêu. Phụ thuộc: US cần US khác xong trước. Đáp ứng: US và BR đáp ứng FR. Kiểm: AC và test case kiểm US, BR | BABOK v3 5.1 |
| Sổ rủi ro, RK | Mục Rủi ro trong `decisions.md`, mỗi rủi ro một mã `RK<n>` với khả năng, tác động, cách xử lý, owner, trạng thái; artifact khác chỉ trỏ mã | BABOK v3 6.3, 10.38 |
| Yêu cầu chuyển đổi, TR | Yêu cầu chỉ cần trong giai đoạn đưa tính năng vào dùng: dữ liệu cũ, cách bật, chạy song song, quay lui, đào tạo. Mã `TR<n>` ở Impact Matrix mục 8 và PRD mục 8 | BABOK v3 2.3, 6.4 |
| Đánh giá giải pháp | Đo lại tiêu chí thành công sau phát hành, tìm hạn chế, đề xuất hành động, bằng lệnh `/po-evaluate` | BABOK v3 chương 8 |
| PIC | Người phụ trách một mảng của tính năng: Design PIC, Tech PIC, QA PIC. Viết file thiết kế của mình và ký Decision Brief ở 2.43. Tech PIC chịu trách nhiệm cả phần Backend và Frontend của `tech-design.md` | PO-Workflow |
| Verification checklist | Checklist tự kiểm của stage cho phần cần phán đoán, mục blocking | PO-Workflow. AWS không có tên tương đương; compartment `## Sensors` của AWS là phần kiểm tự động, ứng với Kiểm bằng máy |
| Kiểm bằng máy | `po-tools.py check` và `trace`: phần kiểm được bằng script, chạy trước checklist | Tương đương sensor của AWS |
| Sổ lượt người | `.po/turns.jsonl`, hook ghi mỗi lượt PO gõ hoặc chọn; `approve` chỉ ghi duyệt khi lời PO có trong sổ. Không commit, AI không sửa được | AWS gọi là HUMAN_TURN, kiểm có người thật ở gate |
| Hook | `engine/scripts/po-hook.py`, chạy khi PO gửi câu, khi PO chọn trong hộp chọn, và trước mỗi lần AI sửa file hoặc chạy lệnh shell. Ghi sổ lượt người và chặn sửa trái quy trình | AWS core/hooks |
| Quyết định ngoài gate | Bỏ qua stage, đổi profile, bật tắt nghi thức, quyết change request, mở lại stage đã duyệt. Chỉ ghi được bằng lệnh `skip`, `profile`, `switch`, `cr`, `reopen` của `po-tools.py` với lời PO; hook chặn sửa tay | AWS ENGINE_OWNED_STATE_TRANSITIONS |
| Quyết từng mục | Ở gate, câu chặn chưa trả lời, GAP, ORPHAN, mã biến mất chỉ qua khi PO quyết riêng từng mã; lời PO phải nêu mã đó | AWS: sensor chặn có Fix hoặc Override ghi lại; không đi tiếp khi câu hỏi chưa trả lời đủ |
| Gửi ký | `po-tools.py sign-start` ghi dấu bản Decision Brief gửi PIC. Chữ ký chỉ tính với đúng bản đó, đúng tên PIC ở `intent.md` | AWS `aidlc-review-freeze`: receipt gắn với bản artifact |
| Review digest | `reviews/review-<slug>-<NN>.digest`, dấu của artifact lúc gọi reviewer, ghi bằng `po-tools.py review-start`. `approve` so dấu này để biết review còn ứng với bản hiện tại | AWS gắn biên nhận review với đúng bản đã review |
| Bản chỉ mục cho Dev | `intents/INDEX.md` do `po-tools.py index` sinh: mã tính năng, bản PRD đã duyệt, service bị chạm, tag, số story đạt điều kiện sẵn sàng | PO-Workflow |
| Tag bản duyệt | `<intent>/prd-v<X.Y>` hoặc `<intent>/decision-brief-v<X.Y>`, gắn mỗi lần PRD hoặc Decision Brief được duyệt; agent của Dev đọc theo tag | PO-Workflow |
| Phiên bản artifact | 0.x là bản nháp; lần duyệt đầu là 1.0; mỗi lần duyệt lại sau change request tăng số phụ | PO-Workflow |
| Mức độ sẵn sàng áp dụng | Quy trình đã sẵn sàng áp dụng tới đâu, theo 2 trục: phạm vi sử dụng (cá nhân, team, liên team, nhân rộng) và giao tiếp (người với người, người với máy, máy với máy). Đánh giá ở README mục 9 | PO-Workflow |
| Archive | Bản chụp tại gate và trước CR, không sửa | AWS |
| Initiative Brief | Tài liệu một trang xác định hướng đi, stage 1.7 | AWS. Thay BRD |
| Decision Brief | Tài liệu ngắn cho buổi họp quyết định ở 2.43: điểm cần quyết, đề xuất sửa PRD, mâu thuẫn giữa các thiết kế, độ phủ, độ lớn so với mốc, ý kiến phản đối nguyên văn, bảng Ký. AI viết, tối đa 1.500 từ cho phần tổng hợp | AWS dùng chữ decision brief cho bản tóm tắt trình người quyết định trước gate |
| File thiết kế của team | `ux-design.md`, `tech-design.md`, `test-design.md` ở `inception/`, do Design PIC, Tech PIC, QA PIC viết từ PRD đã duyệt; AI của PO không sửa | AWS: mỗi vai một artifact riêng ở 2.5, 2.6, 2.8, 3.1, 3.6 |
| HLD Brief | Tài liệu định hướng liên team ở stage 2.41 cũ, trước PRD. Bỏ ngày 20/10/2026, thay bằng 2.43 Design Alignment; bản cũ nằm trong `archive/hld-brief/` của intent | PO-Workflow, ADR 0003 |
| Mob, Mob Elaboration | Không dùng làm tên stage hoặc artifact. Hai nghĩa ở AWS: bài blog AI-DLC (Raja SP, 07/2025) gọi Mob Elaboration là buổi cả team cùng kiểm câu hỏi và đề xuất của AI trong Inception; bản Workflows từ v2.10 gọi mob là chế độ nhiều agent ở stage 2.4 User Stories; từ v2.11 chế độ này mặc định tắt, chỉ bật ở scope `enterprise`. Trong PO-Workflow, buổi họp trên Decision Brief ở 2.43 là bản do người thật thực hiện theo nghĩa trong bài blog; mob agent không chạy | AWS, hai nguồn |
| Unit `U` | Hạng mục trong intent backlog, sinh ở stage 1.4, nhóm user story theo giá trị và ưu tiên để xác định phạm vi và thứ tự. Ở 2.4 mỗi US gắn vào một Unit. PRD có mục Units. Unit of work của Dev ở 2.7 chia theo kiến trúc, có thể khác | AWS gọi là proto-Unit, stage 1.4. PO-Workflow gọi gọn là Unit, quyết định ngày 19/10/2026 |
| Thẻ US | Mô tả 9 mục của một user story ở 2.4: vai và mục tiêu, bối cảnh, luồng chính, nhánh đáng kể, rule đã biết, dữ liệu và vùng chạm, ngoài phạm vi, phụ thuộc, chưa rõ. Đủ để PO viết PRD, chưa có acceptance criteria | Repo. Gần mẫu mô tả luồng người dùng trong ux-guide của AWS hơn là Definition of Ready, vì chưa có AC và chưa ước lượng |
| Impact Analysis · Solution Options · Hidden · KB · CR · PRD · US · BR | Giữ nguyên | |

## Stage
| Mã | Stage | Artifact chính | Thay cho |
|---|---|---|---|
| 1.1 | Intent Capture & Framing | intent-statement.md | Bước 1 đến 3 phần vấn đề, BRD mục 1 đến 4 |
| 1.2 | Market Research | competitive-analysis.md | Nghiên cứu sản phẩm cùng loại |
| 1.4 | Scope Definition | scope-document.md, có intent backlog gồm các Unit | BRD mục 5 đến 7 |
| 1.7 | Approval & Handoff | initiative-brief.md | BRD, Gate 1 |
| 2.3 | Requirements Analysis | requirements.md | clarified-requirements |
| 2.31 | Impact Analysis | related-features-map.md, impact-matrix.md | Bước 5 và 6, Gate 2 |
| 2.32 | Solution Options | solution-options.md | Bước 7 và 8, Gate 3 |
| 2.4 | User Stories | stories.md | 9A, 9A+ |
| 2.42 | PRD Generation | prd.md, traceability.md | 9B, 9C, Gate 4 |
| 2.43 | Design Alignment | decision-brief.md; ux-design.md, tech-design.md, test-design.md do các team viết | mới |

Tiện ích:

- `/new-intent`: tạo intent, chọn profile
- `/po`: chạy stage kế tiếp hoặc tiếp tục
- `/po-status`: trạng thái mọi intent, kiểm lệch
- `/po-review`: review độc lập bằng AI Reviewer
- `/po-replay`: tóm lược diễn biến của một intent khi bàn giao giữa các PO
- `/po-stories`: đẩy story lên Jira qua MCP hoặc sinh Story List để import, từ PRD đã duyệt, sau gate 2.43 với profile M, L; kiểm điều kiện sẵn sàng
- `/change-request`: đổi yêu cầu sau khi đã duyệt
- `/generate-user-guide`: viết User Guide sau khi Dev làm xong
- `/new-domain`: dựng khung domain pack cho sản phẩm mới
- Script `engine/scripts/po-tools.py`: `next` stage kế tiếp; `check` kiểm bằng máy; `approve` ghi chép sau khi duyệt, chỉ khi lời PO có trong sổ lượt người; `review-start` ghi dấu artifact trước khi gọi reviewer; `trace` truy vết FR, US, BR, AC; `archive` chụp bản duyệt; `status` kiểm lệch giữa state và file; `feature-id` cấp mã tính năng; `stories` sinh Story List cho Jira; `jira-sync` lập kế hoạch đẩy story qua Jira MCP và ghi kết quả; `dor` kiểm điều kiện sẵn sàng; `index` sinh chỉ mục; `replay` tóm lược diễn biến của intent; `migrate` chuyển intent từ bản engine cũ; `doctor` kiểm môi trường

## Họ mã
| Họ | Dạng | Phạm vi | Ví dụ | Thay cho |
|---|---|---|---|---|
| Requirement | `FR1`, `FR1.2`, `NFR1` | intent | FR3 | RC |
| User story | `US1` | intent | US12 | giữ |
| Acceptance criteria | `AC1.1` | intent, số đầu là số US, trong PRD | AC12.2 | mới |
| Business rule | `BR1.1` | intent, số đầu là số US | BR12.3 | BR-12.3 |
| Unit | `U1` | intent | U2 | PU1, trước 19/10/2026 |
| Objective | `O1` | intent | O3 | giữ |
| Câu hỏi | `Q1` | một questions file. Stage khác trích `[2.3 Q4]` | Q4 | OQ, F, BA |
| Câu hỏi mở còn treo | `OQ1` | intent, nằm trong Assumptions & Open Questions | OQ2 | OQ-B, OQ-C |
| Quyết định | `DEC1` | intent | DEC7 | mới |
| Change request | `CR1` | intent | CR2 | CR-001 |
| Finding review | `R-01` | một stage | R-03 | mới |
| Trong Impact Matrix | `CF`, `BI`, `CG`, `TR` | một artifact | CF-2 | giữ |
| KB | `BR-<MODULE>-NN`, `KB-<MODULE>-NN` | KB | | giữ |

Quy tắc: mã đã cấp không đánh lại. Trích mã thì kèm nội dung. Mã đứng liền nhau có dấu `·` ở giữa.

Mã trên là mã ngắn, dùng trong artifact của PO và PRD. Ngoài các tài liệu đó, trên story Jira, test case và nhánh code, mọi team dùng mã đầy đủ có mã tính năng, theo `engine/standards/id-conventions.md`:

| Họ | Mã đầy đủ | Ví dụ | Ai cấp |
|---|---|---|---|
| Tính năng | `<SP>-F<NNN>` | `APP-F012` | PO, khi tạo intent |
| User story | `US-<tính năng>-<NN>` | `US-APP-F012-01` | Script đổi từ `US1` |
| Acceptance criteria | `AC-<tính năng>-<NN>.<n>` | `AC-APP-F012-01.1` | Script đổi từ `AC1.1` |
| Business rule | `BR-<tính năng>-<NN>.<n>` | `BR-APP-F012-01.2` | Script đổi từ `BR1.2` |
| Câu hỏi trên story Jira | `Q-<tính năng>-<NN>.<n>` | `Q-APP-F012-01.3` | Người hỏi |
| Màn hình | `SCR-<tính năng>-<NN>` | `SCR-APP-F012-02` | Design PIC |
| Test case | `TC-<tính năng>-<NNN>` | `TC-APP-F012-001` | QA PIC |
| Yêu cầu phi chức năng | `NFR-<tính năng>-<NN>` | `NFR-APP-F012-03` | Script đổi từ `NFR3` |
| Yêu cầu chuyển đổi | `TR-<tính năng>-<NN>` | `TR-APP-F012-01` | Script đổi từ `TR1` |

## Ký hiệu
| Ký hiệu | Nghĩa |
|---|---|
| `[ ]` `[-]` `[?]` `[R]` `[x]` `[S]` | Stage chưa làm, đang làm, chờ duyệt, đang sửa, đã duyệt, bỏ qua |
| `❓PO` | Ô không suy được, cần người điền. Không dùng làm dữ kiện |
| `[suy ra]` | AI suy luận ra; nguồn không nói trực tiếp |
| `[đề xuất]` | Đáp án AI đề xuất trong câu hỏi |
| `[uỷ quyền]` | PO để AI chọn |
| `[desc]` `[Q3]` `[KB-04 §3]` `[DEC5]` `[assumption]` | Thẻ nguồn trong artifact nội bộ |

## Cách dùng sai thường gặp
- "Scope" chỉ phạm vi tính năng In, Out, Potential. Cỡ yêu cầu là "profile".
- Story là đơn vị nghiệm thu. Story List giữ nguyên cách chia của 2.4, mỗi US một story; Design chia việc theo màn hình, Dev theo Unit of work, QA theo tiêu chí chấp nhận.
- "Unit" trong PO-Workflow là nhóm user story PO chia ở 1.4, theo giá trị và ưu tiên. "Unit of work" của AWS ở 2.7 là phần việc Dev chia theo ranh giới kỹ thuật. Hai cách chia có thể khác nhau; khi trao đổi với Dev, nếu dễ nhầm thì ghi rõ "Unit trong PRD".
- "Extension" là chữ trong nguyên lý 8 của spec 2.0. Tên cơ chế là "plugin"; stage do PO-Workflow thêm là "plugin stage".
- "Sensor" là kiểm tự động của AWS; trong repo này là `po-tools.py check` và `trace`. Checklist tự kiểm gọi là "verification checklist".
- "Lead" trong bảng metadata là agent dẫn stage theo AWS. Người phụ trách Design, Tech, QA gọi là PIC.
- "Gate 1" đến "Gate 4" là tên cũ. Gọi theo stage: "gate của 2.3".
- Dữ kiện sản phẩm không ghi vào lệnh hoặc checklist. Ghi vào `domain.md` hoặc KB, để lệnh trỏ tới.
- Mã ngắn `US1`, `AC1.1` chỉ dùng trong tài liệu của PO. Trao đổi với Design, Tech, QA và trên Jira dùng mã đầy đủ `US-<tính năng>-<NN>`.
- "Checkpoint" trong AWS là điểm duyệt ở Construction. Trong PO-Workflow, checkpoint là buổi họp trên Decision Brief ở 2.43. Khi đọc tài liệu AWS, phân biệt hai nghĩa này.
- "Mob" không dùng làm tên stage. Buổi họp trên Decision Brief gần với Mob Elaboration trong bài blog AWS, nhưng tên stage giữ là Design Alignment để không trùng chữ mob của AWS ở 2.4.
