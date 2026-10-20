# 1.4 Scope Definition

| | |
|---|---|
| Stage | 1.4 Scope Definition |
| Slug | scope-definition |
| Thư mục | `ideation/scope-definition` |
| Phase | ideation |
| Plugin | (stage gốc AWS) |
| Lệch so với AWS | AWS sinh scope-document và intent-backlog riêng, kèm value stream map; ở đây backlog là bảng Unit trong scope-document, AWS gọi là proto-Unit, không có value stream map. AWS cần 1.3 Feasibility chạy trước; ở đây không chạy 1.3 |
| Execution | always ở M và L |
| Lead | product |
| Produces | `ideation/scope-definition/scope-document.md` · `scope-definition-questions.md` |
| Consumes | `intent-statement.md` (bắt buộc) · `competitive-analysis.md` (tuỳ) |
| Requires | intent-capture |
| Profiles | M, L |
| Reviewer | none |
| Summary confirmation | required |
| Template | `engine/templates/scope-document.md` |
| Checklist | `engine/verification/scope-definition.md` |
| Knowledge | `domain/domain.md` mục 3 (vùng KB chưa phủ) và mục 4 phần 1.4 · product: `prioritization-frameworks.md` §MoSCoW, `product-guide.md` §MVP Definition Criteria |

Chạy theo `engine/protocol/stage-protocol.md`.

## Mục đích
Vạch biên: làm gì, không làm gì, để sau. Chia nhu cầu thành Unit, là hạng mục của intent backlog, nhóm theo giá trị và ưu tiên; AWS gọi là proto-Unit. Dev tham khảo khi chia Unit of work ở 2.7 nhưng không bắt buộc chia theo đó. AWS: stage 1.4.

## Load
intent-statement; vùng KB chưa phủ theo `domain.md` mục 3; `decisions.md`.

## Ask
1. Phạm vi nhỏ nhất vẫn có giá trị là gì.
2. Hạng mục nào Must, Should, Could, Won't.
3. Phụ thuộc giữa các hạng mục.
4. Ưu tiên theo rủi ro trước, giá trị trước, hay phụ thuộc trước.
5. Mốc cứng nào gắn với hạng mục nào.
6. Thứ người đọc dễ tưởng là có mà không làm. Thứ từng nằm trong yêu cầu nhưng sau đó bị loại.
7. Hạng mục nào trùng tính năng đã có: tra KB, nêu mã, hỏi mở rộng hay làm mới. Vùng KB chưa phủ thì ghi `❓PO`.

## Generate
`scope-document.md` theo template: In, Out, Potential mỗi dòng một câu kèm lý do và nguồn; constraints; intent backlog là bảng Unit `U1`... với tên, mục đích, portal, MoSCoW, phụ thuộc, trùng tính năng có sẵn hay không; thứ tự gợi ý kèm lý do; mốc cứng; Assumptions & Open Questions.
Chia Unit theo bốn quy tắc: theo cơ chế, không theo màn hình; tìm hạng mục nền; tách hạng mục chạm mọi thứ như phân quyền, bật tắt, lịch sử; phụ thuộc một chiều. Định nghĩa hết, kể cả Won't, để Impact Analysis quét đúng.

## Gate
- Profile M: gate chung với 1.1. Thông điệp hoàn thành gộp intent-statement và scope-document. Request Changes nêu rõ sửa artifact nào.
- Profile L: gate riêng.

Stage kế: 1.7 ở L; 2.3 ở M.
