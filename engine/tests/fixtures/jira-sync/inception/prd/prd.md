---
intent: story-list
artifact: prd
feature: LMS-F903
version: 1.0
status: approved
approved_at: 2026-10-15T10:00
---
# [PRD] Chứng chỉ PDF

# Units

| Unit | Gồm US | Phụ thuộc | Release độc lập được? |
|---|---|---|---|
| U1 | US1 | không | có |
| U2 | US2, US3 | U1 | có |

# Specific Requirement

## US1: Tải chứng chỉ PDF

### 1/ User story

Là học viên, tôi tải chứng chỉ dạng PDF sau khi hoàn thành khoá học.

**Ưu tiên:** Must

### 2/ Pre - Condition

- Học viên đã hoàn thành khoá học

### 3/ Scenario

Học viên mở trang khoá học, bấm Tải chứng chỉ.

### 4/ Acceptance criteria

**Tiêu chí chấp nhận**

- `AC1.1` Khi học viên đã hoàn thành khoá học bấm Tải chứng chỉ, trình duyệt tải về một tệp PDF. Theo `BR1.1`
- `AC1.2` Khi học viên chưa hoàn thành khoá học, nút Tải chứng chỉ không hiện. Theo `BR1.2`

**UI / UX / Rule UX / Rule UI**

| Màn hình | Giao diện | Field | Yêu cầu |
| --- | --- | --- | --- |
| Trang khoá học | Nút | **Tải chứng chỉ** | Chỉ hiện khi đã hoàn thành, xem `US1` |

**Business requirement — Business rule**

- `BR1.1` Tệp chứng chỉ là PDF khổ A4 ngang, tên tệp theo mã chứng chỉ
- `BR1.2` Chỉ học viên đã hoàn thành khoá học mới tải được, theo luật có sẵn `BR-CERT-02`

### 5/ Out of scope

- Gửi chứng chỉ qua email

### 6/ Conner case

---

## US2: Xem lại chứng chỉ đã cấp

### 1/ User story

Là học viên, tôi xem lại các chứng chỉ đã được cấp.

Ưu tiên: Should

### 4/ Acceptance criteria

#### UI / UX / Rule UX / Rule UI

| Màn hình | Giao diện | Field | Yêu cầu |
|---|---|---|---|
| Hồ sơ | Danh sách | **Chứng chỉ** | Mới nhất ở đầu |

#### Nội dung thông báo — `MAIL-CERT-01`

| | |
|---|---|
| **Khi nào bắn** | Một chứng chỉ của học viên bị thu hồi |

#### Business requirement — Business rule

- `BR-2.1` Danh sách chỉ hiện chứng chỉ còn hiệu lực, cùng luật `KB-CERT-03` và `BR-EDIT-07`
- `BR-2.2` Chứng chỉ bị thu hồi ẩn khỏi danh sách, xem `BR-1.1`

### 5/ Out of scope

- Chia sẻ chứng chỉ lên mạng xã hội

### 6/ Conner case

- Học viên có hơn 100 chứng chỉ

---

## US3: Chia sẻ đường dẫn chứng chỉ

### 1/ User story

Là học viên, tôi gửi đường dẫn chứng chỉ cho nhà tuyển dụng.

**Ưu tiên:** Could

### 2/ Pre - Condition

- US2 đã xong: học viên thấy danh sách chứng chỉ

### 4/ Acceptance criteria

**Tiêu chí chấp nhận**

- `AC3.1` Khi học viên bấm Sao chép đường dẫn, đường dẫn mở được chứng chỉ mà không cần đăng nhập. Theo `BR3.1`
- `AC3.2` Khi chứng chỉ đã bị thu hồi, đường dẫn báo chứng chỉ không còn hiệu lực. Theo `BR3.1`

**Business requirement — Business rule**

- `BR3.1` Đường dẫn chỉ mở được chứng chỉ còn hiệu lực

---

# Open Issues

| # | Nội dung | Người trả lời | Chặn việc gì |
| --- | --- | --- | --- |
| 1 | Chứng chỉ hết hạn có hiện mờ trong danh sách của `US2` không | PO | Chặn thiết kế màn danh sách |
| 2 | Có cần ảnh xem trước cho `US2` không | Design PIC | Không chặn |
| 3 | Kho lưu tệp PDF ở đâu | Dev | Không chặn |
