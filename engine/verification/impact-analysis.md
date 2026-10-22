# Checklist: 2.31 Impact Analysis

## Related Features Map
- [ ] **[BLOCK]** PO đã xác nhận bản đồ: đủ, sót, không liên quan. `❓PO` đã xử lý, không trôi vào matrix
- [ ] Field, màn Existing được nhận diện ở stage này, không bị coi là mới ở stage sau

## Nguồn
- [ ] KB theo bản đồ trong `domain.md` đã tra: module bị chạm, data model, sự kiện, API surface, định hướng
- [ ] **[BLOCK]** Chạm dữ liệu: schema gốc theo `domain.md` mục 2 đã đọc lại, không dựa bản chép
- [ ] API spec đã tra cho field

## Framework
- [ ] **[BLOCK]** Đủ 5 bước đúng thứ tự
- [ ] **[BLOCK]** Đủ 12 vùng. Vùng không ảnh hưởng có lý do
- [ ] Hidden được xét
- [ ] Từ ba vùng bị ảnh hưởng có sơ đồ phụ thuộc vẽ từ bảng Current Situation, vùng High được đánh dấu
- [ ] Conflict 4 chiều, **[BLOCK]** được escalate, không tự resolve
- [ ] Bidirectional có cả chiều Old sang New
- [ ] Coverage đủ boundary, exception, shared entity, side effect. Shared entity dễ vỡ trong `domain.md` mục 4 phần 2.31 đã kiểm
- [ ] Transition đủ Data, Compatibility, Cutover
- [ ] Tenant đủ 4 câu

## Giao
- [ ] Mỗi dòng matrix có severity và nguồn
- [ ] FR, NFR phát sinh đã bổ sung vào requirements với thẻ `[2.31]`, version tăng, DEC ghi
- [ ] **[BLOCK]** Phụ lục nguồn đã đọc, kể cả chưa tra được
