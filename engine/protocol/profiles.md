# Workflow Profiles

Profile quyết định stage nào chạy, nghi thức nào bật, Depth bao nhiêu. Tương đương "scope" trong engine AWS, phía người dùng AWS gọi là workflow profile. Không dùng chữ Scope vì đã dùng cho phạm vi tính năng.

## Ba profile

| Profile | Độ lớn và độ phức tạp | Stage | Depth | Summary confirmation | Reviewer | Learnings | Gate |
|---|---|---|---|---|---|---|---|
| **S** | Đúng tất cả: chạm 1 màn · không đổi data model · không đổi rule hiện có · không chạm module khác · không chạm Hidden · không tích hợp ngoài · không migration | 2.3, 2.42 | Minimal | Chỉ Field Intake | 2.42 | Tắt | 2 |
| **M** | Chạm tối đa 2 module · thêm field nhưng không đổi quan hệ bảng · không conflict · đã rõ hướng giải | 1.1 và 1.4 duyệt chung, 2.3, 2.31, 2.4, 2.42, 2.43 | Standard | Bật | 2.3, 2.4, 2.42 | Bật | 6 |
| **L** | Một trong số: từ 3 module · đổi data model hoặc quan hệ · conflict với rule hiện có · chạm Hidden · nhiều hướng giải · tích hợp ngoài hoặc job nền · migration dữ liệu cũ · không hoàn tác được | 1.1, 1.2 nếu PO yêu cầu, 1.4, 1.7, 2.3, 2.31, 2.32 nếu có nhiều hướng, 2.4, 2.42, 2.43 | Standard, Comprehensive khi PO yêu cầu | Bật | 1.1, 2.3, 2.4, 2.42 | Bật | 8 đến 10 |

Depth nói mức chi tiết của artifact, không nói số câu hỏi. Số câu hỏi do logic câu chặn quyết định.

## Depth
Theo định nghĩa của AWS AI-DLC, `docs/guide/05-scopes-and-depth.md`. Template đánh dấu mục tuỳ chọn bằng `<!-- tuỳ chọn -->` ở cuối dòng heading; mục không có dấu là bắt buộc.

| Depth | Artifact | Mục bắt buộc | Mục tuỳ chọn |
|---|---|---|---|
| Minimal | Một đến hai trang | Viết ngắn, chỉ điều đã quyết | Bỏ hẳn |
| Standard | Đủ để người đọc không phải hỏi lại | Viết đủ | Viết khi có nội dung thật |
| Comprehensive | Đầy đủ, kèm phân tích và phương án | Viết đủ | Viết hết, mục không áp dụng ghi lý do |

Depth đổi được ở mọi gate. Đổi thì ghi vào `state.md` và một dòng DEC; áp từ stage kế tiếp.

## Danh sách stage
| Mã | Stage | Nguồn | Điều kiện |
|---|---|---|---|
| 1.1 | Intent Capture & Framing | AWS | Luôn chạy ở M, L |
| 1.2 | Market Research | AWS | Khi PO yêu cầu so với sản phẩm khác |
| 1.4 | Scope Definition | AWS | Luôn chạy ở M, L |
| 1.7 | Approval & Handoff, Initiative Brief | AWS | Luôn chạy ở L |
| 2.3 | Requirements Analysis | AWS | Luôn chạy |
| 2.31 | Impact Analysis | PO-Workflow thêm | Luôn chạy ở M, L |
| 2.32 | Solution Options | PO-Workflow thêm | Khi có từ hai hướng giải, hoặc PO chưa có hướng |
| 2.4 | User Stories | AWS | Luôn chạy ở M, L |
| 2.42 | PRD Generation | PO-Workflow thêm | Luôn chạy |
| 2.43 | Design Alignment | PO-Workflow thêm | Luôn chạy ở M, L, sau khi PRD được duyệt |

Stage AWS ngoài phạm vi PO, chỉ để mapping: 1.3, 1.5, 1.6, 2.1, 2.2, 2.5, 2.6, 2.7, 2.8, 2.9 và toàn bộ Construction, Operation.

## Quy tắc
1. Chọn profile ở `/new-intent` sau khi quét nhanh KB, API spec, schema theo `domain.md`. Echo một dòng trước khi chạy: *"Profile M: 7 stage, 6 gate, Depth Standard, reviewer ở 3 stage, summary confirmation bật. Đồng ý không?"* PO có quyền đổi.
2. Nghi ngờ giữa hai profile thì chọn profile lớn hơn.
3. Phát hiện giữa chừng dấu hiệu vượt profile: nói ngay, tại gate gần nhất đưa lựa chọn Add [stage]. Thêm một stage thì chuyển dòng đó về `[ ]`, kèm lý do và một dòng DEC. Đổi hẳn profile thì PO quyết và AI chạy `po-tools.py profile`: stage của profile mới chưa có được thêm `[ ]`, stage ngoài profile chưa làm thành `[S]`.
4. PO muốn tắt một nghi thức cho intent này ("intent này không cần reviewer"): chạy `po-tools.py switch <intent> reviewer off --words "<lời PO>"`. Lệnh sửa dòng Switches của `state.md` và ghi DEC nguyên văn. Áp cho intent này, intent sau về mặc định.
5. S vẫn phải qua Field Intake ở 2.42. Đây là bước dễ sai nhất kể cả với yêu cầu nhỏ.
6. Phase check Ideation: profile L chạy ở 1.7; profile M không có 1.7 nên chạy ở gate chung của 1.1 và 1.4; profile S không có Ideation nên không chạy.
7. Phase check Inception: profile M, L chạy ở gate 2.43; profile S chạy ở gate 2.42.
