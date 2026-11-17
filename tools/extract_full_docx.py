"""
Extract FULL content từ DOCX bao gồm cả bảng (tables),
sau đó so sánh nội dung với PDF.
"""

import docx
import fitz
import re

DOCX_PATH = r"C:\Users\ASUS\Downloads\thesis\AIA double column-OTH_v2.docx"
PDF_PATH  = r"C:\Users\ASUS\Downloads\thesis\MDPI_Article_Template (7).pdf"

# ─────────────────────────────────────────────
# 1. Extract DOCX: paragraphs + tables
# ─────────────────────────────────────────────
def extract_docx_full(path):
    doc = docx.Document(path)
    
    # Lấy tất cả block theo thứ tự xuất hiện trong document
    # (paragraphs và tables xen kẽ nhau)
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    body = doc.element.body
    items = []

    for child in body.iterchildren():
        tag = child.tag.split('}')[-1]  # lấy tên tag bỏ namespace
        
        if tag == 'p':  # paragraph
            para = docx.text.paragraph.Paragraph(child, doc)
            text = para.text.strip()
            if text:
                items.append(('para', text))
        
        elif tag == 'tbl':  # table
            table = docx.table.Table(child, doc)
            rows_data = []
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells]
                # Bỏ các ô trống hoàn toàn
                if any(c for c in row_cells):
                    rows_data.append(row_cells)
            if rows_data:
                items.append(('table', rows_data))

    return items

# ─────────────────────────────────────────────
# 2. Extract PDF
# ─────────────────────────────────────────────
def extract_pdf_full(path):
    doc = fitz.open(path)
    lines = []
    for page in doc:
        text = page.get_text("text")
        for line in text.split("\n"):
            line = line.strip()
            if line:
                lines.append(line)
    return lines

# ─────────────────────────────────────────────
# 3. In DOCX content đầy đủ
# ─────────────────────────────────────────────
print("=" * 70)
print("DOCX FULL CONTENT (paragraphs + tables):")
print("=" * 70)

docx_items = extract_docx_full(DOCX_PATH)
docx_text_lines = []

for kind, content in docx_items:
    if kind == 'para':
        print(f"[P] {content}")
        docx_text_lines.append(content)
    elif kind == 'table':
        print("[TABLE]")
        for row in content:
            row_str = " | ".join(row)
            print(f"  {row_str}")
            # Thêm từng ô vào danh sách text để so sánh
            for cell in row:
                if cell:
                    docx_text_lines.append(cell)

# ─────────────────────────────────────────────
# 4. In PDF content
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("PDF CONTENT (first 200 lines for reference):")
print("=" * 70)
pdf_lines = extract_pdf_full(PDF_PATH)
for i, line in enumerate(pdf_lines[:200], 1):
    print(f"[{i:04d}] {line}")

# ─────────────────────────────────────────────
# 5. So sánh nội dung bảng DOCX vs PDF
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("DOCX TABLE CONTENTS:")
print("=" * 70)
for kind, content in docx_items:
    if kind == 'table':
        print("\n--- TABLE ---")
        for row in content:
            print("  | " + " | ".join(row))
