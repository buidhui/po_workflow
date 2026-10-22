# 2.31 Impact Analysis

| | |
|---|---|
| Stage | 2.31 Impact Analysis |
| Slug | impact-analysis |
| Thư mục | `inception/impact-analysis` |
| Artifact chính | `impact-matrix.md` |
| Phase | inception |
| Plugin | `po-workflow` |
| Lệch so với AWS | Stage thêm của PO-Workflow, không có trong AWS. Đánh số thập phân để chen giữa stage gốc; cơ chế plugin của AWS chỉ cho đánh số sau stage cuối của phase |
| Execution | always ở M và L |
| Lead | product |
| Produces | `inception/impact-analysis/related-features-map.md` · `impact-matrix.md` · `impact-analysis-questions.md` |
| Consumes | `requirements.md` (bắt buộc) · `scope-document.md` · `intent-statement.md` · KB và nguồn sống theo `domain.md` mục 2, 3 và mục 4 phần 2.31 |
| Requires | requirements-analysis |
| Profiles | M, L |
| Reviewer | none |
| Summary confirmation | required, dưới dạng PO xác nhận Related Features Map |
| Template | `engine/templates/related-features-map.md` · `engine/templates/impact-matrix.md` |
| Checklist | `engine/verification/impact-analysis.md` |

Chạy theo `engine/protocol/stage-protocol.md`.

## Mục đích
Biết tính năng mới chạm gì trên hệ đang chạy trước khi chọn cách làm. Năm việc: phát hiện conflict với rule hiện có; bổ sung FR, NFR do tác động qua lại; phủ đủ case; transition để golive an toàn; kiểm chiều tenant. Plugin stage của repo, AWS không có stage tương đương ở tầng nghiệp vụ.

## Bước A, Related Features Map, thay cho bước Ask
Chủ động quét requirements, KB, schema và API spec theo `domain.md`, dựng bảng: Hệ · Tính năng, Module, Entity, Endpoint · New hay Existing · Nguồn · Ghi chú. Bao quát module, màn, entity, API và job, role, rule hiện tại, NFR, mail event, tính năng Hidden. Chưa chắc thì `❓PO`.
Bảng này là Consolidated Summary của stage. Trình bảng, hỏi PO: đủ chưa, sót gì, dòng nào không liên quan, `❓PO` nào trả lời được. Chỉ sang bước B khi PO xác nhận. Nhận ra dễ hơn nhớ ra: PO soát một bản nháp thay vì kể từ đầu.
KB mỏng ở vùng này thì hỏi PO seed danh sách hệ liên quan trước, AI mở rộng sau. Câu hỏi khác chỉ khi cần giả định về hệ cũ hay dữ liệu cũ.

## Bước B, Impact Matrix
Theo đúng thứ tự:
1. Current Situation: đọc để tìm dependency, chưa cần hiểu hết feature. Module, entity và field, rule, process, permission, integration, mail event, Hidden. Từ ba vùng bị ảnh hưởng trở lên thì vẽ sơ đồ phụ thuộc từ bảng, tô màu vùng High, theo `engine/standards/diagrams.md` mục 4. Entity có vòng đời trạng thái bị chạm thì dẫn sơ đồ trạng thái trong KB nếu có.
2. Desired Situation: từ requirements.
3. Impact Matrix 12 vùng: business process, module, screen và report, data, API, role, business rule, NFR, notification và email, reporting, test, release. Mỗi dòng có severity và nguồn. Vùng không ảnh hưởng vẫn ghi lý do. Vùng KB chưa phủ ghi `❓PO`.
   - 3a Conflict bốn chiều: rule, process, data, permission. Phát hiện thì escalate cho PO quyết, không tự resolve.
   - 3b Bidirectional: New sang Old và Old sang New, chiều sau hay bị bỏ.
   - 3c Coverage: boundary, exception, shared entity, side effect. Shared entity dễ vỡ của hệ lấy từ `domain.md` mục 4 phần 2.31.
4. Transition: data, compatibility, cutover.
5. Tenant: các câu kiểm chiều tenant ghi trong `domain.md` mục 4 phần 2.31.
FR, NFR phát sinh: ghi trong impact-matrix, sau đó bổ sung vào `requirements.md` dưới dạng FR mới với thẻ `[2.31]`, tăng version requirements, ghi DEC. Không sửa FR đã duyệt.
Phụ lục nguồn đã đọc, kể cả "chưa tra được", bắt buộc.

## Gate
Trình: tóm tắt theo severity; conflict cần PO quyết, mỗi conflict một DEC; FR, NFR bổ sung; coverage gap; transition; điểm đóng cứng tenant tăng thêm; risk; OQ; phụ lục nguồn.
Stage kế: 2.32 khi có từ hai hướng giải hoặc PO chưa có hướng. Không thì ghi 2.32 `[S]` kèm lý do và sang 2.4.
