# ADR 0004: Template PRD chuẩn chung, đặt trong engine

| | |
|---|---|
| Trạng thái | Đã quyết, thay template PRD theo sản phẩm từng nằm trong domain pack |
| Ngày | 2026-10-20 |
| Người quyết định | PO phụ trách PO-Workflow |

## Bối cảnh

Trước quyết định này, PRD viết theo template của công ty, đặt trong domain pack của từng sản phẩm, với bốn tên mục do chủ template giữ cố định. Template có hai nguồn: bản gốc trên wiki của công ty và bản điều chỉnh trong repo. Khi chạy thật trên intent thí điểm có 20 US, template gây ra năm sự việc có ghi nhận trong nhật ký quyết định của intent:

| Sự việc | Bằng chứng | Nguyên nhân |
|---|---|---|
| PRD đã duyệt nhưng chưa có tiêu chí kiểm được | CR3 ngày 20/10/2026 phải thêm 104 tiêu chí chấp nhận cho 20 US và 130 BR sau khi PRD đã duyệt ba lần (`decisions.md` DEC92) | Mục "Acceptance criteria" của template gốc chỉ chứa giải pháp nghiệp vụ, bảng UI, BR, Data Field, NFR; không có danh sách tiêu chí |
| Góc đã biết bị mất khi sang PRD | Review 2.4 lần 01 có một lỗi Critical: mục "Conner case" trống ở cả 20 US trong khi Impact Matrix đã liệt kê 15 góc. Lỗi bị bác với lý do template quy định để trống (`review-user-stories-02.md` R-01) | Quy tắc "Conner case để trống, QA điền" của bản điều chỉnh |
| Yêu cầu chuyển đổi không vào PRD | Impact Matrix mục 8 đã có dữ liệu cũ, chạy song song hai đường gán, bật làm hai lần; PRD v0.5 không có mục nào nhận các nội dung này | Template không có mục cho yêu cầu chuyển đổi |
| PRD lệch bản đã duyệt | CR4: AI sửa hai ô "Document status" và "Người duyệt" sau khi duyệt v0.4 (DEC95) | Trạng thái và người duyệt ghi trong thân tài liệu, trùng với frontmatter và git |
| Không sửa được tên mục | DEC94: đổi tên mục "Preferences" phải chờ chủ template xác nhận; lỗi chính tả "Conner case" giữ nguyên | Tên mục bị khoá theo sản phẩm |

Ngoài ra, một dữ kiện thường được viết lại ở hai hoặc ba nơi trong cùng US. Ví dụ ở US1 của intent thí điểm: câu thông báo trùng mã có ở AC1.2 và ở bảng UI; câu thông báo vượt số cấp tối đa có ở BR-1.3 và ở AC1.5. Mỗi change request phải sửa đủ các nơi đó. PRD của intent thí điểm, bản v0.5, dài 20.120 từ, 76% nằm ở phần yêu cầu theo US.

## So với AWS AI-DLC 2.11

Đối chiếu với bản `awslabs/aidlc-workflows` commit `0488aff`.

| Điểm | AWS | Quyết định |
|---|---|---|
| PRD | Không sinh PRD. PRD chỉ là tài liệu đầu vào có thể có (`core/aidlc-common/stages/ideation/intent-capture.md`, `docs/guide/08-knowledge.md`). Vai trò của PRD được chia cho `intent-statement.md`, `scope-document.md`, `requirements.md`, `stories.md`, `unit-of-work.md`, sau đó `rules.md` và `entities.md` ở phase Construction | Giữ PRD là tài liệu bàn giao duy nhất cho Design, Tech, QA, để các team đọc một tài liệu liền mạch. Cấu trúc PRD lấy theo thành phần của các artifact AWS |
| Template | Không có template mặc định ("ships NO default template files"). Thứ tự chọn: template của team ở `memory/templates/X.md`, sau đó template mặc định, cuối cùng là mô tả trong file stage. Template đã chọn được dùng nguyên khung, các mục `##` được kiểm (`core/aidlc-common/protocols/stage-protocol.md` mục Template overrides) | Engine có template `engine/templates/prd.md`, dùng chung cho mọi sản phẩm. Domain chỉ chứa knowledge base, không chứa template, nên không có tầng ghi đè; template riêng của công ty, nếu có, chỉ dùng làm bảng ánh xạ khi đăng bản đọc ra ngoài repo |
| Câu yêu cầu | "The system shall [verb] [object] [condition]" (`core/knowledge/aidlc-product-agent/requirements-guide.md`) | Business rule viết theo yêu cầu chức năng ở `requirements.md` viết theo mẫu EARS, gồm cả dạng "hệ thống phải" của AWS. Business rule trong PRD viết theo BABOK 10.9: câu khẳng định về nghiệp vụ, độc lập với cách hệ thống thực hiện, có loại định nghĩa hay hành vi; EARS là cú pháp cho yêu cầu hệ thống nên không dùng cho business rule |
| Tiêu chí chấp nhận | Given/When/Then, 3 tới 6 tiêu chí mỗi story (`user-story-patterns.md`) | Given/When/Then như AWS, theo BABOK 10.1. Quá 6 tiêu chí ở một US thì `po-tools.py` cảnh báo story có thể quá lớn |
| Giả định và câu hỏi mở | Mục `## Assumptions & Open Questions` bắt buộc ở artifact | Hai mục Giả định và Câu hỏi mở |
| Truy vết | FR sang US sang AC sang BR sang code (`core/knowledge/aidlc-shared/verification.md`) | Giữ mã `US1`, `AC1.1`, `BR1.1` và bảng truy vết hiện có |

## Chuẩn tham chiếu

- ISO/IEC/IEEE 29148:2018. Mục 9.6 quy định nội dung tài liệu yêu cầu phần mềm, gồm giả định và phụ thuộc, giới hạn, yêu cầu theo chức năng, thuộc tính chất lượng, cách kiểm chứng. Mục 5.2.5 nêu 9 đặc tính của một yêu cầu tốt: cần thiết, phù hợp, không mơ hồ, đầy đủ, đơn nhất, khả thi, kiểm chứng được, đúng, tuân thủ quy ước. Mục 5.2.6 nêu 5 đặc tính của cả tập yêu cầu: đầy đủ, nhất quán, khả thi, dễ hiểu, xác nhận được.
- EARS (Easy Approach to Requirements Syntax), Mavin và cộng sự, Rolls-Royce, hội nghị RE'09. Năm mẫu câu: luôn đúng, theo sự kiện, theo trạng thái, hành vi không mong muốn, tính năng tuỳ chọn. Nguồn: https://alistairmavin.com/ears/
- Kiro của AWS dùng EARS cho tiêu chí chấp nhận trong `requirements.md` của spec. Nguồn: https://kiro.dev/docs/specs/
- GitHub Spec Kit, template spec: User Scenarios & Testing có ưu tiên và lý do ưu tiên, Edge Cases, Functional Requirements, Key Entities, Success Criteria đo được, Assumptions; tối đa 3 chỗ `[NEEDS CLARIFICATION]`. Nguồn: https://github.com/github/spec-kit/blob/main/templates/spec-template.md và `templates/commands/specify.md`
- BABOK v3 của IIBA, mục 2.3: bốn loại yêu cầu là business, stakeholder, solution (chức năng và phi chức năng), transition.
- Mục "những gì không làm": No-gos của Shape Up (https://basecamp.com/shapeup/1.5-chapter-06) và Non-goals của design doc tại Google (https://www.industrialempathy.com/posts/design-docs-at-google/).
- HEART, Rodden, Hutchinson và Fu, Google, CHI 2010: khung tìm chỉ số trải nghiệm theo Happiness, Engagement, Adoption, Retention, Task success.

## Quyết định

Template PRD chuẩn đặt ở `engine/templates/prd.md`, dùng chung cho mọi sản phẩm. Cơ sở của từng mục:

| Mục | Cơ sở |
|---|---|
| Frontmatter và bảng thông tin rút gọn | Spec Kit ghi trạng thái ở phần đầu spec; AWS ghi version ở frontmatter. Trạng thái và người duyệt chỉ ghi ở frontmatter và `state.md`, để không lặp lại sự việc CR4 |
| Lịch sử phiên bản | Giữ từ template công ty: người đọc thấy thay đổi giữa các bản mà không phải đọc lịch sử git |
| 1. Bối cảnh và mục tiêu | Yêu cầu business của BABOK; mục mục tiêu và các bên liên quan của ISO 29148; `intent-statement.md` của AWS. PRD tóm tắt và dẫn về artifact đã duyệt |
| 2. Tiêu chí thành công | Success Criteria của Spec Kit: đo được, không gắn công nghệ, có mã. Success Metrics của AWS. HEART là kỹ thuật gợi ý, không bắt buộc |
| 3. Ngoài phạm vi | No-gos của Shape Up, Non-goals của Google, ranh giới in/out của `scope-document.md` bên AWS, mục giới hạn của ISO 29148 |
| 4. Giải pháp tổng thể | Mục góc nhìn sản phẩm và ràng buộc thiết kế của ISO 29148; phần nghiệp vụ của `functional-design` bên AWS. Cách làm kỹ thuật do Tech PIC viết ở `tech-design.md`, theo ADR 0003 |
| 5. Units | Units Generation của AWS |
| 6. Yêu cầu theo user story | User Scenarios của Spec Kit và `stories.md` của AWS. Mười mục con: User story kèm ưu tiên và lý do; Tiền điều kiện; Luồng chính; Business rule theo BABOK 10.9, có loại và mức áp dụng, rule dùng chung mã `BR0.<n>`; Tiêu chí chấp nhận Given/When/Then; Giao diện và validate, là nơi duy nhất ghi validate của màn; Dữ liệu (Key Entities của Spec Kit); NFR riêng của US; Trường hợp ngoại lệ (Edge Cases của Spec Kit, corner checklist của AWS, coverage gap của Impact Matrix); Ngoài phạm vi của US |
| 7. Yêu cầu phi chức năng | Thuộc tính chất lượng của ISO 29148; nhóm NFR của AWS: hiệu năng, bảo mật, khả năng mở rộng, độ tin cậy, khả năng quan sát; mỗi NFR có chỉ số đo |
| 8. Chuyển đổi và triển khai | Yêu cầu transition của BABOK: dữ liệu hiện có, chuyển đổi dữ liệu, cách bật, chạy song song, quay lui, tenant, hướng dẫn người dùng. Các template spec cho AI như Spec Kit và Kiro không có phần này |
| 9. Giả định | Mục giả định và phụ thuộc của ISO 29148; Assumptions của AWS và Spec Kit. Mỗi giả định ghi hệ quả nếu sai |
| 10. Câu hỏi mở | Open Questions của AWS; giới hạn 3 chỗ chưa rõ của Spec Kit, áp cho ký hiệu `❓PO` khi trình duyệt |
| 11. Truy vết | Chuỗi truy vết của AWS; thuộc tính truy vết của ISO 29148 |

Ánh xạ cho người quen template công ty:

| Template công ty | Template chuẩn |
|---|---|
| Bảng đầu, Document version, Document status | Frontmatter, bảng thông tin rút gọn, Lịch sử phiên bản |
| Problem, Analytics, Objective, Stakeholder | 1. Bối cảnh và mục tiêu |
| Metrics success | 2. Tiêu chí thành công |
| Out of scope | 3. Ngoài phạm vi |
| Solution, Technical Direction, Data to Retain | 4. Giải pháp tổng thể |
| Units | 5. Units |
| Specific Requirement với sáu mục mỗi US | 6. Yêu cầu theo user story với mười mục mỗi US |
| NFR trong từng US | 7. Yêu cầu phi chức năng, NFR riêng vẫn ở US |
| Chưa có | 8. Chuyển đổi và triển khai |
| Chưa có | 9. Giả định |
| Open Issues | 10. Câu hỏi mở |
| Traceability | 11. Truy vết |
| Comments | Góp ý qua review trong repo |

Mã `US1`, `AC1.1`, `BR1.1` không đổi, nên `po-tools.py` truy vết, kiểm điều kiện sẵn sàng và sinh Story List như cũ. Script nhận thêm tên mục mới và bỏ qua kiểm tên mục với PRD viết theo template cũ.

## Mức tin cậy của bằng chứng

- Bằng chứng nội bộ ở mục Bối cảnh là sự việc có ghi trong repo, nhưng chỉ từ một intent.
- Bằng chứng bên ngoài mạnh nhất nói về yêu cầu thiếu hoặc mơ hồ. Khảo sát NaPiRE ở 228 công ty xếp "yêu cầu không đầy đủ hoặc bị ẩn" là vấn đề phổ biến nhất, 48% (https://arxiv.org/abs/1611.10288). OpenAI ghi nhận 38,3% mẫu của SWE-bench có đề bài mô tả thiếu (https://openai.com/index/introducing-swe-bench-verified/). ClarifyGPT cho thấy để mô hình hỏi lại chỗ chưa rõ trước khi viết code làm tăng tỉ lệ code đúng của GPT-4 trên MBPP từ 70,96% lên 80,80% (https://arxiv.org/abs/2310.10996). Các bằng chứng này ủng hộ tiêu chí kiểm được, mục ngoại lệ, giả định và câu hỏi mở; chúng không so sánh trực tiếp hai template.
- EARS chủ yếu có case study của chính nhóm tác giả. Spec-driven development chưa có nghiên cứu đối chứng; Thoughtworks Technology Radar xếp ở mức Assess và cảnh báo spec dài thì khó review (https://www.thoughtworks.com/radar/techniques/spec-driven-development).

## Hệ quả

- PRD không còn phụ thuộc sản phẩm. Sản phẩm mới không phải viết template PRD khi dựng domain pack.
- Góc ngoại lệ và yêu cầu chuyển đổi đã có trong Impact Matrix được đưa vào PRD, nên Design, Tech, QA nhận đủ.
- Một dữ kiện chỉ ghi ở một nơi: validate ở bảng giao diện, luật ở business rule, tiêu chí chấp nhận trỏ về hai nơi đó.
- Người quen template công ty cần đọc bảng ánh xạ một lần. PRD đã duyệt theo template cũ giữ nguyên; chuyển sang template mới qua change request.
- Template riêng của công ty không thay template engine. Công ty cần bản đọc theo mẫu riêng thì repo sản phẩm tự chuyển đổi khi đăng ra ngoài; bản chính thức vẫn là file trong git.

## Cách đo hiệu quả

So intent đầu tiên viết theo template chuẩn với PRD v0.5 của intent thí điểm (20 US, 104 AC, 130 BR, 20.120 từ, bốn change request trong 11 ngày từ 09/10 tới 20/10/2026) theo sáu chỉ số: số từ trên mỗi US; số change request sau khi duyệt; số lỗi Critical và Major ở review; tỉ lệ BR có AC trỏ tới; số câu Design, Tech, QA hỏi lại sau khi nhận PRD; số ngày từ 2.3 tới khi PRD được duyệt. Hai intent là mẫu nhỏ, nên kết quả là tín hiệu để quyết định tiếp, chưa phải bằng chứng thống kê.
