import dateutil
from pypdf import PdfReader, PdfWriter, PageObject
from argparse import ArgumentParser

DEFAULT_OUTPUT_FILE_NAME = "output.pdf"

def get_args() -> ArgumentParser.Namespace :
    parser = ArgumentParser(
        prog="dedupdf",
        description="Remove duplicated pages from PDF files (like animations in PDF export slides)"
    )

    parser.add_argument("filename")
    parser.add_argument("-o", "--output")

    return parser.parse_args()

def is_date(s: str) -> bool:
    try:
        dateutil.parser.parse(s)
        return True
    except ValueError:
        return False

def get_heading(page: PageObject) -> str:
    lines = page.extract_text().split("\n")
    if is_date(lines[0]):
        return lines[1]
    return lines[0]

def main():
    args = get_args()

    output_file_name = DEFAULT_OUTPUT_FILE_NAME
    if args.output != None:
        output_file_name = args.output

    reader = PdfReader(args.filename) 
    writer = PdfWriter(args.filename)

    page_numbers_to_delete = [] 

    previous_page = reader.pages[0]
    previous_heading = get_heading(previous_page)

    for i in range(1, len(reader.pages)):
        heading = get_heading(reader.pages[i])
        if heading == previous_heading:
            page_numbers_to_delete.append(i-1)
        previous_page = reader.pages[i]
        previous_heading = heading
    
    for i in range(len(page_numbers_to_delete)):
        # we need to subtract i, because the number of pages changes when we delete a page
       writer.remove_page(page_numbers_to_delete[i]-i) 

    writer.write(output_file_name)

main()