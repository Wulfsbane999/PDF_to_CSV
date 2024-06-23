import fitz  # PyMuPDF

def is_bold(font_name):
    # may need to adjust it based on your specific PDF.
    return 'Bold' in font_name or 'bold' in font_name

def remove_bold_text(pdf_path, output_pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    output_document = fitz.open()  # New document to store the processed content

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        
        new_page = output_document.new_page(width=page.rect.width, height=page.rect.height)
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_name = span.get("font", "")
                        if not is_bold(font_name):
                            text_position = (span["bbox"][0], span["bbox"][1])
                            new_page.insert_text(text_position, span["text"], fontsize=span["size"], fontname='helv')

    output_document.save(output_pdf_path)
    print(f"Processed PDF saved as {output_pdf_path}")


pdf_path = 'C:\\Users\\1337_b0x\\Desktop\\pdf_test_python\\Building_Con_FL_6930.pdf'
output_pdf_path = 'C:\\Users\\1337_b0x\\Desktop\\pdf_test_python\\new_pdf.pdf'
remove_bold_text(pdf_path, output_pdf_path)
