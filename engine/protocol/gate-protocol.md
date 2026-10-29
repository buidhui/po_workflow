# Gate Protocol

Mọi stage kết thúc bằng một approval gate. Bám theo AWS AI-DLC `stage-protocol.md` mục 1 và 2. Gate để chặn sai sót ở từng tầng.

## Trước khi mở gate
- `po-tools.py check` không còn cảnh báo, hoặc cảnh báo còn lại đã có lý do để trình PO. Checklist của stage đã đạt mục blocking. Review độc lập đã xong nếu stage có, và artifact không đổi sau lần review đó.
- Đánh dấu stage `[?]` trong `state.md`. Chỉ `po-tools.py approve` được đánh `[x]`; hook của Claude Code chặn AI sửa tay.
- Câu chặn trong questions file của stage đã có câu trả lời. Ở 2.4 và 2.42, `po-tools.py trace` không còn GAP, ORPHAN. Khi stage đã có bản duyệt trước, mọi mã của bản đó còn trong bản này, mã bỏ thì giữ dòng và ghi 'bỏ', 'chuyển sang' hoặc 'gộp vào'.

## Có người thật tại gate
AWS AI-DLC giữ kiểm này ở mọi scope, kể cả khi hạ các guard khác: duyệt chỉ hợp lệ khi có lượt trả lời của người sau khi gate được trình. PO-Workflow làm theo cách tương tự:
- Hook `engine/scripts/po-hook.py` ghi mỗi lượt PO gõ và mỗi lựa chọn PO bấm trong hộp chọn vào `.po/turns.jsonl`. File này không commit, AI không sửa được.
- `po-tools.py approve` chỉ ghi khi `--words` có nguyên văn trong một lượt PO ghi sau lần sửa artifact cuối cùng. Không thấy thì từ chối và giải thích.
- Câu chặn chưa trả lời, GAP hoặc ORPHAN của trace, mã có ở bản duyệt trước mà bản này không còn: approve từ chối và liệt kê từng mục. Một lời chấp nhận chung không cho qua các mục này. Muốn giữ nguyên một mục, như hoãn câu chặn hay nhận một GAP, PO quyết riêng từng mục: AI trình danh sách mã, PO trả lời có nêu từng mã, lệnh chạy với `--accept-items "<mã>,<mã>" --item-words "<lời PO>"`. Script đối chiếu để lời PO nêu đủ mọi mã được quyết. AWS làm tương tự: không đi tiếp khi câu hỏi chưa trả lời đủ, sensor chặn chỉ qua khi người sửa hoặc vượt có ghi lại.
- Kiểm máy còn cảnh báo thì approve từ chối, trừ khi PO chấp nhận; lời chấp nhận đưa vào `--accept-warnings`. Stage có reviewer mà artifact đổi sau review thì approve từ chối, trừ khi PO quyết duyệt không review lại; lời đó đưa vào `--accept-review-gap`. Hai lời này cũng phải có trong lượt PO và được ghi vào DEC.
- Dùng công cụ không có hook: PO tự chạy lệnh approve trong terminal. Script coi người gõ lệnh trong terminal là PO.

## Quyết định của PO ngoài gate
Theo danh sách chuyển trạng thái chỉ engine được làm của AWS (ENGINE_OWNED_STATE_TRANSITIONS), các quyết định dưới đây đổi phần `state.md` hoặc `decisions.md` do engine giữ. AI hỏi PO, chờ PO trả lời, sau đó chạy lệnh với lời PO; lời phải nằm trong 3 lượt gần nhất của PO. Hook chặn AI sửa tay các dòng này.

| Quyết định | Lệnh |
|---|---|
| Bỏ qua một stage | `po-tools.py skip <intent> <stage> --words "<lời PO>" --reason "<lý do>"`. Stage có Execution conditional mà điều kiện không xảy ra thì AI chạy không cần `--words` |
| Đổi profile | `po-tools.py profile <intent> <S/M/L> --words "<lời PO>" --reason "<lý do>"` |
| Bật, tắt reviewer, summary confirmation, learnings | `po-tools.py switch <intent> <reviewer/summary/learnings> <on/off> --words "<lời PO>"` |
| Nhận, Hoãn, Bác, Đóng change request | `po-tools.py cr <intent> CR<n> <nhan/hoan/bac/dong> --words "<lời PO>"`; Nhận kèm `--reopen <stage>` để mở lại stage đã duyệt |
| Mở lại gate đã ghi nhầm Approve | `po-tools.py reopen <intent> <stage> --words "<lời PO>" --reason "<lý do>"` |

Thêm stage, tức chuyển `[S]` về `[ ]` hoặc thêm dòng stage `[ ]`, thì sửa tay được, vì làm quy trình chặt hơn.

## Thứ tự tại gate
1. Thông điệp hoàn thành.
2. Câu hỏi bài học, nếu profile bật learnings, hỏi thành một lượt riêng.
3. Câu hỏi duyệt.

PO cần đọc kết quả trước, sau đó mới biết điều gì đáng nhớ. Hỏi bài học trước thông điệp hoàn thành là hỏi khi PO chưa thấy stage làm ra gì.

## Thông điệp hoàn thành, năm phần, đúng thứ tự
1. Tiêu đề: `# <Tên stage> hoàn thành`.
2. Bảng artifact: tên file, nội dung tóm tắt bằng số (số FR, số US, số câu đã trả lời). Số lấy từ script khi có, không tự đếm. Không có lời dặn như "xin xem lại".
3. Kết quả review nếu có: READY hoặc NOT-READY, sau đó từng finding còn mở trong sổ finding: mã, mức, vị trí, vấn đề, hành động.
4. Đường dẫn để mở: thư mục của stage.
5. Một câu nói duyệt xong thì sao: stage kế là gì, ai làm gì tiếp.

Lần đầu trong intent, thêm một dòng: profile, depth, cách trả lời đang dùng, và cách đổi.

## Câu hỏi bài học
Đưa các dòng mới của stage trong `memory.md` thành danh sách chọn, hỏi "Có gì cần nhớ cho lần sau không?" với hai lựa chọn Không có, Thêm ghi chú. Hỏi kể cả khi danh sách rỗng. Dòng được giữ ghi theo `stage-protocol.md` bước 6.

## Câu hỏi duyệt
Hộp chọn AskUserQuestion. Mỗi lựa chọn ghi rõ hệ quả. Lựa chọn khuyến nghị đứng đầu. Approve nêu tên stage kế tiếp.

| Lựa chọn | Khi nào có | Hệ quả |
|---|---|---|
| **Approve** | Luôn | Ghi chép sau Approve bên dưới. Finding còn mở ghi *Accepted risk*. Sang stage kế |
| **Request Changes** | Luôn | `[R]`. Lời PO là phản hồi. Sửa, chạy lại review nếu artifact đổi, trình lại gate. Đếm số lần |
| **Accept as-is** | Từ lần Request Changes thứ ba. Báo trước từ lần thứ hai. Riêng Alignment gate: có ngay khi PIC quá hạn chưa duyệt | Như Approve, ghi "chấp nhận có điều kiện" và điều kiện |
| **Add [stage]** | Ideation và Inception, khi có stage bị bỏ qua mà stage hiện tại thấy cần | Thêm stage vào `state.md`, nói một dòng, tiếp tục |
| **Reject Initiative** | Chỉ ở 1.7 | Kết thúc intent, ghi lý do, `state.md` chuyển Archived |

Stage 2.43 Design Alignment là Alignment gate: Approve chỉ khi bảng Duyệt của Decision Brief có Design PIC, Tech PIC, QA PIC ghi "Đồng ý" hoặc "Có ý kiến"; PIC tự ghi, hoặc PO ghi theo tin nhắn xác nhận lưu trong `decisions.md`. Lượt duyệt chỉ tính khi tên trùng tên PIC ở `intent.md`, cột Bản trùng bản đã gửi duyệt bằng `po-tools.py sign-start`, và Decision Brief không đổi sau lần gửi đó; Decision Brief đổi thì tăng version, chạy lại `sign-start` và lấy lại lượt duyệt, như receipt của AWS gắn với đúng bản artifact đã review. Một PIC ghi "Yêu cầu sửa" là Request Changes. Tới hạn mà còn PIC chưa duyệt thì PO chọn chờ thêm, hoặc Accept as-is ngay kèm lý do ghi DEC, không cần chờ lần Request Changes thứ ba. Script coi thiếu lượt duyệt là cảnh báo, nên lệnh approve chạy với `--accept-warnings`.

Profile M: stage 1.1 và 1.4 duyệt chung một gate. Thông điệp hoàn thành gộp hai artifact. Request Changes nêu rõ sửa artifact nào. Profile M không chạy 1.7, nên phase check Ideation chạy ở gate chung này: năm điều kiện Ideation trong `engine/templates/phase-check.md`, ghi `verification/phase-check-ideation.md`.

## Đọc câu trả lời của PO
- Một lựa chọn rõ ("1", "approve", "duyệt", "ok"): ghi đúng lựa chọn đó.
- Duyệt kèm chỉ thị ("ok nhưng đổi tên trường X"): làm việc được yêu cầu, nói một dòng đã làm gì, hỏi lại một câu "Duyệt bản đã sửa?". Ghi Approve khi PO trả lời. Lời duyệt phải đến sau lần sửa cuối, nên không ghi Approve trước và sửa sau.
- Duyệt kèm dừng ("duyệt, hôm nay dừng"): ghi Approve, ghi *Parked* vào `state.md`, nói cách tiếp tục bằng `/po`.
- Yêu cầu sửa không kèm duyệt: ghi Request Changes, lời PO là phản hồi. Chỉ hỏi "sửa gì" khi PO chưa nói.
- Nhờ một việc mà không duyệt ("thêm giúp một dòng ví dụ"): làm việc đó, giữ gate mở, trình lại. Không ghi Approve.
- Chọn ô "Khác" mà không viết gì: không ghi nhận, hỏi lại một câu.
- Câu hỏi: trả lời, sau đó kết thúc lượt. Lượt kế tiếp mới là quyết định.
- Không rõ ("hmm", "để xem"): hỏi một câu ngắn. Không suy đoán là duyệt.
- Làm lại stage, nhảy stage, bắt đầu intent mới: không phải câu trả lời gate. Làm theo `/po`.

## Ghi chép sau Approve
Chạy một lệnh, làm trọn mọi việc ghi chép:

```
python3 engine/scripts/po-tools.py approve intents/<slug> <slug-stage> --words "<lời PO nguyên văn>"
```

Script từ chối nếu stage không ở `[?]`, nếu lời duyệt không có trong lượt PO, nếu kiểm máy còn cảnh báo hoặc review không ứng với bản hiện tại mà PO chưa chấp nhận, xem mục Có người thật tại gate. Qua được thì làm theo thứ tự:
1. Frontmatter artifact: `version` theo quy tắc phiên bản dưới đây, `status: approved`, `approved_at`.
2. Chụp bản duyệt vào `archive/<slug>/<artifact>-v<version>-<YYYYMMDD>.md`. Từ chối ghi đè. File trong archive không bao giờ sửa.
3. `decisions.md`: một dòng DEC, cột *Nguyên văn* là lời PO không sửa chữ, cột *Người quyết* là tên trong `git config user.name`, kèm giờ.
4. `state.md`: `[x]`, bảng Versions, dòng Log có giờ và tên, stage kế và việc kế tiếp.
5. In dòng tiến độ: `Progress: <đã xong>/<tổng stage của profile> | <PHASE> <đã xong>/<tổng> · Next: <tên stage kế>`.

Sau script, AI tự làm hai việc: finding Accepted risk ghi vào bảng Accepted risks của `decisions.md` kèm lý do; sổ finding của stage chuyển các finding còn mở sang Accepted risk. Không chạy được python thì làm tay đủ năm việc trên.

### Quy tắc phiên bản
- Bản nháp là 0.x. Mỗi lần PO trả lời xong một đợt câu hỏi hoặc yêu cầu sửa thì tăng số phụ: 0.1, 0.2.
- Lần duyệt đầu tiên của một artifact: 1.0.
- Mỗi lần duyệt lại sau đó, do Request Changes sau duyệt hay change request: tăng số phụ, 1.0 thành 1.1.
- Intent cũ đã duyệt ở 0.x trước quy tắc này giữ nhánh 0.x và tăng số phụ.

### Gắn tag cho bản bàn giao
Duyệt `prd` hoặc `decision-brief`: script in tên tag gợi ý dạng `<intent>/prd-v1.0` hoặc `<intent>/decision-brief-v1.0`. Sau khi commit, gắn tag và push tag. Agent của Dev đọc PRD theo tag nên luôn lấy đúng bản đã duyệt, xem README mục 6. Profile S: duyệt `prd` xong thì chạy `/po-stories`. Profile M, L: duyệt `prd` xong thì giao ba team viết file thiết kế theo 2.43; chỉ chạy `/po-stories` sau khi 2.43 được duyệt.

## Sửa lựa chọn bị ghi nhầm
PO nói vừa rồi chọn nhầm:
- Ghi nhầm Request Changes: trình lại gate, không đổi file.
- Ghi nhầm Approve: PO nói rõ là ghi nhầm, AI chạy `po-tools.py reopen <intent> <stage> --words "<lời PO>" --reason "<lý do>"`. Lệnh đưa stage từ `[x]` về `[?]` và thêm DEC đính chính. Trình lại gate. Bản chụp trong `archive/` giữ nguyên làm lịch sử; lần duyệt sau lên số phụ mới.

## Sau Request Changes
- Sửa đúng phần PO nêu, không viết lại toàn bộ. Nói đã đổi gì.
- Artifact đổi và stage có reviewer: chạy lại review trước khi trình lại.
- Trình lại gate với thông điệp hoàn thành mới.
- Không để stage ở `[R]` mà không trình lại gate.
