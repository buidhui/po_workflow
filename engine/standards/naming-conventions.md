# Quy ước đặt tên và liên kết giữa các team

Áp cho mọi thứ sinh ra từ một tính năng sau PO: tài liệu thiết kế, Figma, story và test case trên Jira, nhánh, commit, pull request, đặc tả API, test tự động. Mục tiêu: từ một mã, người và agent của Design, Tech, QA tìm ra được mọi file liên quan, và khi PO đổi yêu cầu thì agent của từng team tự liệt kê được chỗ phải sửa. Bảng mã nằm ở `id-conventions.md`; tài liệu này quy định cách các mã đó xuất hiện ở từng nơi.

Trạng thái: mục 1 tới 5 áp dụng cho repo PO. Mục 6 tới 10 nằm trong repo và công cụ của các team, có hiệu lực khi Tech PIC và QA PIC đồng ý; mỗi team ghi quyết định áp dụng vào ADR của mình.

## 1. Cơ sở

| Quy ước | Nguồn |
|---|---|
| Mã không đổi, không dùng lại kể cả khi yêu cầu bị xoá | ISO/IEC/IEEE 29148:2018 mục 5.2.8.2; BABOK v3 3.4, thuộc tính absolute reference |
| Mã là khoá truy vết, stage sau giữ nguyên, không đánh lại | AWS AI-DLC 2.11, `requirements-analysis.md` bước 10: "permanent traceability keys" |
| Thư mục intent `<YYMMDD>-<nhãn>`, tên artifact chữ thường và gạch nối | AWS AI-DLC, `docs/reference/16-artifact-vocabulary.md` |
| File truy vết máy đọc, tập trạng thái đóng OK, GAP, ORPHAN, Deferred, N/A | AWS AI-DLC, `core/sensors/aidlc-traceability.md` |
| Thư mục tài liệu theo tính năng, tên có số thứ tự và mô tả | GitHub Spec Kit, `specs/NNN-feature-name/` |
| Commit theo `<loại>(<phạm vi>): <mô tả>`, phần chân theo dạng trailer | Conventional Commits 1.0.0; `git interpret-trailers` |
| Nhánh `<loại>/<mô tả>` | Conventional Branch 1.1.0 |
| Jira tự liên kết khi key viết hoa có trong tên nhánh, commit, tiêu đề PR | Atlassian, Reference issues in your development work |
| Tag test bắt đầu bằng `@`, không có khoảng trắng | Cucumber, Playwright, JUnit 5, pytest |
| Trường mở rộng của OpenAPI bắt đầu bằng `x-` | OpenAPI 3.1.1 |
| ADR đặt tên `NNNN-tieu-de.md` | MADR 4.0.0 |

## 2. Ba nguyên tắc

1. Mã tính năng là khoá gốc. Mọi thứ thuộc một tính năng mang mã tính năng trong tên, trong khoá `feature` của frontmatter, hoặc trong nhãn trên Jira. Agent bắt đầu tìm từ mã này.
2. Ngoài repo PO chỉ dùng mã đầy đủ. Mã ngắn như `US1`, `AC1.1` chỉ có nghĩa trong một intent và trùng dạng với mã của AWS AI-DLC, Spec Kit, Kiro; mã đầy đủ như `AC-APP-F012-01.1` là duy nhất trong toàn công ty nên tìm bằng `git grep` không lẫn.
3. Mã không đổi, tên thì đổi được. Tên file, tên màn, tiêu đề story có thể sửa; mã giữ nguyên. Agent tìm theo mã, không tìm theo tên hay đường dẫn.

## 3. Cú pháp của mã đầy đủ

Mọi mã đầy đủ chỉ dùng chữ hoa, chữ số, dấu chấm và gạch nối, nên dùng được làm tag test, giá trị trailer, nhãn Jira mà không cần đổi. Một biểu thức chính quy đọc được mọi mã đầy đủ:

```
\b(US|AC|BR|SCR|TC|NFR|TR|SC|Q)-([A-Z][A-Z0-9]*-F\d{3,})-(\d{2,3})(?:\.(\d+))?\b
```

Nhóm 1 là loại mã, nhóm 2 là mã tính năng, nhóm 3 là số thứ tự, nhóm 4 là số con nếu có. Mã trong KB của domain, như `BR-EDIT-07`, theo `domain-kb.md` và không khớp biểu thức này. Mã tính năng `<SP>-F<NNN>` có chữ F đứng trước số, nên khác dạng key issue của Jira là key dự án, gạch nối, số, như `LMS-123`.

## 4. Thư mục và tên file trong repo PO

| Thứ | Quy ước | Ví dụ |
|---|---|---|
| Intent | `intents/<YYMMDD>-<slug>/`, giống `intents/<YYMMDD>-<label>/` của AWS | `intents/261009-bao-cao-giai-doan-1/` |
| Artifact | `<giai đoạn>/<stage>/<artifact>.md`, tên artifact theo `^[a-z][a-z0-9-]*$` | `inception/prd/prd.md` |
| File thiết kế của team | `inception/ux-design/ux-design.md`, `inception/tech-design/tech-design.md`, `inception/test-design/test-design.md` | |
| Bản đã duyệt | `archive/<stage>/<artifact>-v<version>-<YYYYMMDD>.md` và tag git `<intent>/<artifact>-v<version>` | tag `261009-bao-cao-giai-doan-1/prd-v1.0` |
| Story List | `stories/story-list-prd-v<version>.csv` | `stories/story-list-prd-v1.1.csv` |

Slug viết chữ thường, không dấu, nối bằng gạch, không quá 64 ký tự. Team khác trỏ tới PRD bằng tag, nên luôn đọc đúng bản đã duyệt.

## 5. Khoá frontmatter dùng chung

Mọi tài liệu Markdown của một tính năng, ở repo PO hay repo của team, mở đầu bằng frontmatter có các khoá sau. Agent đọc các khoá này để biết tài liệu thuộc tính năng nào và dựng từ bản nào.

| Khoá | Ý nghĩa | Bắt buộc | Ví dụ |
|---|---|---|---|
| `feature` | Mã tính năng | Có | `APP-F012` |
| `artifact` | Loại tài liệu, chữ thường và gạch nối | Có | `tech-design` |
| `version` | Phiên bản `X.Y`; bản duyệt đầu là 1.0 | Có | `0.2` |
| `status` | `draft`, `approved` | Có | `draft` |
| `owner` | Người chịu trách nhiệm | Có với file thiết kế | `Bình` |
| `inputs` | Tài liệu và phiên bản đã đọc khi viết, dạng `<artifact>@<version>`; ngoài repo PO thêm mã tính năng phía trước | Có | `prd@1.0, ux-design@0.2`; ngoài repo PO: `APP-F012/prd@1.0` |
| `implements` | Mã đầy đủ mà tài liệu này đáp ứng, dùng cho tài liệu ngoài repo PO | Khuyến nghị | `US-APP-F012-01, BR-APP-F012-01.2` |

Khi PRD lên phiên bản mới, tài liệu nào có `inputs` trỏ bản cũ là tài liệu cần xem lại. `po-tools.py status` đã báo việc này cho ba file thiết kế; agent của team làm tương tự trong repo của mình.

## 6. Thiết kế giao diện

- Trang Figma của tính năng đặt tên `<mã tính năng> <Tên tính năng>`, ví dụ `APP-F012 Làm lại bài kiểm tra`.
- Frame của mỗi màn đặt tên bắt đầu bằng mã màn đầy đủ: `SCR-APP-F012-02 Trang kết quả`. Link ở bảng Danh sách màn của `ux-design.md` trỏ tới đúng frame.
- Gắn story Jira vào frame bằng plugin Jira của Figma Dev Mode; link Jira hiện ở mục Dev resources của frame.

Figma không có chuẩn đặt tên frame chính thức; quy ước này là của PO-Workflow, để agent tìm được frame từ mã màn.

## 7. Git: nhánh, commit, pull request

Nhánh: `<loại>/<JIRA-KEY>-<mô-tả>`. Loại theo Conventional Branch: `feat`, `fix`, `hotfix`, `release`, `chore`. Key Jira là key của story, viết hoa vì Jira chỉ nhận key viết hoa; đây là chỗ khác Conventional Branch, vốn yêu cầu chữ thường.

```
feat/LMS-123-lam-lai-bai-kiem-tra
```

Commit theo Conventional Commits; phạm vi là vùng code, không phải mã yêu cầu. Mã yêu cầu ghi ở trailer cuối thông điệp, cách thân bằng một dòng trống:

```
feat(quiz): cho phép làm lại bài kiểm tra

Giới hạn số lần làm lại theo cấu hình của khoá học.

Refs: LMS-123
Feature: APP-F012
Story: US-APP-F012-01
Implements: AC-APP-F012-01.1, AC-APP-F012-01.2, BR-APP-F012-01.2
```

| Trailer | Giá trị | Bắt buộc |
|---|---|---|
| `Refs` | Key Jira của story | Có |
| `Feature` | Mã tính năng | Có |
| `Story` | Mã US đầy đủ, khi commit thuộc một story | Có khi có story |
| `Implements` | Mã AC, BR, NFR đầy đủ mà commit làm hoặc sửa | Khuyến nghị |

Đọc lại bằng git: `git log --format='%h %(trailers:key=Implements,valueonly)'`. Pull request có key Jira trong tiêu đề và chép các trailer vào phần mô tả.

AWS AI-DLC không đọc thông điệp commit; nguồn gốc commit của AI-DLC lấy từ mã băm nội dung (`docs/reference/20-commit-provenance.md`). Trailer phục vụ Jira và agent của các team.

## 8. Test

Mỗi test tự động gắn tag mã AC đầy đủ mà nó kiểm. Test của một màn gắn thêm mã màn; test case có mã thì gắn thêm mã test case. Test case viết tay trên Jira ghi mã AC ở trường liên kết.

| Công cụ | Cách gắn |
|---|---|
| Cucumber, Gherkin | `@US-APP-F012-01` trên Feature; `@AC-APP-F012-01.1 @TC-APP-F012-001` trên Scenario |
| Playwright | `test('...', { tag: ['@AC-APP-F012-01.1', '@SCR-APP-F012-02'] }, ...)`; lọc bằng `--grep @AC-APP-F012-01.1` |
| JUnit 5 | `@Tag("AC-APP-F012-01.1")` |
| pytest | `@pytest.mark.req("AC-APP-F012-01.1")`, khai báo marker `req` và chạy với `--strict-markers` |

Mã test case theo `id-conventions.md`: `TC-<tính năng>-<NNN>`, ba chữ số như `TC-NNN` trong `testing-guide.md` của AWS. Nếu QA dùng Xray hoặc Zephyr Scale, hai công cụ này liên kết theo key Jira; gắn thêm tag của công cụ, như `@REQ_LMS-123` của Xray hay `@TestCaseKey=LMS-T12` của Zephyr Scale, bên cạnh tag mã AC.

## 9. API, Frontend, ghi chú trong code

- OpenAPI: `operationId` duy nhất, viết camelCase. Mỗi operation có trường mở rộng `x-requirements` liệt kê mã US, BR đầy đủ mà nó phục vụ. OpenAPI không có trường chuẩn cho việc này nên đây là quy ước riêng, theo luật trường mở rộng `x-`.
- Frontend: bảng Màn và component ở `tech-design.md` mục 5 là nơi nối mã màn với route và component. Storybook đặt `id` cố định trong meta khi story có thể đổi tên, để đường dẫn tới story không gãy.
- Ghi chú trong code: chỉ ghi mã business rule tại chỗ code kiểm rule đó, dạng `// BR-APP-F012-01.2: tối đa 3 lần làm lại`. Không ghi mã US, AC vào code; liên kết đó nằm ở trailer và file truy vết. Khi BR đổi, `git grep -n "BR-APP-F012-01.2"` ra đúng chỗ phải sửa.

## 10. File truy vết máy đọc

Team nào cần truy vết chi tiết thì ghi file theo đúng khuôn `traceability.json` của AWS AI-DLC, dùng mã đầy đủ, mỗi tính năng một file, ở `docs/features/<mã tính năng>-<slug>/traceability.json` trong repo của team. Thư mục này cũng chứa tài liệu kỹ thuật chi tiết của tính năng, giống `specs/NNN-feature-name/` của Spec Kit.

```json
{
  "stage": "code-generation",
  "feature": "APP-F012",
  "upstream_ids": ["AC-APP-F012-01.1", "BR-APP-F012-01.2"],
  "coverage": [
    { "id": "AC-APP-F012-01.1", "status": "OK", "target": "src/quiz/retake.ts" },
    { "id": "BR-APP-F012-01.2", "status": "OK", "target": "src/quiz/retake-policy.ts" }
  ],
  "reverse": []
}
```

Trạng thái chỉ dùng năm giá trị OK, GAP, ORPHAN, Deferred, N/A; OK có đích, Deferred và N/A ghi lý do ở `target`. Khoá `feature` là phần thêm của PO-Workflow; các khoá còn lại giữ nguyên tên của AWS để công cụ của AI-DLC đọc được. Phía Dev, `target` là đường dẫn file code hoặc test; phía QA, `target` là mã test case.

## 11. Agent làm gì khi PO đổi yêu cầu

1. Lấy phiên bản mới từ frontmatter của PRD đã gắn tag, hoặc từ tên Story List mới.
2. Lấy danh sách mã bị đổi: `po-tools.py stories` in story mới, story đổi và story bị bỏ so với Story List trước; dòng change request trong `decisions.md` ghi mã bị chạm.
3. Với mỗi mã, tìm nơi dùng: `git grep -n "<mã>"` trong repo của team; trailer `Implements` trong `git log`; tag test; `traceability.json`; frame Figma có tên bắt đầu bằng mã màn.
4. Tài liệu có `inputs` trỏ phiên bản cũ là tài liệu cần xem lại.
5. In danh sách file và test bị chạm cho người phụ trách quyết sửa.

## 12. Khi team dùng AWS AI-DLC, Spec Kit, Kiro hoặc OpenSpec

Các công cụ này đánh mã riêng trong một intent hoặc một spec và không đọc được mã đầy đủ: bộ kiểm truy vết của AWS chỉ nhận `US\d+\.\d+`, `AC\d+\.\d+\.\d+`, `BR\d+\.\d+`, `FR\d+`, `NFR\d+` (`core/tools/aidlc-sensor-traceability.ts`). Quy tắc nối: dòng nào có mã riêng của công cụ mà bắt nguồn từ yêu cầu của PO thì ghi mã đầy đủ trong ngoặc ngay sau, trên cùng dòng. Hai bên đều đọc được bằng biểu thức của mình, không cần bảng quy đổi riêng.

| Công cụ | Mã riêng | Cách ghi |
|---|---|---|
| AWS AI-DLC | `US1.1`, `AC1.1.1`, `BR1.1`, `FR1` | `US1.1 (US-APP-F012-01)`; `AC1.1.1 (AC-APP-F012-01.1)`; `BR1.1 (BR-APP-F012-01.2)` |
| GitHub Spec Kit | `FR-001`, `SC-001`, User Story N, task `T012 [US1]` | `FR-001 (BR-APP-F012-01.2)`; `User Story 1 (US-APP-F012-01)` |
| Kiro | Requirement 1, tiêu chí 1.1, task trỏ `_Requirements: 1.1_` | `1.1 (AC-APP-F012-01.1)` |
| OpenSpec | Không có mã số, yêu cầu nhận diện theo tiêu đề | `### Requirement: Giới hạn số lần làm lại (BR-APP-F012-01.2)` |

Tài liệu của PO tương ứng với tài liệu của các công cụ:

| PO-Workflow | AWS AI-DLC | Spec Kit | Kiro | OpenSpec |
|---|---|---|---|---|
| PRD: US, BR, AC | `requirements.md`, `stories.md` | `spec.md` | `requirements.md` | `specs/<capability>/spec.md` |
| `tech-design.md` | `domain-design/`, `contract-design/`, `construction/<unit>/functional-design/` | `plan.md`, `data-model.md`, `contracts/` | `design.md` | `design.md` |
| Unit of work ở `tech-design.md` mục 7 | `units-generation/unit-of-work.md` | `tasks.md` | `tasks.md` | `tasks.md` |
| `test-design.md` | `build-and-test/` | Kịch bản Given/When/Then trong `spec.md` | Tiêu chí chấp nhận trong `requirements.md` | `#### Scenario:` |
| Change request | Intent mới hoặc stage mở lại | Spec mới | Sửa spec | `changes/<change-id>/` |
