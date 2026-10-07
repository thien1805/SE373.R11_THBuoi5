# Báo cáo đánh giá bài tập Block 1: Tra cứu chính sách đúng phiên bản

> **Thông tin sinh viên:**
> - **Sinh viên:** Phạm Ngọc Thiện
> - **MSSV:** 23521485
> - **Nhóm thực hành / GVHD:** Thầy Nguyễn Hiếu Nghĩa
> - **Môn học:** Agentic AI Engineering (D05 - Tool Use & Skill Use)

---

## 1. Kết quả kiểm tra Tool `list_files` trực tiếp

Tool `list_files` được kiểm thử với 4 trường hợp theo đúng yêu cầu đề bài:

| STT | Trường hợp kiểm tra | Đường dẫn đầu vào | Kết quả trả về | Đánh giá |
|:---:|:---|:---|:---|:---:|
| 1 | Thư mục hợp lệ | `data/policies` | `{"ok": true, "path": "data/policies", "items": [{"name": "policy-before-oct.md", "path": "data/policies/policy-before-oct.md", "type": "file"}, {"name": "policy-from-oct.md", "path": "data/policies/policy-from-oct.md", "type": "file"}]}` | **Đạt** (liệt kê đúng file, sắp xếp theo tên, có type) |
| 2 | Đường dẫn là file | `data/weekly_notes.md` | `{"ok": false, "error": {"code": "NOT_A_DIRECTORY", "message": "Đây là file, không phải thư mục: data/weekly_notes.md"}}` | **Đạt** (báo lỗi rõ ràng, không trả rỗng) |
| 3 | Đường dẫn không tồn tại | `data/khong-ton-tai` | `{"ok": false, "error": {"code": "DIRECTORY_NOT_FOUND", "message": "Không tìm thấy thư mục: data/khong-ton-tai"}}` | **Đạt** (báo lỗi rõ ràng) |
| 4 | Đường dẫn vượt workspace | `../` | `{"ok": false, "error": {"code": "PATH_OUTSIDE_WORKSPACE", "message": "Đường dẫn thoát ra ngoài workspace: ../"}}` | **Đạt** (chặn traversal an toàn) |

---

## 2. Kết quả kiểm thử các trường hợp nghiệp vụ

### Trường hợp A: Mua trước ngày đổi chính sách
- **Câu hỏi người dùng:**
  > *"Tôi mua ngày 28/09/2026, yêu cầu hoàn ngày 06/10/2026, chưa kích hoạt. Tôi có được hoàn không?"*
- **Phân tích:**
  - Ngày mua: 28/09/2026 (< 2026-10-01) → Chọn chính sách trước tháng 10 (`data/policies/policy-before-oct.md`).
  - Số ngày lịch đã qua: từ 28/09/2026 đến 06/10/2026 là **8 ngày**.
  - Giới hạn quy định: trong vòng **7 ngày**.
- **Kết luận của Agent:** **Không đủ điều kiện** hoàn tiền do quá hạn 7 ngày.
- **Bằng chứng trong Trace:**
  - File trace: `stage-02-skills/traces/20261007-124552_782759d6_turn01_ff251ba4.jsonl` (Conversation ID: `782759d6aeb5490b8ed21912873731fe`, Run ID: `ff251ba4099c430e8574f22782da6022`)
  - Agent đọc metadata skill `refund-policy`.
  - Gọi `read_file("skills/refund-policy/SKILL.md")` (sequence 4).
  - Gọi `list_files("data/policies")` (sequence 8).
  - Gọi `read_file("data/policies/policy-before-oct.md")` (sequence 12).
  - Gọi `read_file("data/policies/policy-from-oct.md")` (sequence 16).
  - Gọi `read_file("skills/refund-policy/references/answer-template.md")` (sequence 20).
  - Trả lời dẫn đúng căn cứ tài liệu và định dạng template: 8 ngày > 7 ngày, KHÔNG ĐỦ ĐIỀU KIỆN.

### Trường hợp B: Mua từ ngày đổi chính sách
- **Câu hỏi người dùng:**
  > *"Tôi mua ngày 02/10/2026, yêu cầu hoàn ngày 12/10/2026, chưa kích hoạt. Tôi có được hoàn không?"*
- **Phân tích:**
  - Ngày mua: 02/10/2026 (>= 2026-10-01) → Chọn chính sách từ tháng 10 (`data/policies/policy-from-oct.md`).
  - Số ngày lịch đã qua: từ 02/10/2026 đến 12/10/2026 là **10 ngày**.
  - Giới hạn quy định: trong vòng **14 ngày**.
  - Trạng thái kích hoạt: Chưa kích hoạt.
- **Kết luận của Agent:** **ĐỦ ĐIỀU KIỆN** hoàn tiền. **Phí hoàn tiền: Không thu phí hoàn tiền (0%)**.
- **Bằng chứng trong Trace:**
  - File trace: `stage-02-skills/traces/20261007-124657_782759d6_turn02_92484153.jsonl` (Run ID: `924841534d984476b4d24b192d9bd7a1`)
  - Tận dụng context đã nạp từ Turn 1 (skill + nội dung policy), Agent tính toán số ngày = 10 ngày.
  - Trả lời đúng cấu trúc template: 10 ngày <= 14 ngày, ĐỦ ĐIỀU KIỆN, không thu phí.

### Trường hợp Đổi tên file:
- **Thao tác:** Đổi tên `policy-before-oct.md` thành `policy-v1-old.md` và `policy-from-oct.md` thành `policy-v2-new.md` trong `data/policies/`. Mở hội thoại mới và chạy lại Case A & Case B.
- **Kết quả:** Agent tự động gọi `list_files("data/policies")`, nhận được danh sách tên file mới, gọi `read_file` theo tên mới và đưa ra kết luận chính xác như cũ.
- **Bằng chứng trong Trace:** Agent không bị lỗi `FILE_NOT_FOUND`, không dùng tài liệu từ bộ nhớ cũ mà đọc từ các file vừa đổi tên.

### Trường hợp Thiếu thông tin:
- **Câu hỏi người dùng:**
  > *"Tôi mua ngày 02/10/2026, muốn hoàn ngày 12/10/2026."*
- **Kết quả:** Agent nhận diện còn thiếu thông tin trạng thái kích hoạt của sản phẩm. Agent lịch sự phản hồi yêu cầu người dùng cung cấp tình trạng kích hoạt, không tự ý giả định "chưa kích hoạt" và chưa vội đưa ra kết luận.
- **Bằng chứng trong Trace:**
  - File trace: `stage-02-skills/traces/20261007-124817_782759d6_turn03_ffc8810f.jsonl` (Run ID: `ffc8810f97314b8195bd43d2f6d1dc7c`)
  - Agent không đưa ra kết luận hoàn tiền sớm mà hỏi lại khách hàng tình trạng kích hoạt theo đúng bước 1 của `SKILL.md`.

---

## 3. Trả lời câu hỏi cuối bài

> **Câu hỏi:** *Vì sao cần tool để tìm file và skill để hướng dẫn chọn chính sách? Nếu agent chưa có tool tìm file, việc sửa prompt có giải quyết được yêu cầu đổi tên file không? Giải thích.*

### Trả lời:

1. **Vì sao cần tool để tìm file (`list_files`):**
   - Môi trường tệp tin thực tế tại runtime là môi trường động (dynamic environment). Tên file, số lượng file có thể thay đổi hoặc cập nhật bất cứ lúc nào mà không thể biết trước khi lập trình prompt.
   - Tool `list_files` trao cho Agent khả năng **nhận thức môi trường (grounded perception)** tại thời điểm thực thi, giúp agent tự khám phá danh mục tài liệu sẵn có thay vì đoán mò (hallucinate) tên file.

2. **Vì sao cần skill để hướng dẫn chọn chính sách (`refund-policy`):**
   - Logic nghiệp vụ hoàn tiền bao gồm nhiều quy tắc chi tiết: quy ước ngày hiệu lực, tính toán khoảng cách ngày lịch, xác thực điều kiện kích hoạt, công thức phí và xử lý khi thiếu thông tin đầu vào.
   - Nếu đưa toàn bộ quy tắc này vào System Prompt ban đầu sẽ gây ra hiện tượng **context bloat** (phình to context), lãng phí token và làm loãng khả năng phản hồi của agent ở các tác vụ khác.
   - Skill cho phép áp dụng nguyên lý **Progressive Disclosure** (tiết lộ lũy tiến): Agent chỉ nắm metadata tóm tắt trong catalog; khi và chỉ khi người dùng yêu cầu nghiệp vụ liên quan, agent mới đọc chi tiết `SKILL.md` và `references/` để làm theo quy trình chuẩn.

3. **Nếu agent chưa có tool tìm file, việc sửa prompt có giải quyết được yêu cầu đổi tên file không?:**
   - **HOÀN TOÀN KHÔNG.**
   - Prompt là dữ liệu tĩnh được nạp vào lúc khởi tạo hoặc gửi kèm tin nhắn. Nếu không có tool `list_files`, Agent hoàn toàn "mù" trước cấu trúc thư mục thực tế trên đĩa cứng.
   - Khi tên file trên ổ đĩa bị đổi, nếu không có ai sửa thủ công prompt để cập nhật tên file mới, agent sẽ vẫn cố đọc tên file cũ và bị lỗi `FILE_NOT_FOUND` hoặc phải đoán bừa.
   - Việc cố tình "sửa prompt để ghi sẵn tên file" thực chất chỉ là hardcode lại tên file mới vào prompt, vi phạm yêu cầu thiết kế thích ứng động và sẽ tiếp tục gãy ngay khi file bị đổi tên lần nữa. Vì vậy, tool tìm file là điều kiện tiên quyết không thể thay thế bằng prompt.
