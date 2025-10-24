# SPDX-FileCopyrightText: 2025 Leon Maraite
#
# SPDX-License-Identifier: Apache-2.0

"""Main entry point for dedupdf.

Removes duplicated pages from PDF files (like animations in PDF export slides).

Since argparse is used you can refer to `--help` for parameter documentation.
"""

from argparse import ArgumentParser

from dedupdf import PdfHandler

DEFAULT_OUTPUT_FILE_NAME = "output.pdf"

def get_cli_args() -> ArgumentParser.Namespace:
    parser = ArgumentParser(
        prog="dedupdf",
        description="Remove duplicated pages from PDF files (like animations in PDF export slides)"
    )

    parser.add_argument("filename", help="Input PDF filename")
    parser.add_argument("-o", "--output", help="Output PDF filename")

    return parser.parse_args()

def main():
    args = get_cli_args()

    output_file_name = DEFAULT_OUTPUT_FILE_NAME
    if args.output != None:
        output_file_name = args.output

    pdf_handler = PdfHandler(args.filename, output_file_name)
    pdf_handler.deduplicate_pdf()
    pdf_handler.write()

main()