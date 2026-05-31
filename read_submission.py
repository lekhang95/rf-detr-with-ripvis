import docx

DOCX_PATH = r'C:\Users\ASUS\Downloads\rf-detr-with-ripvis\10411 Submission.docx'

doc = docx.Document(DOCX_PATH)
body = doc.element.body
items = []

for child in body.iterchildren():
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        para = docx.text.paragraph.Paragraph(child, doc)
        text = para.text.strip()
        if text:
            items.append(('para', text))
    elif tag == 'tbl':
        table = docx.table.Table(child, doc)
        rows_data = []
        for row in table.rows:
            row_cells = [cell.text.strip() for cell in row.cells]
            if any(c for c in row_cells):
                rows_data.append(row_cells)
        if rows_data:
            items.append(('table', rows_data))

for kind, content in items:
    if kind == 'para':
        print(f'[P] {content}')
    elif kind == 'table':
        print('[TABLE]')
        for row in content:
            print('  ' + ' | '.join(row))
