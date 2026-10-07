---
name: refund-policy
description: Tra cứu chính sách hoàn tiền và đánh giá điều kiện hoàn tiền cho đơn hàng theo ngày mua của khách hàng. Dùng khi người dùng hỏi về việc hoàn tiền, đổi trả, điều kiện hoàn trả hoặc phí hoàn tiền.
---

# Quy trình kiểm tra chính sách hoàn tiền

Hướng dẫn tra cứu chính sách và phản hồi yêu cầu hoàn tiền của khách hàng.

## Các bước thực hiện

1. **Kiểm tra thông tin đầu vào:**
   Kiểm tra xem người dùng đã cung cấp đủ 3 thông tin sau chưa:
   - Ngày mua hàng.
   - Ngày yêu cầu hoàn tiền.
   - Trạng thái kích hoạt của sản phẩm (đã kích hoạt hay chưa kích hoạt).
   
   **Quy tắc bắt buộc:** Nếu thiếu bất kỳ thông tin nào trong 3 thông tin trên (ví dụ không nêu rõ sản phẩm đã kích hoạt hay chưa), **phải hỏi lại người dùng để làm rõ trước khi kết luận**, tuyệt đối không tự ý giả định hay phỏng đoán.

2. **Khám phá tài liệu chính sách:**
   - Dùng tool `list_files` với đường dẫn `data/policies` để lấy danh sách các file chính sách hiện có trong thư mục (không đoán trước hoặc cố định tên file).
   - Dùng tool `read_file` đọc nội dung từng tài liệu chính sách tìm được để xác định phạm vi hiệu lực (thời gian áp dụng) của từng chính sách.

3. **Chọn chính sách áp dụng theo Ngày Mua:**
   - Đối chiếu ngày mua của khách hàng với phạm vi hiệu lực trong tài liệu:
     - Ngày mua trước `2026-10-01`: Áp dụng chính sách trước tháng 10.
     - Ngày mua từ `2026-10-01` trở đi (bao gồm ngày này): Áp dụng chính sách từ tháng 10.

4. **Tính toán số ngày và đối chiếu điều kiện:**
   - Tính số ngày chênh lệch lịch giữa ngày yêu cầu hoàn tiền và ngày mua:
     `Số ngày = Ngày yêu cầu hoàn - Ngày mua`
     *(Lưu ý: Dùng ngày yêu cầu trong câu hỏi của khách hàng, không dùng ngày hiện tại của máy tính. Nếu số ngày bằng đúng giới hạn quy định thì vẫn đủ điều kiện về thời gian).*
   - Đối chiếu với điều kiện của chính sách đã chọn:
     - Nếu sản phẩm đã kích hoạt: Không được hoàn tiền.
     - Nếu số ngày vượt quá thời hạn cho phép: Không được hoàn tiền do quá hạn.
     - Nếu trong thời hạn cho phép và sản phẩm chưa kích hoạt: Đủ điều kiện hoàn tiền. Xác định mức phí hoàn tiền theo chính sách (ví dụ 10% hoặc không thu phí).

5. **Đọc template và trả lời:**
   - Dùng tool `read_file` đọc template tại `skills/refund-policy/references/answer-template.md`.
   - Trình bày câu trả lời theo đúng cấu trúc của template, nêu rõ đường dẫn file tài liệu làm căn cứ.
