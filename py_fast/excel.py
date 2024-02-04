from openpyxl import Workbook
from docx import Document
from openpyxl import load_workbook

def create_empty_excel_file(filename):
    """创建一个空的Excel文件"""
    workbook = Workbook()
    workbook.save(filename)

def create_empty_word_file(filename):
    """创建一个空的Word文件"""
    document = Document()
    document.save(filename)



def update_excel_cell(filename, cell, value):
    """
    修改指定Excel文件中指定单元格的内容。

    :param filename: Excel文件的路径。
    :param cell: 要修改的单元格，例如 'A1'。
    :param value: 新值。
    """
    # 加载Excel文件
    workbook = load_workbook(filename)
    # 选择活动工作表
    sheet = workbook.active
    # 修改指定单元格的值
    sheet[cell] = value
    # 保存文件
    workbook.save(filename)
