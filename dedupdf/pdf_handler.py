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

        previous_page = Page(self.__reader.pages[0])

        for i in range(1, len(self.__reader.pages)):
            page = Page(self.__reader.pages[i])

            if page.heading == previous_page.heading and page.first_line == previous_page.first_line:
                page_numbers_to_delete.append(i-1)
            previous_page = page
        
        for i in range(len(page_numbers_to_delete)):
            # we need to subtract i, because the number of pages changes when we delete a page
            self.__writer.remove_page(page_numbers_to_delete[i]-i) 

    def write(self):
        """
        Write the modified PDF to the output file.
        """
        self.__writer.write(self.output_file_name)

class Page:
    """
    Represents a PDF page.

    Attributes:
        heading (str): The heading of the PDF page
        first_line (str): The first line of the PDF page
    """

    def __init__(self, page: PageObject):
        """
        Initialize Page  

        Args: 
            page (pypdf.PageObject): The object from which this page should be created
        """
        lines = page.extract_text().split("\n")
        num_lines = len(lines)

        if num_lines == 0:
            self.heading = ""
            self.first_line = ""
            return

        if num_lines == 1:
            self.heading = self.first_line = lines[0]
            return 
        
        if self.__is_date(lines[0]):
            self.heading = lines[1]
            self.first_line = lines[2] if num_lines > 2 else lines[0]
        else:
            self.heading = lines[0]
            self.first_line = lines[1]

    def __is_date(self, s: str) -> bool:
        try:
            dateutil.parser.parse(s)
            return True
        except ValueError:
            return False