# Quy ước mã

Mã dùng chung cho mọi team nhận việc từ PO: Design, Tech, QA. Mã đi từ PRD sang story trên Jira, test case, nhánh code và commit, nên phải duy nhất trong toàn công ty và không bao giờ đánh lại.

## Mã sản phẩm

`<SP>` là mã sản phẩm, đặt khi dựng domain pack và ghi ở khoá `code` trong frontmatter của `domain/domain.md`. Không ghi cứng trong engine. Domain đang cài dùng mã ghi trong file đó.

## Bảng mã

| Đối tượng | Mẫu | Ví dụ | Ai cấp | Ở đâu |
|---|---|---|---|---|
| Tính năng | `<SP>-F<NNN>` | `APP-F012` | PO, khi tạo intent, bằng `po-tools.py feature-id` | `intent.md`, đầu PRD, nhãn của mọi story trên Jira |
| User story | `US-<tính năng>-<NN>` | `US-APP-F012-01` | PO, ở 2.4 | Nhãn và tham chiếu của story trên Jira |
| Acceptance criteria | `AC-<tính năng>-<NN>.<n>` | `AC-APP-F012-01.1` | PO, ở 2.42 | Description của story trên Jira |
| Business rule | `BR-<tính năng>-<NN>.<n>` | `BR-APP-F012-01.2` | PO, ở 2.42 | Description của story trên Jira |
| Business rule dùng chung | `BR-<tính năng>-00.<n>` | `BR-APP-F012-00.1` | PO, ở 2.42, PRD mục 4 | Description của mọi story trỏ tới nó |
| Câu hỏi mở | `Q-<tính năng>-<NN>.<n>` | `Q-APP-F012-01.3` | Người hỏi, bất kỳ team nào | Comment trên story Jira |
| Màn hình | `SCR-<tính năng>-<NN>` | `SCR-APP-F012-02` | Design PIC, ở `ux-design.md` tại 2.43 | Story trên Jira, lấy từ bảng Danh sách màn |
| Test case | `TC-<tính năng>-<NN>` | `TC-APP-F012-01` | QA PIC | Test case trên Jira |
| Nhánh code | `feat/<tính năng>-<mô tả>` | `feat/APP-F012-quiz-retake` | Dev | Git |
| Commit | Trailer `Feature: <tính năng>`, thêm `Story: <US>` khi commit thuộc một story | `Feature: APP-F012` | Dev | Git |

`<NNN>` ba chữ số, `<NN>` hai chữ số, đều có số 0 ở đầu. `<n>` là số thứ tự trong story, bắt đầu từ 1.

## Mã ngắn trong tài liệu của intent

Artifact nội bộ và PRD dùng mã ngắn cho dễ đọc: `US1`, `AC1.1`, `BR1.2`. Đầu PRD ghi mã tính năng. Quy đổi là cơ học:

| Mã ngắn trong tài liệu của `APP-F012` | Mã đầy đủ |
|---|---|
| `US1` | `US-APP-F012-01` |
| `AC1.1` | `AC-APP-F012-01.1` |
| `BR1.2`, hoặc `BR-1.2` ở PRD cũ | `BR-APP-F012-01.2` |
| `BR0.1` | `BR-APP-F012-00.1` |
| `SCR2` | `SCR-APP-F012-02` |

`po-tools.py stories` đổi mã khi sinh Story List. Không đổi tay. Từ story trên Jira trở đi, mọi team chỉ dùng mã đầy đủ.

Mã nội bộ của PO như `FR1`, `OQ3`, `DEC5` không đi ra ngoài. Mã Unit `U1` chỉ dùng trong PRD để nhóm user story, còn trên Jira chỉ xuất hiện trong nhãn `<tính năng>-U<n>`, không dùng ở test case.

## Luật không đánh lại

- Mã đã cấp không đổi, không dùng lại, kể cả khi mục bị xoá.
- Tách một story: story cũ giữ mã; phần tách ra nhận số story mới. AC chuyển sang story mới nhận mã mới; AC cũ ghi "chuyển sang `AC-...`", không xoá dòng. Test case trỏ mã cũ vì vậy vẫn tìm được đường đi.
- Gộp hai story: story còn lại giữ mã; story bị gộp ghi "gộp vào `US-...`" và giữ file.
- Cấp số tính năng: script lấy số lớn nhất đã có cộng một. Hai PO cấp cùng lúc trên hai nhánh có thể trùng số; `po-tools.py status` và `doctor` báo trùng ngay sau khi gộp nhánh, PO đến sau đổi số trước khi bàn giao.

## Mã trong tài liệu của PO, theo loại yêu cầu của BABOK 2.3

| Loại | Mã ngắn | Ở đâu | Đi ra ngoài PO? |
|---|---|---|---|
| Nghiệp vụ | `O<n>` mục tiêu, `SC<n>` tiêu chí thành công | intent-statement, PRD mục 1, 2 | Có, trong PRD |
| Của các bên | `US<n>` | stories, PRD mục 6 | Có, mã đầy đủ trên Jira |
| Giải pháp, chức năng | `FR<n>`, `BR<n>.<m>`, `BR0.<n>`, `AC<n>.<m>` | requirements, PRD | BR và AC có, FR nằm trong PRD mục 11 |
| Giải pháp, phi chức năng | `NFR<n>` | requirements, PRD mục 7 | Có, trong PRD |
| Chuyển đổi | `TR<n>` | Impact Matrix mục 8, PRD mục 8 | Có, trong PRD |
| Rủi ro | `RK<n>` | `decisions.md` mục Rủi ro | Có, trong Decision Brief |

## Truy vết

```
FR (nội bộ PO) → US → AC → TC
                      BR → AC
                      SCR → AC
```

Mọi BR có ít nhất một AC. Mọi AC có ít nhất một TC; QA viết TC sau khi story lên Jira và theo dõi độ phủ trên Jira, điều kiện giao Dev không chờ TC. Nhánh và commit truy về tính năng và story qua trailer.

## Khi Dev dùng AWS AI-DLC

AI-DLC sinh mã riêng ở Construction, ví dụ `BR1.1` trong `rules.md` của stage 3.1, cùng dạng với mã ngắn trong PRD nhưng khác nghĩa. Nếu team Dev dùng AI-DLC, mọi tài liệu và story phía Dev trỏ tới yêu cầu của PO bằng mã đầy đủ như `BR-APP-F012-01.1`, không dùng mã ngắn của PRD. Chưa xác định team Dev có dùng AI-DLC hay không; khi đã rõ thì thêm bảng quy đổi vào mục này.
