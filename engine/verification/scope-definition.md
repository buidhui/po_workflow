# Checklist: 1.4 Scope Definition

## Phạm vi
- [ ] **[BLOCK]** Tách đủ In, Out, Potential. Mỗi dòng một câu kèm lý do và nguồn
- [ ] Out of scope có nội dung thật, gồm thứ người đọc dễ tưởng là có và thứ từng bị loại
- [ ] Hạng mục trùng tính năng có sẵn đã tra KB, nêu mã, quyết định mở rộng hay làm mới
- [ ] Vùng KB chưa phủ ghi `❓PO`, không kết luận

## Units
- [ ] **[BLOCK]** Mọi hạng mục In scope thuộc một Unit. Định nghĩa cả Won't
- [ ] Chia theo cơ chế, không theo màn hình. Có hạng mục nền. Hạng mục chạm mọi thứ tách riêng
- [ ] Phụ thuộc một chiều, không có vòng
- [ ] Mỗi Unit có MoSCoW, portal, nguồn
- [ ] Must không kéo theo Could hoặc Won't. MVP vẫn có xử lý lỗi cơ bản và đạt NFR tối thiểu về bảo mật, toàn vẹn dữ liệu
- [ ] Có mốc cứng thì phạm vi Must làm kịp mốc theo ước lượng thô, hoặc đã nêu rủi ro trễ mốc; AWS gọi là scope-vs-timeline validation

## Nguồn và câu hỏi
- [ ] **[BLOCK]** Bảng Độ phủ của questions file có mọi chủ đề trong mục Ask; mỗi dòng có nguồn đã trả lời hoặc câu hỏi
- [ ] **[BLOCK]** Mọi câu đã có câu trả lời; câu trả lời mơ hồ, mâu thuẫn đã được hỏi tiếp
- [ ] **[BLOCK]** Thẻ nguồn ở mọi khối. Assumptions & Open Questions có
- [ ] Câu chặn đã trả lời. Câu trả lời nguyên văn
- [ ] Profile M: gate chung với 1.1, thông điệp gộp hai artifact
