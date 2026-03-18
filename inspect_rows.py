from docx import Document
import sys

doc_path = "mdas/docs_final/priority_mdas/Prioritisation Framework for Government Digitisation  Automation - v03 - Approved - Priority MDAs.docx"
doc = Document(doc_path)
table = doc.tables[0]

print("Row 19:")
print([cell.text for cell in table.rows[19].cells])

print("Row 23:")
print([cell.text for cell in table.rows[23].cells])
