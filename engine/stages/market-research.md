# 1.2 Market Research

| | |
|---|---|
| Stage | 1.2 Market Research |
| Slug | market-research |
| Thư mục | `ideation/market-research` |
| Phase | ideation |
| Plugin | (stage gốc AWS) |
| Lệch so với AWS | AWS sinh competitive-analysis, market-trends, build-vs-buy; ở đây chỉ competitive-analysis. AWS chạy khi có định vị thị trường hoặc cân nhắc build-vs-buy; ở đây chạy khi PO yêu cầu |
| Execution | conditional: PO yêu cầu so với sản phẩm khác, hoặc 1.1 cho thấy cách làm chuẩn trên thị trường ảnh hưởng tới phạm vi |
| Lead | product |
| Produces | `ideation/market-research/competitive-analysis.md` · `market-research-questions.md` |
| Consumes | `intent-statement.md` (bắt buộc) |
| Requires | intent-capture |
| Profiles | L |
| Reviewer | none |
| Summary confirmation | required |
| Template | `engine/templates/competitive-analysis.md` |
| Checklist | `engine/verification/market-research.md` |
| Knowledge | `engine/knowledge/market-research-methods.md` §Competitive Analysis Framework, §Build vs Buy Assessment |

Chạy theo `engine/protocol/stage-protocol.md`.

## Mục đích
Xem sản phẩm khác giải bài toán này thế nào, để đặt tên khái niệm đúng, không phát minh lại, và biết đâu là chuẩn người dùng đã quen. AWS: stage 1.2.

## Ask
1. So với sản phẩm nào, tối đa ba. Mặc định lấy danh sách trong `domain.md` mục 4 phần 1.2.
2. Xem khía cạnh nào: mô hình khái niệm, thuật ngữ, luồng chính, giới hạn, cách tích hợp.
3. Quyết định nào phụ thuộc vào kết quả này. Không có thì ghi `[S]` và không chạy.

## Generate
`competitive-analysis.md`: mỗi sản phẩm một mục ngắn; bảng so sánh theo khía cạnh đã chọn; thuật ngữ nên dùng; điểm nên áp dụng và lý do phù hợp với sản phẩm; điểm không áp dụng và lý do; đối chiếu với yêu cầu hiện tại, điểm làm thay đổi phạm vi hay rule; nguồn kèm link và ngày đọc. Trích đúng, không suy diễn tính năng từ tên menu.
Thu thập: nguồn nào chặn tải tự động thì dùng cách ghi trong `domain.md` mục 4 phần 1.2. Bài đã lấy lưu nguyên văn vào `inputs/` để tra lại.

## Gate
Trình bảng so sánh và danh sách điểm nên áp dụng. Stage kế: 1.4.
