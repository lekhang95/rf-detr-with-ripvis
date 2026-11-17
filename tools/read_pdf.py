import fitz
import os

PDF_PATH = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\10411 Submission revies v1.pdf"

doc = fitz.open(PDF_PATH)
print(f"Tổng số trang: {doc.page_count}")
print("=" * 80)

for page_num, page in enumerate(doc, 1):
    text = page.get_text("text")
    print(f"\n{'='*80}")
    print(f"TRANG {page_num}")
    print(f"{'='*80}")
    for line in text.split("\n"):
        line = line.strip()
        if line:
            print(line)
