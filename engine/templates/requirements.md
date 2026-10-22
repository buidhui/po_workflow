---
intent: <slug>
artifact: requirements
version: 0.1
status: draft
inputs: <artifact đầu vào@version, ví dụ requirements@1.0; stage đầu tiên ghi none>
---
# Requirements: <Tên tính năng>

## 1. Intent summary
<Một đoạn.> [desc] [1.1 Q1]

## 2. Functional requirements
<Mỗi FR một hành vi, viết theo một trong năm mẫu EARS: luôn đúng "Hệ thống phải…"; theo sự kiện "Khi <sự kiện>, hệ thống phải…"; theo trạng thái "Trong khi <trạng thái>, hệ thống phải…"; hành vi không mong muốn "Nếu <điều kiện>, hệ thống phải…"; tuỳ chọn "Với <cấu hình> đang bật, hệ thống phải…". AWS viết "The system shall…". Hai hành vi nối bằng "và" thì tách thành FRn.m. Cột Phục vụ ghi mục tiêu `O<n>` hoặc Unit `U<n>` mà FR đáp ứng, theo BABOK 5.1 và 7.3.>
### Nhóm A: <tên khả năng>
| ID | Yêu cầu, điều phải đúng | Ưu tiên | Phục vụ | Existing, New, Changed | Mã KB liên quan | Nguồn |
|---|---|---|---|---|---|---|
| FR1 | | Must | O1 | New | | [Q1] |
| FR1.1 | | | | | | |

### Nhóm B: <tên khả năng>
| ID | Yêu cầu | Ưu tiên | Phục vụ | Existing, New, Changed | Mã KB | Nguồn |
|---|---|---|---|---|---|---|

## 3. Non-functional requirements
| ID | Yêu cầu | Chỉ số đo | Nguồn |
|---|---|---|---|
| NFR1 | | | |
<Ghi chỉ số đo được. Chưa có chỉ số thì ghi OQ ở mục Assumptions & Open Questions để PO xác định, không bỏ NFR.>

## 4. Constraints
| Loại | Ràng buộc | Nguồn |
|---|---|---|
| Nghiệp vụ | | |
| Tenant và hằng số | <cứng hay cấu hình> | [KB] |
| Tích hợp | | |
| Dữ liệu cũ | | |

## 5. Assumptions & Open Questions
| # | Nội dung | Loại | Chặn | Owner | Trạng thái |
|---|---|---|---|---|---|
| OQ1 | | | | | mở |

## 6. Out of scope
| Không làm | Vì sao |
|---|---|

## 7. Sources read
| Nguồn | Cụ thể | Last verified |
|---|---|---|
| KB | | |
| API spec | | |
| Schema | | |
Chưa tra được: <vùng nào không có nguồn để tra>
