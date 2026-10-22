# 1.7 Approval & Handoff

| | |
|---|---|
| Stage | 1.7 Approval & Handoff |
| Slug | approval-handoff |
| Thư mục | `ideation/approval-handoff` |
| Phase | ideation |
| Plugin | (stage gốc AWS) |
| Lệch so với AWS | AWS do delivery agent dẫn, sinh initiative-brief và decision-log; ở đây product dẫn, decision log là `decisions.md` của intent, chỉ chạy ở profile L, không đọc đầu ra của 1.3, 1.5, 1.6 |
| Execution | always ở L |
| Lead | product |
| Produces | `ideation/approval-handoff/initiative-brief.md` · `approval-handoff-questions.md` · `verification/phase-check-ideation.md` |
| Consumes | `intent-statement.md`, `scope-document.md` (bắt buộc) · `competitive-analysis.md` (tuỳ) · `decisions.md` |
| Requires | scope-definition |
| Profiles | L |
| Reviewer | none |
| Summary confirmation | off, chỉ ba câu duyệt |
| Template | `engine/templates/initiative-brief.md` |
| Checklist | `engine/verification/approval-handoff.md` |

Chạy theo `engine/protocol/stage-protocol.md`.

## Mục đích
Gói mọi thứ của Ideation thành một trang để quyết đi tiếp hay dừng. AWS: stage 1.7, có lựa chọn Reject Initiative.

## Ask
Ba câu, không cần tóm tắt xác nhận:
1. Stakeholder đã thống nhất vấn đề và phạm vi chưa. Ai chưa.
2. Rủi ro và giả định lớn nhất đã được nêu và chấp nhận chưa.
3. Có nguồn lực và mốc cho đợt này chưa.

## Generate
`initiative-brief.md`, một trang: vấn đề và mục tiêu; phạm vi biên; Unit và ưu tiên; rủi ro và giả định lớn; quyết định đã đưa ra từ `decisions.md`; khuyến nghị go hay no-go kèm điều kiện. Tài liệu bàn giao: không thẻ nguồn, mã kèm nội dung, không viết tắt.
Kiểm ranh giới phase Ideation sang Inception theo `engine/templates/phase-check.md`, ghi `verification/phase-check-ideation.md`: mọi objective có hạng mục phục vụ; mọi Unit truy về objective; Out không mâu thuẫn In; OQ chặn đã đóng. Không đạt thì sửa stage tương ứng trước khi mở gate.

## Gate
Lựa chọn: Approve sang Inception · Request Changes · Reject Initiative kết thúc intent, ghi lý do, `state.md` chuyển Archived. Brief ngắn nên trình nguyên văn.

Stage kế: 2.3.
