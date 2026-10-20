---
intent: good
artifact: requirements
version: 1.0
status: approved
approved_at: 2026-10-01T09:00
---
# Requirements: Nhắc lịch học

## 1. Intent summary
Học viên quên buổi học nên cần được nhắc trước giờ học. [desc] [Q1]

## 2. Functional requirements
### Nhóm A: Nhắc lịch
| ID | Yêu cầu, điều phải đúng | Ưu tiên | Existing, New, Changed | Mã KB liên quan | Nguồn |
|---|---|---|---|---|---|
| FR1 | Hệ thống nhắc học viên trước buổi học | Must | New | - | [Q1] |
| FR1.1 | Nhắc qua email trước 24 giờ | Must | New | - | [Q1] |
| FR1.2 | Nhắc trong ứng dụng trước 1 giờ | Should | New | - | [Q1] |
| FR2 | Học viên tự chọn giờ nhắc | Could | New | - | [Q2] |

## 3. Non-functional requirements
| ID | Yêu cầu | Chỉ số đo | Nguồn |
|---|---|---|---|

Đợt này không có NFR đo được. [Q2]

## 4. Constraints
| Loại | Ràng buộc | Nguồn |
|---|---|---|
| Nghiệp vụ | Chỉ nhắc buổi học chưa kết thúc | [suy ra] |

## 5. Assumptions & Open Questions
| # | Nội dung | Loại | Chặn | Owner | Trạng thái |
|---|---|---|---|---|---|
| OQ1 | Học viên đã có email hợp lệ | [assumption] | không | PO | mở |

## 6. Out of scope
| Không làm | Vì sao |
|---|---|
| Nhắc qua SMS | Chưa có kênh gửi SMS [DEC1] |

## 7. Sources read
| Nguồn | Cụ thể | Last verified |
|---|---|---|
| KB | không có | 2026-10-01 |

Chưa tra được: không có.
