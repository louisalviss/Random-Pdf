"""
random_text_generator.py
Sinh nội dung text ngẫu nhiên, vô nghĩa, không trùng lặp.

Cách dùng:
    python main.py -n 10              # Tạo 10 file PDF, số trang random 5-10
    python main.py -n 5 -p 8          # Tạo 5 file PDF, mỗi file 8 trang
    python main.py -p 7               # Tạo 1 file PDF 7 trang (mặc định)
    python main.py -p 5 -f txt        # Tạo 1 file TXT 5 trang
    python main.py -o tenfile.pdf     # Chỉ định tên file
    python main.py --seed 42          # Seed cố định
"""

import random
import argparse
import hashlib
import sys
import os
import re
from datetime import datetime

# ─────────────────────────────────────────────
# Bộ từ vựng ngẫu nhiên
# ─────────────────────────────────────────────

CONSONANTS = list("bcdfghjklmnprstvwxz")
VOWELS     = list("aeiou")
CLUSTERS   = ["tr", "bl", "fr", "gr", "cl", "fl", "pr", "st", "sp", "sk",
               "dr", "br", "cr", "gl", "sl", "sm", "sn", "sw", "th", "wh"]
ENDINGS    = ["", "n", "m", "t", "s", "k", "l", "r", "nd", "st", "nt", "ng", "ld", "lt"]

CONNECTORS = [
    "và", "nhưng", "tuy nhiên", "do đó", "vì vậy", "mặc dù", "hơn nữa",
    "bên cạnh đó", "trong khi đó", "đồng thời", "theo đó", "ngoài ra",
    "cụ thể là", "nói chung", "thực ra", "mặt khác", "dù sao",
    "therefore", "however", "furthermore", "meanwhile", "consequently",
    "in addition", "on the other hand", "as a result", "for instance",
]

FILLER_PHRASES = [
    "trong bối cảnh đó",
    "xét về mặt tổng thể",
    "theo quan điểm this",
    "dựa trên các yếu tố trên",
    "về cơ bản mà nói",
    "một cách khách quan",
    "nhìn từ góc độ khác",
    "tại thời điểm hiện tại",
    "từ góc nhìn đa chiều",
    "trong phạm vi nghiên cứu",
]

SECTION_TITLES = [
    "Phần {n}: Khảo sát ban đầu",
    "Chương {n}: Phân tích dữ liệu",
    "Mục {n}: Đánh giá kết quả",
    "Phần {n}: Tổng hợp thông tin",
    "Chương {n}: Nhận định chuyên sâu",
    "Mục {n}: Triển khai mô hình",
    "Phần {n}: Kết luận trung gian",
    "Chương {n}: Xem xét các trường hợp",
    "Mục {n}: So sánh và đối chiếu",
    "Phần {n}: Nghiên cứu bổ sung",
]

DOCUMENT_TITLES = [
    "Báo Cáo Phân Tích Hiệu Suất Hệ Thống Quản Lý Kho",
    "Tổng Hợp Kiến Thức Cơ Bản Về Mạng Máy Tính",
    "Nghiên Cứu Ứng Dụng AI Trong Nhận Diện Hình Ảnh",
    "Tài Liệu Hướng Dẫn Thiết Kế Cơ Sở Dữ Liệu Oracle",
    "Báo Cáo Đánh Giá Chất Lượng Dịch Vụ Logistics",
    "Phân Tích Thuật Toán Tối Ưu Đường Đi Ngắn Nhất",
    "Đề Tài Nghiên Cứu Hành Vi Người Dùng Trên Website",
    "Chuyên Đề An Toàn Thông Tin Trong Doanh Nghiệp",
    "Báo Cáo Thực Tập Hệ Thống Quản Lý Nhân Sự",
    "Tổng Quan Công Nghệ Điện Toán Đám Mây",
    "Phân Tích Dữ Liệu Doanh Thu Quý II Năm 2025",
    "Tài Liệu Kiểm Thử Phần Mềm Và Quy Trình QA",
    "Báo Cáo Khảo Sát Hiệu Năng API Nội Bộ",
    "Nghiên Cứu Giải Pháp Tự Động Hóa Quy Trình Sản Xuất",
    "Đồ Án Thiết Kế Ứng Dụng Quản Lý Công Việc",
    "Chuyên Đề Xử Lý Ảnh Và Nhận Dạng Ký Tự OCR",
    "Báo Cáo Phân Tích Tải Trọng Máy Chủ Linux",
    "Tài Liệu Học Tập Lập Trình Python Nâng Cao",
    "Nghiên Cứu So Sánh MongoDB Và PostgreSQL",
    "Báo Cáo Kiểm Tra Tính Ổn Định Của Hệ Thống RFID",
]

# ─────────────────────────────────────────────
# Sinh từ duy nhất
# ─────────────────────────────────────────────

_generated_words: set[str] = set()

def make_syllable() -> str:
    style = random.randint(0, 3)
    if style == 0:
        return random.choice(CONSONANTS) + random.choice(VOWELS) + random.choice(ENDINGS)
    elif style == 1:
        return random.choice(CLUSTERS) + random.choice(VOWELS) + random.choice(ENDINGS)
    elif style == 2:
        return random.choice(VOWELS) + random.choice(CONSONANTS) + random.choice(ENDINGS)
    else:
        return random.choice(CONSONANTS) + random.choice(VOWELS) + random.choice(VOWELS)

def make_word(min_syllables: int = 1, max_syllables: int = 3) -> str:
    for _ in range(200):
        n = random.randint(min_syllables, max_syllables)
        word = "".join(make_syllable() for _ in range(n))
        if word not in _generated_words:
            _generated_words.add(word)
            return word
    base = "".join(make_syllable() for _ in range(2))
    suffix = hashlib.md5(base.encode()).hexdigest()[:4]
    unique = base + suffix
    _generated_words.add(unique)
    return unique

# ─────────────────────────────────────────────
# Sinh câu / đoạn / phần
# ─────────────────────────────────────────────

def make_sentence(word_count_range=(8, 20)) -> str:
    n_words = random.randint(*word_count_range)
    words = []
    for i in range(n_words):
        if i > 0 and random.random() < 0.08:
            words.append(random.choice(CONNECTORS))
        if i > 0 and random.random() < 0.05:
            words.append(random.choice(FILLER_PHRASES))
            continue
        syl = random.choices([1, 2, 3], weights=[3, 5, 2])[0]
        words.append(make_word(syl, syl))
    sentence = " ".join(words)
    sentence = sentence[0].upper() + sentence[1:]
    ending = random.choices([".", ".", ".", "!", "?"], weights=[7, 7, 7, 2, 2])[0]
    return sentence + ending

def make_paragraph(sentence_count_range=(4, 8)) -> str:
    n = random.randint(*sentence_count_range)
    return " ".join(make_sentence() for _ in range(n))

TABLE_COLUMN_HEADERS = [
    ["STT", "Mã", "Tên", "Giá trị", "Ghi chú"],
    ["ID", "Thời gian", "Người thực hiện", "Kết quả", "Trạng thái"],
    ["Mã số", "Hạng mục", "Số lượng", "Đơn giá", "Thành tiền"],
    ["STT", "Chỉ tiêu", "Đơn vị", "Giá trị", "Tỷ lệ %"],
    ["Mã", "Tên đối tượng", "Ngày bắt đầu", "Ngày kết thúc", "Tiến độ"],
    ["STT", "Nhóm", "Phân loại", "Mô tả", "Đánh giá"],
]

def make_table() -> dict:
    """Sinh bảng ngẫu nhiên: {'headers': [str], 'rows': [[str]]}"""
    headers = random.choice(TABLE_COLUMN_HEADERS)
    n_cols = len(headers)
    n_rows = random.randint(3, 7)
    rows = []
    for i in range(n_rows):
        row = []
        for j in range(n_cols):
            if j == 0:
                row.append(str(i + 1))
            elif j == n_cols - 1:
                val = random.random()
                if val < 0.3:
                    row.append("Hoàn thành")
                elif val < 0.5:
                    row.append("Đang xử lý")
                elif val < 0.7:
                    row.append(f"{random.randint(50, 100)}%")
                else:
                    row.append(make_word(2, 2))
            elif "giá" in headers[j].lower() or "tiền" in headers[j].lower() or "thành" in headers[j].lower():
                row.append(f"{random.randint(10, 9999):,}")
            elif "lượng" in headers[j].lower() or "số" in headers[j].lower():
                row.append(str(random.randint(1, 500)))
            elif "thời" in headers[j].lower() or "ngày" in headers[j].lower():
                m = random.randint(1, 12)
                d = random.randint(1, 28)
                row.append(f"{d:02d}/{m:02d}/2025")
            else:
                row.append(make_word(1, 2))
        rows.append(row)
    return {"headers": headers, "rows": rows}

def make_section(section_number: int) -> dict:
    """Trả về dict {'title': str, 'paragraphs': [str], 'table': dict|None}"""
    title = random.choice(SECTION_TITLES).format(n=section_number)
    paragraphs = [make_paragraph() for _ in range(random.randint(2, 4))]
    table = make_table() if random.random() < 0.3 else None
    return {"title": title, "paragraphs": paragraphs, "table": table}

# ─────────────────────────────────────────────
# Sinh toàn bộ nội dung (dạng cấu trúc)
# ─────────────────────────────────────────────

WORDS_PER_PAGE = 500

def generate_content(pages: int = 7) -> dict:
    """Trả về dict chứa metadata + danh sách sections."""
    target_words = pages * WORDS_PER_PAGE
    title = random.choice(DOCUMENT_TITLES)
    sections = []
    total_words = 0
    section_num = 1

    while total_words < target_words:
        sec = make_section(section_num)
        word_count = sum(len(p.split()) for p in sec["paragraphs"]) + len(sec["title"].split())
        sections.append(sec)
        total_words += word_count
        section_num += 1

    return {
        "title": title,
        "pages": pages,
        "sections": sections,
        "total_words": total_words,
        "unique_words": len(_generated_words),
        "section_count": section_num - 1,
    }

def title_to_filename(title: str) -> str:
    """Chuyển tiêu đề thành tên file không dấu, viết thường, nối bằng gạch dưới."""
    s = title.lower()
    # Replace Vietnamese diacritics
    s = re.sub(r'[àáảãạăằắẳẵặâầấẩẫậ]', 'a', s)
    s = re.sub(r'[èéẻẽẹêềếểễệ]', 'e', s)
    s = re.sub(r'[ìíỉĩị]', 'i', s)
    s = re.sub(r'[òóỏõọôồốổỗộơờớởỡợ]', 'o', s)
    s = re.sub(r'[ùúủũụưừứửữự]', 'u', s)
    s = re.sub(r'[ỳýỷỹỵ]', 'y', s)
    s = re.sub(r'[đ]', 'd', s)
    s = re.sub(r'[^a-z0-9]+', '_', s)
    s = re.sub(r'_+', '_', s)
    s = s.strip('_')
    # Thêm hậu tố random 4 ký tự để không trùng
    suffix = hashlib.md5(f"{title}_{random.random()}".encode()).hexdigest()[:4]
    return f"{s[:45]}_{suffix}"

# ─────────────────────────────────────────────
# Xuất TXT
# ─────────────────────────────────────────────

def save_txt(content: dict, output_path: str):
    lines = []
    for sec in content["sections"]:
        lines.append(sec["title"])
        lines.append("=" * len(sec["title"]))
        lines.append("")
        for para in sec["paragraphs"]:
            lines.append(para)
            lines.append("")
        if sec.get("table"):
            tbl = sec["table"]
            col_widths = [len(h) for h in tbl["headers"]]
            for row in tbl["rows"]:
                for j, val in enumerate(row):
                    col_widths[j] = max(col_widths[j], len(val))
            sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
            header_line = "|" + "|".join(" {h:<{w}} ".format(h=h, w=col_widths[j]) for j, h in enumerate(tbl["headers"])) + "|"
            lines.append(sep)
            lines.append(header_line)
            lines.append(sep)
            for row in tbl["rows"]:
                row_line = "|" + "|".join(" {v:<{w}} ".format(v=v, w=col_widths[j]) for j, v in enumerate(row)) + "|"
                lines.append(row_line)
            lines.append(sep)
            lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ─────────────────────────────────────────────
# Xuất PDF (reportlab)
# ─────────────────────────────────────────────

def save_pdf(content: dict, output_path: str):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
        )
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import platform
    except ImportError:
        print("[LỖI] Chưa cài reportlab. Chạy: pip install reportlab", file=sys.stderr)
        sys.exit(1)

    font_name = "Helvetica"
    font_candidates = []

    system = platform.system()
    if system == "Linux":
        font_candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        ]
    elif system == "Windows":
        font_candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/times.ttf",
        ]
    elif system == "Darwin":
        font_candidates = [
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]

    for path in font_candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("CustomFont", path))
                font_name = "CustomFont"
                break
            except Exception:
                continue

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        fontName=font_name,
        fontSize=16,
        leading=22,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6,
        alignment=1,
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        fontName=font_name,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2c3e8c"),
        spaceBefore=18,
        spaceAfter=6,
        fontWeight="bold",
    )
    body_style = ParagraphStyle(
        "Body",
        fontName=font_name,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#222222"),
        spaceAfter=10,
        firstLineIndent=18,
        alignment=4,
    )

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title=content["title"],
        author="random_text_generator",
    )

    story = []

    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(content["title"], title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2c3e8c"), spaceAfter=16))

    for sec in content["sections"]:
        story.append(Paragraph(sec["title"], heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd"), spaceAfter=6))
        for para in sec["paragraphs"]:
            safe_para = para.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe_para, body_style))
        if sec.get("table"):
            tbl = sec["table"]
            data = [tbl["headers"]] + tbl["rows"]
            col_widths = [(11 * cm) / len(tbl["headers"])] * len(tbl["headers"])
            table = Table(data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e8c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), font_name),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("FONTNAME", (0, 1), (-1, -1), font_name),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            story.append(Spacer(1, 0.3 * cm))
            story.append(table)
            story.append(Spacer(1, 0.3 * cm))

    doc.build(story)

# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

def generate_one_file(pages: int, fmt: str, output_dir: str, output: str = None) -> str:
    """Sinh 1 file, trả về đường dẫn file đã lưu."""
    content = generate_content(pages=pages)
    if output is None:
        filename = title_to_filename(content["title"])
        output = f"{filename}.{fmt}"
    base, ext = os.path.splitext(output)
    if ext.lower() != f".{fmt}":
        output = f"{base}.{fmt}"

    output_path = os.path.join(output_dir, os.path.basename(output))
    if fmt == "pdf":
        save_pdf(content, output_path)
    else:
        save_txt(content, output_path)
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description="Sinh nội dung text ngẫu nhiên, vô nghĩa, không trùng lặp.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Số file muốn sinh (mặc định: 1)",
    )
    parser.add_argument(
        "-p", "--pages",
        type=int,
        default=None,
        choices=range(5, 11),
        metavar="[5-10]",
        help="Số trang mỗi file (mặc định: random 5-10)",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["txt", "pdf"],
        default="pdf",
        help="Định dạng xuất ra: pdf (mặc định) hoặc txt",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Tên file đầu ra (chỉ dùng khi -n=1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed để tái tạo kết quả",
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    # Tạo thư mục output/{timestamp} chung cho cả lượt chạy
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join("output", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    if args.count == 1 and args.output:
        pages = args.pages if args.pages else random.randint(5, 10)
        output = generate_one_file(pages, args.format, output_dir, args.output)
        print(f"[OK] Đã lưu: {output}", file=sys.stderr)
    else:
        if args.output and args.count > 1:
            print("[WARN] Tùy chọn -o bị bỏ qua khi tạo nhiều file.", file=sys.stderr)
        for i in range(args.count):
            pages = args.pages if args.pages else random.randint(5, 10)
            output = generate_one_file(pages, args.format, output_dir)
            print(f"[OK] [{i+1}/{args.count}] Đã lưu: {output} ({pages} trang)", file=sys.stderr)

if __name__ == "__main__":
    main()
