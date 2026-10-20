---
intent: <slug>
artifact: decision-brief
feature: <mã tính năng>
version: 0.1
status: draft
inputs: <prd@1.0, ux-design@0.1, tech-design@0.1, test-design@0.1>
---
# [Decision Brief] <Tên tính năng>

<Tài liệu cho buổi họp chốt ở 2.43. Chỉ ghi điểm cần người quyết hoặc cần cả nhóm biết; không chép lại PRD hay thiết kế. Mục 1 đến 9 do AI viết, không quá 1.500 từ. Xoá dòng hướng dẫn khi viết.>

## 1. Tóm tắt
<Ba đến năm dòng: tính năng làm gì, PRD bản nào, ba bản thiết kế bản nào, mốc cứng, số điểm cần quyết.>

## 2. Điểm cần quyết
| # | Vấn đề | Ai nêu | Lựa chọn và hệ quả | Đề xuất |
|---|---|---|---|---|

## 3. Đề xuất sửa PRD
| # | Mã trong PRD | Đề xuất | Ai đề xuất | PO quyết |
|---|---|---|---|---|

## 4. Mâu thuẫn giữa các thiết kế <!-- tuỳ chọn -->
| # | Giữa | Nội dung | Đề xuất xử lý |
|---|---|---|---|

## 5. Độ phủ
<Kết quả `po-tools.py check` của stage: US có giao diện chưa có màn, AC chưa có trong kế hoạch test, US chưa có trong thiết kế kỹ thuật. Không còn thì ghi "Đủ".>

## 6. Phụ thuộc và thứ tự làm
| Việc | Team | Phụ thuộc | Mốc |
|---|---|---|---|

## 7. Độ lớn so với mốc
<Ước lượng của Tech PIC theo Unit of work, so với mốc cứng ở scope-document. Vượt mốc thì nêu lựa chọn: cắt phạm vi, dời mốc, tách đợt.>

## 8. Rủi ro
<Mã `RK<n>` của sổ rủi ro trong `decisions.md`; rủi ro mới nêu ở buổi họp thì thêm vào sổ.>
| RK | Rủi ro | Ai nêu | Cách giảm | Chấp nhận |
|---|---|---|---|---|

## 9. Ý kiến phản đối
<Chép nguyên văn từng ý kiến Phản đối còn lại sau khi xử lý, kèm tên người nêu. Không có thì ghi "Không có".>

## 10. Ký
| Vai | Người | Trạng thái | Ngày | Ghi chú |
|---|---|---|---|---|
| Design PIC | | Chưa xem | | |
| Tech PIC | | Chưa xem | | |
| QA PIC | | Chưa xem | | |

Trạng thái: Chưa xem, Có ý kiến, Đồng ý, Yêu cầu sửa.
