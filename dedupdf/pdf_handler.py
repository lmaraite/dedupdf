import dateutil
from pypdf import PdfReader, PdfWriter, PageObject

class PdfHandler:
    """
    Handles PDF reading, deduplication, and writing.

    Attributes:
        output_file_name (str): name of the file to write the modified PDF to
    """

    def __init__(self, input_file_name: str, output_file_name: str):
        """
        Initialize PdfHandler with input and output filenames.

        Args:
            input_file_name (str): Input PDF filename.
            output_file_name (str): Output PDF filename.
        """
        self.__reader = PdfReader(input_file_name)
        self.__writer = PdfWriter(input_file_name)
        self.output_file_name = output_file_name

    def deduplicate_pdf(self):
        """
        Remove duplicated pages from the PDF based on headings.
        """
        page_numbers_to_delete = []

        previous_page = self.__reader.pages[0]
        previous_heading = self.__get_heading(previous_page)
        previous_first_line = self.__get_first_line(previous_page)

        for i in range(1, len(self.__reader.pages)):
            heading = self.__get_heading(self.__reader.pages[i])
            first_line = self.__get_first_line(self.__reader.pages[i])
            if heading == previous_heading and first_line == previous_first_line:
                page_numbers_to_delete.append(i-1)
            previous_page = self.__reader.pages[i]
            previous_heading = heading
            previous_first_line = first_line
        
        for i in range(len(page_numbers_to_delete)):
            # we need to subtract i, because the number of pages changes when we delete a page
            self.__writer.remove_page(page_numbers_to_delete[i]-i) 

    def write(self):
        """
        Write the modified PDF to the output file.
        """
        self.__writer.write(self.output_file_name)

    def __is_date(self, s: str) -> bool:
        try:
            dateutil.parser.parse(s)
            return True
        except ValueError:
            return False

    def __get_heading(self, page: PageObject) -> str:
        lines = page.extract_text().split("\n")
        if self.__is_date(lines[0]) and len(lines) > 1:
            return lines[1]
        return lines[0]

    def __get_first_line(self, page: PageObject) -> str:
        lines = page.extract_text().split("\n")
        if self.__is_date(lines[0]) and len(lines) > 2:
            return lines[2]
        if len(lines) > 1:
            return lines[1]
        return lines[0]