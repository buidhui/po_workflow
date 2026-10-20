# ADR 0003: Thiết kế của các team ở file riêng, chốt trên Decision Brief

| | |
|---|---|
| Trạng thái | Đã quyết, thay phần checkpoint của ADR 0002 |
| Ngày | 2026-10-20 |
| Người quyết định | PO phụ trách PO-Workflow |

## Bối cảnh

Luồng trước đó đặt buổi checkpoint trên HLD Brief ở 2.41, trước khi viết PRD: PO viết mục 1 tới 7, Design PIC, Tech PIC, QA PIC ghi định hướng ở mục 8, 9, 10 và ký. Khi chạy thật, các team không đưa ra được Technical Design, Test Design và UI/UX Design từ HLD Brief; họ cần PRD chi tiết. Sau khi có ba bản thiết kế, nếu gộp tất cả vào PRD thì PRD quá dài để mang đi họp và chốt.

Ba cách đã xét:
1. Các team viết thẳng vào các mục thiết kế trong PRD, sau đó AI tổng hợp một file ngắn để họp.
2. Mỗi team viết một file riêng; AI của PO gộp vào PRD và chỉnh tài liệu; sau đó tổng hợp một file ngắn để họp.
3. Mỗi team viết một file riêng; PRD giữ là tài liệu yêu cầu; AI đối chiếu ba file với PRD và viết Decision Brief để họp; thay đổi PRD đi qua change request.

## So với AWS AI-DLC 2.11

| Điểm | AWS | Quyết định |
|---|---|---|
| Thiết kế nằm ở đâu | Mỗi vai một artifact riêng trong thư mục stage: `refined-mockups/` ở 2.5, `domain-design/` ở 2.6, `contract-design/` ở 2.8, `construction/<unit>/functional-design/` ở 3.1, `build-and-test/` ở 3.6. Requirements không chứa thiết kế | `inception/ux-design/`, `inception/tech-design/`, `inception/test-design/`, PRD không chứa thiết kế |
| Nhiều vai cùng góp | Mỗi người ghi file đóng góp riêng để làm song song; người chủ gộp và chịu trách nhiệm bản cuối; bất đồng trích nguyên văn ở gate (`stage-protocol-collaborators.md`) | Mỗi team một file, có mục Ý kiến về PRD với lập trường Đồng ý, Đề xuất sửa, Phản đối; Phản đối chép nguyên văn vào Decision Brief |
| Tài liệu trình người quyết định | Decision brief do công cụ dựng trước gate: kết quả, finding, hệ quả của lựa chọn (`aidlc-review-brief.ts`) | Decision Brief, AI viết, tối đa 1.500 từ cho phần tổng hợp, kèm bảng Ký |
| Design, Dev, QA góp ý ở 2.4 | Chỉ khi bật chế độ cộng tác; mặc định tắt trừ scope enterprise | Bỏ bước PIC xem thẻ US; các team đọc PRD chi tiết một lần ở 2.43 |
| Test design trước khi code | Không có; quality agent kiểm tính kiểm thử được của AC ở 2.4 và viết hướng dẫn test ở 3.6 | `test-design.md` trước khi code, là phần thêm; ý kiến về AC nằm ở đây |

## Quyết định

Chọn cách 3.
- Bỏ stage 2.41 HLD Brief. Thêm stage 2.43 Design Alignment sau PRD, chạy ở profile M và L.
- Ba team viết `ux-design.md`, `tech-design.md`, `test-design.md` từ PRD đã duyệt, mỗi team chỉ sửa file của mình. Ngoài khung file tạo lúc giao việc, AI của PO không viết và không sửa ba file này.
- AI đối chiếu ba file với PRD, bằng máy và bằng đọc hiểu, và viết Decision Brief. Họp trên Decision Brief; ba PIC ký. Thay đổi yêu cầu đi qua change request trên PRD.
- Story List chỉ sinh sau khi 2.43 được duyệt. Mã màn `SCR` lấy từ `ux-design.md`.

## Hệ quả

- PRD chỉ đổi khi yêu cầu đổi. Không lặp lại sự cố thiết kế kỹ thuật ghi đè làm mất ràng buộc nghiệp vụ trong PRD, như đã gặp khi Dev ghi technical design thẳng vào PRD.
- Không có xung đột git giữa bốn bên trên một file dài.
- Mất buổi thống nhất định hướng trước PRD. Lệch hướng giữa PRD và thiết kế sẽ lộ ra ở 2.43 và phải sửa PRD qua change request; chi phí này thấp hơn chi phí sửa sau khi Dev đã làm, vì Story List chưa sinh. PO giảm số lần sửa bằng cách đánh dấu `[đề xuất]` và OQ gắn PIC cho điểm chưa chắc trong PRD.
- Intent đang làm dở ở 2.41 chuyển bằng `po-tools.py migrate`: bản HLD Brief vào `archive/hld-brief/`, stage chuyển sang 2.43.
