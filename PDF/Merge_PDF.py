# author='lwz'
# coding:utf-8
# !/usr/bin/env python3

from PyPDF4 import PdfFileReader, PdfFileWriter


def merge_pdfs(files, output):
    pdf_writer = PdfFileWriter()

    for file in files:
        pdf_reader = PdfFileReader(file)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as f:
        pdf_writer.write(f)
    print("{} write over".format(output))


if __name__ == '__main__':
    files = ['document1.pdf', 'document2.pdf']
    merge_pdfs(files, output='merged.pdf')