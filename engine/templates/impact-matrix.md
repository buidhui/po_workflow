---
intent: <slug>
artifact: impact-matrix
version: 0.1
status: draft
inputs: <artifact đầu vào@version, ví dụ requirements@1.0; stage đầu tiên ghi none>
---
# Impact Matrix: <Tên tính năng>

| | |
|---|---|
| Nguồn input | `requirements.md` v<N> · `related-features-map.md` · KB · schema · API spec, theo `domain.md` |
| Ngày | |

Bản phân tích nội bộ. Kết quả chảy vào `stories.md`, PRD mục Data Field, Out of scope, và vùng hồi quy trong `test-design.md` ở 2.43.

## 1. Summary
<Ba đến năm dòng: ảnh hưởng tới đâu, vùng nào rủi ro nhất, conflict nào phải quyết.>

| | Số lượng |
|---|---|
| Vùng bị ảnh hưởng High, Medium, Low | |
| Conflict cần PO quyết | |
| FR, NFR bổ sung | |
| Coverage gap | |
| Điểm đóng cứng tenant tăng thêm | |

## 2. Current Situation, Dependency Map
| Loại | Mục | Nguồn | Ghi chú |
|---|---|---|---|
| Module, Feature | | KB `0X §Y` | |
| Data, Entity, Field | | file data model · bảng `<tên>` | |
| Business rule | | `BR-XXX-01`, `KB-XXX-01` | |
| Process | | | |
| Permission | | file phân quyền theo `domain.md` · bảng rule | |
| Integration, Consumer | | file API surface | |
| Sự kiện, mail | | file sự kiện · mail số N | đang bật hay tắt |
| Tính năng Hidden bị chạm | | index KB mục Trạng thái | |

<Từ ba vùng bị ảnh hưởng trở lên: sơ đồ phụ thuộc, `flowchart LR`, mỗi thành phần trong bảng trên một nút, mũi tên theo quan hệ phụ thuộc, nút thuộc vùng High tô màu. Theo `engine/standards/diagrams.md` mục 4.>

## 3. Desired Situation
<Từ requirements: tính năng mới làm gì, process mới ra sao.>

## 4. Impact Matrix, 12 vùng
| Mức | Nghĩa |
|---|---|
| High | Đổi hành vi hiện tại, hoặc hỏng dữ liệu, luồng nếu làm sai |
| Medium | Phải sửa nhưng không đổi hành vi hiện tại |
| Low | Chỉ thêm mới, không chạm cái cũ |

| # | Vùng | Bị ảnh hưởng? | Mô tả | Severity | Nguồn |
|---|---|---|---|---|---|
| 1 | Business process | | | | |
| 2 | Module, function | | | | |
| 3 | Screen, report | | | | |
| 4 | Data | | | | |
| 5 | API | | | | |
| 6 | Role, permission | | | | |
| 7 | Business rule | | | | |
| 8 | NFR | | | | |
| 9 | Notification, email | | | | file sự kiện |
| 10 | Reporting | | | | |
| 11 | Test | | | | |
| 12 | Release | | | | |
Vùng không bị ảnh hưởng vẫn ghi lý do. Vùng KB chưa phủ ghi `❓PO`.

## 5. Conflict, 4 chiều: rule, process, data, permission
| # | Chiều | Conflict | Hiện tại | Mới | Ai quyết |
|---|---|---|---|---|---|
| CF-1 | | | | | PO |

## 6. Bidirectional, FR và NFR còn thiếu
| # | Chiều New sang Old, Old sang New | Phát hiện | FR, NFR bổ sung | Đã thêm vào requirements? |
|---|---|---|---|---|
| BI-1 | | | | |

## 7. Coverage gaps: boundary, exception, shared entity, side effect
| # | Loại | Case chưa định nghĩa | FR bổ sung |
|---|---|---|---|
| CG-1 | | | |

## 8. Transition <!-- tuỳ chọn -->
| Loại | Nội dung |
|---|---|
| Data | migration, backfill, dữ liệu cũ |
| Compatibility | bản cũ và mới chạy song song được không |
| Cutover | thứ tự bật, rollback, ẩn hiện khi golive |

## 9. Tenant, theo câu hỏi trong `domain.md` mục 4 phần 2.31 <!-- tuỳ chọn -->
| Câu hỏi | Trả lời | Xử lý |
|---|---|---|
| Có nhúng thêm logic riêng một tenant vào code không | | |
| Có hằng số cứng mới không | | cứng hay cấu hình |
| Bảng mới có `tenant_id` không | | |
| Enum mới do hệ thống hay tenant định nghĩa | | |

## 10. Risk
| # | Risk | Mức | Giảm nhẹ |
|---|---|---|---|

## 11. Assumptions & Open Questions
| # | Nội dung | Loại | Chặn | Owner |
|---|---|---|---|---|

## 12. Nguồn đã đọc
| Nguồn | Cụ thể |
|---|---|
| KB | |
| DB | |
| API spec | |
| Mail | |
| Chưa tra được | |
