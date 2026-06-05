from PyPDF2 import PdfReader, PdfWriter

input_path = "test.pdf"
output_path = "test_from_59.pdf"

reader = PdfReader(input_path)
writer = PdfWriter()

start_page = 58  # zero-based index (59th page)

for page_num in range(start_page, len(reader.pages)):
    writer.add_page(reader.pages[page_num])

with open(output_path, "wb") as f:
    writer.write(f)

print(f"Saved pages 59 to end into: {output_path}")