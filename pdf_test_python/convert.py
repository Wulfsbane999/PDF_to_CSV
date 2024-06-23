import fitz  # PyMuPDF
import csv
import PyPDF2
import csv
import re

'''
def pdf_to_csv(pdf_path, csv_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    
    # Open a CSV file for writing
    with open(csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Iterate through each page
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text = page.get_text("text")
            
            # Split the text into lines and then into cells
            for line in text.split('\n'):
                row = line.split()
                csv_writer.writerow(row)
    



pdf_path = 'C:\\Users\\1337_b0x\\Desktop\\pdf_test_python\\new_pdf.pdf'
csv_path = 'C:\\Users\\1337_b0x\\Desktop\\pdf_test_python\\new_csv.csv'
pdf_to_csv(pdf_path, csv_path)


'''


#open the pdf

pdf_path = 'C:\\Users\\1337_b0x\\Desktop\\pdf_test_python\\new_pdf.pdf'
pdf_file = open(pdf_path, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)


#extract text from each page of pdf
pdf_text = []
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    pdf_text.append(page.extract_text())

pdf_file.close()


#split text into lines
new_lines = []
#filter specific text patterns
page_number_pattern = re.compile(r'^\s*(Page\s*\d+|\d+|Page\s+\d+\s+of\s+\d+|Page\s*\d+\s*\/\s*\d+)\s*$', re.IGNORECASE)
specific_text_pattern = re.compile(r'rconlist_web-CurrentDate\.rpt|UNIT |SUITE ', re.IGNORECASE)
phone_number_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

for text in pdf_text:
    if text:
        lines = text.split('\n')
        filtered_lines = [line for line in lines if not page_number_pattern.match(line) and not specific_text_pattern.search(line)]
        new_lines.extend(filtered_lines)



#new row after phone number
processed_lines = []
current_row = []
for line in new_lines:
    current_row.append(line)
    if any(phone_number_pattern.search(cell) for cell in current_row):
        # Move phone numbers to the 2nd column
        for i in range(len(current_row)):
            if phone_number_pattern.search(current_row[i]):
                phone_number = current_row.pop(i)
                current_row.insert(1, phone_number)
                break
        while len(current_row) < 5:  # Ensure each row has exactly 5 columns
            current_row.append('')
        processed_lines.append(current_row)
        current_row = []
if current_row:  
    while len(current_row) < 5:  
        current_row.append('')
    processed_lines.append(current_row)



# define csv destination path
new_csv_path = 'C:\\Users\\1337_b0x\\Desktop\\pdf_test_python\\new_csv.csv'


# formating csv
'''
with open(new_csv_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for i in range(0, len(new_lines), 5):
        csv_writer.writerow(new_lines[i:i+5])

'''

with open(new_csv_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for row in processed_lines:
        csv_writer.writerow(row)
        





