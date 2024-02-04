from openpyxl import Workbook
from docx import Document

def create_empty_excel_file(filename):
    """创建一个空的Excel文件"""
    workbook = Workbook()
    workbook.save(filename)

def create_empty_word_file(filename):
    """创建一个空的Word文件"""
    document = Document()
    document.save(filename)
