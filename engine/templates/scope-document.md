---
intent: <slug>
artifact: scope-document
version: 0.1
status: draft
inputs: <artifact đầu vào@version, ví dụ requirements@1.0; stage đầu tiên ghi none>
---
# Scope: <Tên tính năng>

## In scope
| # | Hạng mục | Vì sao | Nguồn |
|---|---|---|---|

## Out of scope
| # | Không làm | Vì sao: chưa yêu cầu, chờ tính năng khác, đã cân nhắc và loại, thuộc tính năng khác | Nguồn |
|---|---|---|---|

## Potential scope <!-- tuỳ chọn -->
| # | Để sau | Điều kiện để làm | Nguồn |
|---|---|---|---|

## Constraints
- Nghiệp vụ: <...> [nguồn]
- Tenant và hằng số: <cứng hay cấu hình> [KB]
- Tích hợp: <...>
- Dữ liệu cũ: <...>

## Intent backlog, Units
| Unit | Tên | Mục đích | Portal | MoSCoW | Phụ thuộc | Trùng tính năng có sẵn? | Nguồn |
|---|---|---|---|---|---|---|---|
| U1 | | | | Must | | <mã KB hoặc "không"> | |

Thứ tự gợi ý: <U1, U2... theo rủi ro, giá trị, hay phụ thuộc, kèm lý do> [Q4]
<Tuỳ chọn, từ hai Unit: sơ đồ luồng giá trị, các bước từ nhu cầu của người dùng tới kết quả, ghi Unit phục vụ từng bước; AWS gọi là value stream map. Theo `engine/standards/diagrams.md`.>
Mốc cứng: <...> [Q5]

## Assumptions & Open Questions
| # | Nội dung | Loại | Chặn | Owner |
|---|---|---|---|---|
