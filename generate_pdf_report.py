import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register fonts supporting Vietnamese
FONT_REGULAR = "Arial"
FONT_BOLD = "Arial-Bold"
FONT_ITALIC = "Arial-Italic"

pdfmetrics.registerFont(TTFont(FONT_REGULAR, "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont(FONT_BOLD, "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFont(TTFont(FONT_ITALIC, "C:/Windows/Fonts/ariali.ttf"))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont(FONT_REGULAR, 8.5)
        self.setFillColor(colors.HexColor("#74675b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, A4[1] - 30, "Agentic AI Engineering | D05 - Tool Use & Skill Use | Block 1")
            self.setStrokeColor(colors.HexColor("#ded4c7"))
            self.setLineWidth(0.5)
            self.line(45, A4[1] - 35, A4[0] - 45, A4[1] - 35)
        
        # Footer
        text = f"Trang {self._pageNumber} / {page_count}"
        self.drawRightString(A4[0] - 45, 25, text)
        self.drawString(45, 25, "SV: Phạm Ngọc Thiện (MSSV: 23521485) | GVHD: Thầy Nguyễn Hiếu Nghĩa | Block 1")
        self.setStrokeColor(colors.HexColor("#ded4c7"))
        self.setLineWidth(0.5)
        self.line(45, 36, A4[0] - 45, 36)
        self.restoreState()

def build_pdf(filename="Bao_Cao_Bai_Tap_Block_1_Tra_Cuu_Chinh_Sach.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    style_eyebrow = ParagraphStyle(
        'Eyebrow',
        fontName=FONT_BOLD,
        fontSize=9.5,
        textColor=colors.HexColor("#795438"),
        leading=12,
        spaceAfter=4,
        textTransform='uppercase'
    )
    
    style_title = ParagraphStyle(
        'MainTitle',
        fontName=FONT_BOLD,
        fontSize=20,
        textColor=colors.HexColor("#2a1d15"),
        leading=25,
        spaceAfter=6
    )
    
    style_subtitle = ParagraphStyle(
        'Subtitle',
        fontName=FONT_REGULAR,
        fontSize=11,
        textColor=colors.HexColor("#5c4d41"),
        leading=16,
        spaceAfter=15
    )
    
    style_meta = ParagraphStyle(
        'MetaBox',
        fontName=FONT_REGULAR,
        fontSize=9.5,
        textColor=colors.HexColor("#333333"),
        leading=14
    )
    
    style_h1 = ParagraphStyle(
        'Heading1',
        fontName=FONT_BOLD,
        fontSize=13,
        textColor=colors.HexColor("#3b2418"),
        leading=17,
        spaceBefore=14,
        spaceAfter=6
    )

    style_h2 = ParagraphStyle(
        'Heading2',
        fontName=FONT_BOLD,
        fontSize=10.5,
        textColor=colors.HexColor("#516044"),
        leading=14,
        spaceBefore=8,
        spaceAfter=4
    )

    style_body = ParagraphStyle(
        'Body',
        fontName=FONT_REGULAR,
        fontSize=9.5,
        textColor=colors.HexColor("#26221f"),
        leading=14,
        spaceAfter=5
    )

    style_code = ParagraphStyle(
        'CodeSnippet',
        fontName=FONT_REGULAR,
        fontSize=8.5,
        textColor=colors.HexColor("#1e293b"),
        leading=12,
        backColor=colors.HexColor("#f1ece4"),
        borderPadding=6,
        spaceAfter=6
    )

    style_qa_q = ParagraphStyle(
        'QA_Q',
        fontName=FONT_BOLD,
        fontSize=9.5,
        textColor=colors.HexColor("#795438"),
        leading=14,
        spaceBefore=6,
        spaceAfter=3
    )

    style_th = ParagraphStyle(
        'TH',
        fontName=FONT_BOLD,
        fontSize=8.5,
        textColor=colors.HexColor("#3b2418"),
        leading=11,
        alignment=0
    )

    style_td = ParagraphStyle(
        'TD',
        fontName=FONT_REGULAR,
        fontSize=8,
        textColor=colors.HexColor("#26221f"),
        leading=11,
        alignment=0
    )

    story = []

    # Header Box
    story.append(Paragraph("AGENTIC AI ENGINEERING / D05 / BÀI LUYỆN TẬP 01", style_eyebrow))
    story.append(Paragraph("Báo Cáo Nghiệm Thu: Tra Cứu Chính Sách Đúng Phiên Bản", style_title))
    story.append(Paragraph("Cài đặt Tool tìm kiếm tài liệu động và Skill đánh giá điều kiện hoàn tiền", style_subtitle))

    # Meta card table
    meta_data = [
        [
            Paragraph("<b>Sinh viên:</b> Phạm Ngọc Thiện &nbsp;&nbsp;|&nbsp;&nbsp; <b>MSSV:</b> 23521485", style_meta),
            Paragraph("<b>Nhóm TH / GVHD:</b> Thầy Nguyễn Hiếu Nghĩa", style_meta)
        ],
        [
            Paragraph("<b>Môi trường:</b> Windows, Python 3.14, uv workspace", style_meta),
            Paragraph("<b>Model sử dụng:</b> Gemini 2.5 Flash (OpenAI Compatible)", style_meta)
        ],
        [
            Paragraph("<b>Phạm vi:</b> Stage 00 (Chat) → Stage 01 (Files) → Stage 02 (Skills)", style_meta),
            Paragraph(f"<b>Thời gian nghiệm thu:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", style_meta)
        ],
        [
            Paragraph("<b>Đánh giá bài tập:</b> <b>HOÀN THÀNH 100% CÁC TIÊU CHÍ (VERIFIED)</b>", style_meta),
            Paragraph("<b>Hồ sơ Trace:</b> Đã đối chiếu đầy đủ với file trace thực tế", style_meta)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[240, 265])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fbf9f5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#ded4c7")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # SECTION 1
    story.append(Paragraph("1. Mục tiêu và Kiến trúc giải pháp", style_h1))
    story.append(Paragraph(
        "Bài thực hành giải quyết bài toán cốt lõi trong Agentic AI: <b>Làm thế nào để Agent tự khám phá và áp dụng đúng phiên bản tài liệu nghiệp vụ trong một môi trường thay đổi liên tục mà không cần hardcode?</b>",
        style_body
    ))
    story.append(Paragraph(
        "• <b>Tool <code>list_files(path)</code>:</b> Cung cấp khả năng nhận thức môi trường tại runtime (Grounded Perception). Agent có thể duyệt nội dung thư mục tương đối trong workspace, hỗ trợ sắp xếp theo tên, xử lý lỗi an toàn và chặn hoàn toàn path traversal.<br/>"
        "• <b>Skill <code>refund-policy</code>:</b> Thực hiện nguyên lý Progressive Disclosure. Không nhồi nhét quy tắc vào System Prompt, chỉ nạp metadata vào Catalog. Khi có câu hỏi liên quan, Agent tự đọc <code>SKILL.md</code> và <code>references/answer-template.md</code> để ra quyết định.<br/>"
        "• <b>Chính sách động (Data Policies):</b> Hai phiên bản chính sách được đặt tại <code>data/policies/</code> với mốc chuyển giao 01/10/2026. Agent phải tự đọc và chọn chính sách theo <b>ngày mua</b> của khách hàng.",
        style_body
    ))

    story.append(Spacer(1, 6))

    # SECTION 2
    story.append(Paragraph("2. Kết quả kiểm tra trực tiếp Tool <code>list_files</code>", style_h1))
    story.append(Paragraph("Đã thực hiện unit test và kiểm tra biên với 4 kịch bản theo yêu cầu đề bài:", style_body))

    tool_test_data = [
        [
            Paragraph("STT", style_th),
            Paragraph("Trường hợp kiểm tra", style_th),
            Paragraph("Đường dẫn (path)", style_th),
            Paragraph("Kết quả trả về", style_th),
            Paragraph("Đánh giá", style_th),
        ],
        [
            Paragraph("1", style_td),
            Paragraph("Thư mục hợp lệ", style_td),
            Paragraph("<code>data/policies</code>", style_td),
            Paragraph("<code>{\"ok\": true, \"items\": [policy-before-oct.md, policy-from-oct.md]}</code>", style_td),
            Paragraph("<font color='#2e7d32'><b>ĐẠT</b></font>", style_td),
        ],
        [
            Paragraph("2", style_td),
            Paragraph("Đường dẫn là file", style_td),
            Paragraph("<code>data/weekly_notes.md</code>", style_td),
            Paragraph("<code>{\"ok\": false, \"error\": {\"code\": \"NOT_A_DIRECTORY\"}}</code>", style_td),
            Paragraph("<font color='#2e7d32'><b>ĐẠT</b></font>", style_td),
        ],
        [
            Paragraph("3", style_td),
            Paragraph("Thư mục không tồn tại", style_td),
            Paragraph("<code>data/khong-ton-tai</code>", style_td),
            Paragraph("<code>{\"ok\": false, \"error\": {\"code\": \"DIRECTORY_NOT_FOUND\"}}</code>", style_td),
            Paragraph("<font color='#2e7d32'><b>ĐẠT</b></font>", style_td),
        ],
        [
            Paragraph("4", style_td),
            Paragraph("Thoát workspace", style_td),
            Paragraph("<code>../</code>", style_td),
            Paragraph("<code>{\"ok\": false, \"error\": {\"code\": \"PATH_OUTSIDE_WORKSPACE\"}}</code>", style_td),
            Paragraph("<font color='#2e7d32'><b>ĐẠT</b></font>", style_td),
        ]
    ]

    t_tool = Table(tool_test_data, colWidths=[25, 110, 115, 205, 50])
    t_tool.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ede3d5")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#ded4c7")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tool)

    story.append(Spacer(1, 10))

    # SECTION 3
    story.append(Paragraph("3. Kết quả thực nghiệm và Đối chiếu Bằng chứng Trace", style_h1))
    story.append(Paragraph("Các kết quả dưới đây được trích xuất trực tiếp từ các file trace JSONL thực tế được sinh ra trong quá trình chạy ứng dụng Streamlit tại Stage 02:", style_body))

    # Case A
    story.append(Paragraph("Trường hợp A: Khách hàng mua trước ngày đổi chính sách (28/09/2026)", style_h2))
    story.append(Paragraph(
        "• <b>Câu hỏi:</b> <i>\"Tôi mua ngày 28/09/2026, yêu cầu hoàn ngày 06/10/2026, chưa kích hoạt. Tôi có được hoàn không?\"</i><br/>"
        "• <b>Phân tích tính toán:</b> Ngày mua 28/09/2026 (< 01/10/2026) → Chọn chính sách cũ (giới hạn 7 ngày, phí 10%). Chênh lệch ngày lịch: từ 28/09 đến 06/10 = <b>8 ngày</b>. Vì 8 ngày > 7 ngày nên <b>KHÔNG ĐỦ ĐIỀU KIỆN</b>.<br/>"
        "• <b>Bằng chứng trong Trace (File <code>traces/20261007-124552_782759d6_turn01_ff251ba4.jsonl</code>):</b><br/>"
        "  - Seq 4: Gọi <code>read_file('skills/refund-policy/SKILL.md')</code><br/>"
        "  - Seq 8: Gọi <code>list_files('data/policies')</code> → trả về danh sách file<br/>"
        "  - Seq 12: Gọi <code>read_file('data/policies/policy-before-oct.md')</code><br/>"
        "  - Seq 16: Gọi <code>read_file('data/policies/policy-from-oct.md')</code><br/>"
        "  - Seq 20: Gọi <code>read_file('skills/refund-policy/references/answer-template.md')</code><br/>"
        "  - Seq 23: Agent phản hồi đúng chuẩn template: Căn cứ <code>data/policies/policy-before-oct.md</code>, số ngày 8/7, kết luận <b>KHÔNG ĐỦ ĐIỀU KIỆN</b>.",
        style_body
    ))

    # Case B
    story.append(Paragraph("Trường hợp B: Khách hàng mua từ ngày đổi chính sách (02/10/2026)", style_h2))
    story.append(Paragraph(
        "• <b>Câu hỏi:</b> <i>\"Tôi mua ngày 02/10/2026, yêu cầu hoàn ngày 12/10/2026, chưa kích hoạt. Tôi có được hoàn không?\"</i><br/>"
        "• <b>Phân tích tính toán:</b> Ngày mua 02/10/2026 (>= 01/10/2026) → Chọn chính sách từ tháng 10 (giới hạn 14 ngày, không thu phí). Chênh lệch ngày lịch: 12 - 2 = <b>10 ngày</b>. Vì 10 ngày <= 14 ngày và chưa kích hoạt nên <b>ĐỦ ĐIỀU KIỆN</b>.<br/>"
        "• <b>Bằng chứng trong Trace (File <code>traces/20261007-124657_782759d6_turn02_92484153.jsonl</code>):</b><br/>"
        "  - Agent tận dụng context và tài liệu đã đọc, tính đúng số ngày là 10 ngày.<br/>"
        "  - Phản hồi dẫn căn cứ <code>data/policies/policy-from-oct.md</code>, kết luận <b>ĐỦ ĐIỀU KIỆN</b>, phí <b>Không thu phí hoàn tiền (0%)</b>.",
        style_body
    ))

    # Case Missing Info
    story.append(Paragraph("Trường hợp Thiếu thông tin bắt buộc", style_h2))
    story.append(Paragraph(
        "• <b>Câu hỏi:</b> <i>\"Tôi mua ngày 02/10/2026, muốn hoàn ngày 12/10/2026.\"</i> (Không nêu trạng thái kích hoạt).<br/>"
        "• <b>Bằng chứng trong Trace (File <code>traces/20261007-124817_782759d6_turn03_ffc8810f.jsonl</code>):</b><br/>"
        "  - Tuân thủ nghiêm ngặt Quy tắc bắt buộc tại Bước 1 của <code>SKILL.md</code>.<br/>"
        "  - Agent phản hồi đặt câu hỏi làm rõ về trạng thái kích hoạt của sản phẩm, <b>không tự ý giả định</b> là chưa kích hoạt và <b>chưa đưa ra kết luận sớm</b>.",
        style_body
    ))

    # Case Rename files
    story.append(Paragraph("Trường hợp Đổi tên file chính sách (Dynamic Discovery)", style_h2))
    story.append(Paragraph(
        "• Khi đổi tên tệp tin chính sách thành <code>policy-v1-old.md</code> và <code>policy-v2-new.md</code>, Agent mở cuộc trò chuyện mới vẫn tự động gọi <code>list_files('data/policies')</code>, tìm ra các file có tên mới và đưa ra kết luận hoàn toàn chính xác, không bị lỗi gãy đường dẫn.",
        style_body
    ))

    story.append(Spacer(1, 10))

    # SECTION 4
    story.append(Paragraph("4. Trả lời câu hỏi thảo luận cuối bài", style_h1))
    
    story.append(Paragraph("Câu hỏi 1: Vì sao cần tool để tìm file và skill để hướng dẫn chọn chính sách?", style_qa_q))
    story.append(Paragraph(
        "<b>Trả lời:</b><br/>"
        "1. <b>Cần Tool tìm file (<code>list_files</code>):</b> Môi trường tệp tin thực tế là động (dynamic environment). Số lượng và tên file có thể thay đổi liên tục. Tool giúp Agent có khả năng <i>nhận thức môi trường tại runtime (grounded perception)</i>, tự động khám phá các tài nguyên thực có thay vì suy đoán mò (hallucinate).<br/>"
        "2. <b>Cần Skill hướng dẫn (<code>refund-policy</code>):</b> Nghiệp vụ chọn chính sách có logic phức tạp (xét ngày hiệu lực, tính ngày lịch, kiểm tra kích hoạt, xử lý thiếu thông tin). Việc nhồi nhét toàn bộ vào System Prompt sẽ gây <i>phình to context (context bloat)</i> và giảm độ chính xác tổng thể. Skill áp dụng nguyên lý <i>tiết lộ lũy tiến (Progressive Disclosure)</i>: chỉ load khi người dùng yêu cầu, giúp bảo toàn context và tái sử dụng linh hoạt.",
        style_body
    ))

    story.append(Paragraph("Câu hỏi 2: Nếu agent chưa có tool tìm file, việc sửa prompt có giải quyết được yêu cầu đổi tên file không? Giải thích.", style_qa_q))
    story.append(Paragraph(
        "<b>Trả lời: HOÀN TOÀN KHÔNG.</b><br/>"
        "Prompt là dữ liệu tĩnh được thiết lập trước khi chạy. Nếu không có tool <code>list_files</code>, Agent hoàn toàn \"mù\" đối với cấu trúc thư mục thực tế trên ổ đĩa. Khi file bị đổi tên tại runtime, Agent không có bất kỳ cơ chế nào để biết tên file mới trừ khi con người lại can thiệp thủ công sửa prompt. Việc cố ép tên file vào prompt thực chất chỉ là hành vi hardcode, hoàn toàn thất bại khi file tiếp tục bị đổi tên hoặc có thêm file mới.",
        style_body
    ))

    story.append(Spacer(1, 10))

    # SECTION 5
    story.append(Paragraph("5. Danh mục bàn giao bài nộp", style_h1))
    story.append(Paragraph(
        "Các thành phần sau đã được triển khai hoàn chỉnh trong repository và sẵn sàng nộp bài:<br/>"
        " [x] <b>Tool <code>list_files</code>:</b> Cài đặt và đăng ký ở cả <code>stage-01-files</code> và <code>stage-02-skills</code>.<br/>"
        " [x] <b>Thư mục Skill <code>refund-policy/</code>:</b> Gồm <code>SKILL.md</code> và <code>references/answer-template.md</code>.<br/>"
        " [x] <b>Tài liệu chính sách:</b> <code>policy-before-oct.md</code> và <code>policy-from-oct.md</code> trong <code>workspace/data/policies/</code>.<br/>"
        " [x] <b>Hồ sơ Trace:</b> Các trace JSONL đầy đủ tại <code>stage-02-skills/traces/</code> chứng minh luồng gọi tool và xử lý.<br/>"
        " [x] <b>Báo cáo <code>analysis.md</code>:</b> Bản markdown chi tiết tại thư mục gốc và trong <code>stage-02-skills/</code>.<br/>"
        " [x] <b>Bản in báo cáo PDF:</b> File <code>Bao_Cao_Bai_Tap_Block_1_Tra_Cuu_Chinh_Sach.pdf</code> chuẩn bị nộp bài.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generated successfully:", filename)

if __name__ == "__main__":
    build_pdf()
