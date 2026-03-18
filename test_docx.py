from docx import Document
import sys

doc = Document("mdas/docs_final/priority_mdas/Prioritisation Framework for Government Digitisation  Automation - v03 - Approved - Priority MDAs.docx")
for i, table in enumerate(doc.tables):
    print(f"Table {i}: {len(table.rows)} rows, {len(table.columns)} columns")
    if len(table.rows) > 0:
        row = table.rows[0]
        print([cell.text for cell in row.cells])
