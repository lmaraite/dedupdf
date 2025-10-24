# SPDX-FileCopyrightText: 2025 Leon Maraite
#
# SPDX-License-Identifier: Apache-2.0

import unittest
import os
from pypdf import PdfReader
from dedupdf import PdfHandler

class TestPdfHandler(unittest.TestCase):
    input_file_name = "tests/resources/test.pdf"
    output_file_name = "tests/resources/output.pdf"

    def tearDown(self):
        try:
            os.remove(self.output_file_name) 
        except:
            pass

    def test_deduplicate_pdf(self): 
        pdf_handler = PdfHandler(self.input_file_name, self.output_file_name)

        pdf_handler.deduplicate_pdf()
        pdf_handler.write()

        reader = PdfReader(self.output_file_name)
        pages = [page.extract_text().split("\n") for page in reader.pages]

        self.assertEqual(8, len(pages))
        self.assertEqual("Test Slides", pages[0][0])
        self.assertEqual("Test Slide 1", pages[1][0])
        self.assertEqual("Date Slide", pages[2][1])
        self.assertEqual("Groot", pages[3][0])
        self.assertEqual("Rocket", pages[4][0])
        self.assertEqual("Summary", pages[5][0])
        self.assertEqual("Summary", pages[6][0])
        self.assertEqual("", pages[7][0])

if __name__ == "__main__":
    unittest.main()