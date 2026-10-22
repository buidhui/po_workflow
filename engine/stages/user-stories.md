# 2.4 User Stories

| | |
|---|---|
| Stage | 2.4 User Stories |
| Slug | user-stories |
| Thư mục | `inception/user-stories` |
| Phase | inception |
| Plugin | (stage gốc AWS) |
| Lệch so với AWS | AWS chạy mob với design, developer, quality agent và sinh stories kèm acceptance criteria mã `AC`, personas, user-stories-assessment. Ở đây không mob và các PIC không góp ý ở stage này, giống cấu hình mặc định của AWS khi chế độ cộng tác tắt; các team đọc PRD chi tiết ở 2.43. Không viết acceptance criteria, phần đó viết ở 2.42; không có file personas; cần 2.31 xong trước |
| Execution | always ở M và L. S gộp vào 2.42 |
| Lead | product |
| Produces | `inception/user-stories/stories.md` · `user-stories-questions.md` |
| Consumes | `requirements.md` (bắt buộc) · `scope-document.md` (Unit) · `impact-matrix.md` · `solution-options.md` (tuỳ) · `decisions.md` |
| Requires | requirements-analysis, impact-analysis |
| Profiles | M, L |
| Reviewer | ai-reviewer |
| Summary confirmation | required |
| Template | `engine/templates/stories.md` |
| Checklist | `engine/verification/user-stories.md` |
| Knowledge | `engine/standards/story-splitting.md` · `engine/knowledge/user-story-patterns.md` §INVEST, §Story Splitting Patterns, §Anti-Patterns, §Definition of Ready Checklist · `product-guide.md` §Story Decomposition Patterns |

Chạy theo `engine/protocol/stage-protocol.md`.

## Mục đích
Danh sách user story đầy đủ, mỗi US gắn vào một Unit, mỗi FR có US phủ, và mỗi US có một thẻ đủ để PO viết PRD chi tiết ở 2.42 mà không phải mở lại requirements. Thẻ phải tả đủ luồng, rule và vùng chạm; acceptance criteria thì chưa, vì phần đó viết ở PRD. AWS: stage 2.4 chạy mob với Design, Developer, Quality agent khi bật chế độ cộng tác; mặc định tắt. PO-Workflow để các team đọc PRD chi tiết và thiết kế ở 2.43.

## Load
requirements (FR, OQ); scope-document (Unit); impact-matrix (coverage gap sinh US); solution-options (option đã chọn); decisions.

## Ask
1. Cách chia theo `engine/standards/story-splitting.md`: dựng bản đồ story theo vai và bước trong hành trình, đề xuất sẵn danh sách story và cách tách cho story quá lớn.
2. Độ mịn: một US là một mục tiêu hoàn chỉnh của người dùng. Không chia theo màn hình, không chia theo rule.
3. US nào làm đợt này, US nào định nghĩa nhưng chưa làm.
4. Vai nào xuất hiện. Có cần vai mới không.
5. Unit từ 1.4 còn đúng hay không. Cần tách, gộp không, vì sao.
6. Nhánh đáng kể nào phải có trong thẻ US, tức ngoại lệ làm đổi luồng. AI đề xuất từ requirements và Impact Matrix, PO thêm bớt.

Mỗi mục trên là một chủ đề của bảng Độ phủ trong questions file, theo `engine/protocol/question-format.md`.

## Generate
`stories.md` theo template: bảng `US1`... với tên một câu tự nhiên theo vai, không ép khuôn As a, I want; vai; Unit; MoSCoW; FR nguồn; đợt này hay chưa làm. Mỗi US một thẻ chín mục theo template: vai và mục tiêu, bối cảnh, luồng chính ba đến bảy bước ở mức hành vi, nhánh đáng kể, rule đã biết kèm mã, dữ liệu và vùng chạm từ Impact Matrix, ngoài phạm vi của US, phụ thuộc, chưa rõ. Thẻ phải đủ để PO viết PRD mà không cần mở lại requirements; mục không có ghi "không có". Không acceptance criteria, không validate theo field, không kiểu dữ liệu, phần đó ở PRD. Bảng FR sang US với trạng thái OK, GAP, Deferred, N/A, GAP phải xử lý trước gate. Bảng Unit: gồm US, phụ thuộc, release độc lập được không, thứ tự gợi ý, thay đổi so với 1.4 kèm lý do. Thẻ nguồn. Assumptions & Open Questions.
Từ ba Unit trở lên thì vẽ sơ đồ phụ thuộc Unit ở mục Units, theo `engine/standards/diagrams.md` mục 4. Chia theo `engine/standards/story-splitting.md`: tiêu chí INVEST ở mục 2, dấu hiệu quá lớn ở mục 4, 8 cách tách ở mục 5, các cách không được chia ở mục 7. Story giữ một dấu hiệu quá lớn mà không tách thì ghi lý do trong thẻ. Story là đơn vị nghiệm thu: cách chia ở đây được giữ nguyên tới Story List sau PRD, và Tech PIC xác nhận cỡ story ở checkpoint.

## Verify
Checklist. Chạy `python3 engine/scripts/po-tools.py trace intents/<slug>` (chưa có PRD nên script chỉ kiểm FR sang US và US mồ côi); GAP hoặc ORPHAN thì sửa trước. Reviewer ai-reviewer.

## Gate
Trình: danh sách US theo Unit, số US đợt này và chưa làm, FR chưa có US, Unit đổi so với 1.4, US có nhánh đáng kể hoặc mục chưa rõ, finding review. Approve là xác nhận cả danh sách lẫn nội dung thẻ, vì PRD viết chi tiết từ thẻ này. Stage kế: 2.42.
