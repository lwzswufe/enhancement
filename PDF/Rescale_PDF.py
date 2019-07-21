# author='lwz'
# coding:utf-8
# !/usr/bin/env python3

from PyPDF4 import PdfFileReader, PdfFileWriter

'''
页面坐标         mediaBox
上              page_obj.mediaBox.getUpperRight_y()
下              page_obj.mediaBox.getLowerLeft_y()
左              page_obj.mediaBox.getLowerLeft_x()
右              page_obj.mediaBox.getUpperRight_x()
                
调整页面到指定大小 page_obj.scaleTo(width, height)
'''


def get_page_scale(page_obj):
    '''
    获取页面大小
    :param page_obj:
    :return:
    '''
    width = page_obj.mediaBox.getUpperRight_x() - page_obj.mediaBox.getLowerLeft_x()
    height = page_obj.mediaBox.getUpperRight_y() - page_obj.mediaBox.getLowerLeft_y()
    return width, height


def rescale_pages_to_uniform_width(file, output, resample_page_num):
    '''

    :param file:
    :param output:
    :param resample_page_num: 采样前XX页 统计出现频次最多的宽度 若有相同频次 就选择较大者
    :return:
    '''
    pdf_reader = PdfFileReader(file)
    pdf_writer = PdfFileWriter()
    width_stat = {}
    max_freq = 0
    max_freq_width = 0
    for page_num in range(min(resample_page_num, pdf_reader.getNumPages())):
        page_obj = pdf_reader.getPage(page_num)
        width, height = get_page_scale(page_obj)
        print("page:{} width:{} height:{}".format(page_num, width, height))
        # 更新这种宽度页面出现的频次
        if width not in width_stat.keys():
            width_freq = 1
        else:
            width_freq = width_stat[width] + 1
        width_stat[width] = width_freq
        # 更新最常见页面 与 最常见页面出现的频次
        if width_freq > max_freq or \
            (width_freq == max_freq and max_freq_width < width):
                max_freq = width_freq
                max_freq_width = width
    print("set uniform width:{}".format(max_freq_width))

    for page_num in range(pdf_reader.getNumPages()):
        # Add each page to the writer object
        page_obj = pdf_reader.getPage(page_num)
        width, height = get_page_scale(page_obj)
        if width != max_freq_width:
            sx = float(max_freq_width / width)
            sy = sx
            page_obj.scale(sx, sy)
        pdf_writer.addPage(page_obj)

        # pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as f:
        pdf_writer.write(f)
    print("{} write over".format(output))


if __name__ == '__main__':
    file = 'document1.pdf'
    output_file = 'document2.pdf'
    rescale_pages_to_uniform_width(file, output_file, resample_page_num=10)



