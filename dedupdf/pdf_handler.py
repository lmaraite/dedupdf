import dateutil
from pypdf import PdfReader, PdfWriter, PageObject

class PdfHandler:

    def __init__(self, input_file_name, output_file_name):
        self.reader = PdfReader(input_file_name)
        self.writer = PdfWriter(input_file_name)
        self.output_file_name = output_file_name

    def deduplicate_pdf(self):
        page_numbers_to_delete = []

        previous_page = self.reader.pages[0]
        previous_heading = self.__get_heading(previous_page)

        for i in range(1, len(self.reader.pages)):
            heading = self.__get_heading(self.reader.pages[i])
            if heading == previous_heading:
                page_numbers_to_delete.append(i-1)
            previous_page = self.reader.pages[i]
            previous_heading = heading
        
        for i in range(len(page_numbers_to_delete)):
            # we need to subtract i, because the number of pages changes when we delete a page
            self.writer.remove_page(page_numbers_to_delete[i]-i) 

    def write(self):
        self.writer.write(self.output_file_name)

    def __is_date(self, s: str) -> bool:
        try:
            dateutil.parser.parse(s)
            return True
        except ValueError:
            return False

    def __get_heading(self, page: PageObject) -> str:
        lines = page.extract_text().split("\n")
        if self.__is_date(lines[0]):
            return lines[1]
        return lines[0]
