# Knowledge pack vai PO

Kiến thức chung cho vai Product, không phụ thuộc sản phẩm, chép từ AWS AI-DLC Workflows (`core/knowledge/aidlc-product-agent/`, giấy phép MIT-0).

## Bản AWS đang bám

| | |
|---|---|
| Repo | https://github.com/awslabs/aidlc-workflows |
| Commit đối chiếu lần cuối | `0488aff`, ngày 18/10/2026, sau bản phát hành 2.11.0 |
| Kết quả đối chiếu | 8 file dưới đây trùng nội dung bản đó, chỉ khác dòng ghi nguồn. Nhãn "v2.10" ghi trước đây là sai: nội dung đã là bản 2.11 |
| Lần đối chiếu sau | Khi AWS ra bản mới: so từng file ở đây, sau đó so dòng "Lệch so với AWS" trong bảng đầu mỗi file `engine/stages/` với stage cùng số của AWS |

Protocol stage, gate và review của quy trình cũng bám bản này. Knowledge base của sản phẩm nằm riêng ở `domain/` tại gốc repo. File stage trong `engine/stages/` ghi file nào cần đọc.

| File | Nội dung | Stage đọc | Tình trạng |
|---|---|---|---|
| `corner-checklist-aws.md` | Góc thường bị sót, quét từng thành phần qua danh sách cố định. Bản gốc chung; mỗi domain viết lại thành `domain/corner-checklist.md` | 2.3, 2.42 qua bản của domain | Nguyên văn AWS |
| `requirements-guide.md` | FR, NFR, constraint, assumption; mẫu acceptance criteria; completeness checklist; ma trận truy vết | 2.3 | Nguyên văn AWS |
| `requirements-elicitation.md` | Phỏng vấn, workshop, quan sát, phân tích tài liệu, prototype; validation checklist | 1.1, 2.3 | Nguyên văn AWS |
| `user-story-patterns.md` | INVEST, cách tách story, Given/When/Then, anti-pattern, Definition of Ready | 2.4, 2.42 | Nguyên văn AWS |
| `prioritization-frameworks.md` | MoSCoW, WSJF, RICE, Kano; xử lý hoà và bất đồng | 1.4, 2.4 | Nguyên văn AWS |
| `product-guide.md` | Persona, MVP, story mapping, workflow planning | 1.1, 1.4, 2.4 | Nguyên văn AWS |
| `market-research-methods.md` | Competitive analysis, SWOT, build vs buy, market sizing | 1.2 | Nguyên văn AWS |
| `functional-design-guide.md` | Business rule, quy tắc tính toán, phân quyền, luồng, máy trạng thái | 2.42 | Nguyên văn AWS; PO chỉ dùng phần nghiệp vụ |

File chép nguyên văn giữ tiếng Anh, có dòng nguồn ở đầu. Cập nhật từ AWS: `git clone --depth 1 https://github.com/awslabs/aidlc-workflows`, so với bản trong repo, giữ dòng nguồn. `functional-design-guide.md` chép để PRD theo đúng cách AWS đặc tả business rule, quy tắc tính toán, phân quyền và máy trạng thái; phần thiết kế thực thể trong file là việc của Tech PIC.
