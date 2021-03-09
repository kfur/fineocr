
from enum import Enum

class DocExportType(Enum):
    DOCX = "Docx"
    PDF = "Pdf"
    PDFA = "Pdfa"
    EPUB = "Epub"
    XLSX = "Xlsx"
    TXT = "Text"


class DocLangType(Enum):
    English = "English"
    French = "French"
    German = "German"
    Russian = "Russian"
    Spanish = "Spanish"
    Chinese = "ChinesePrc"
    Japanese = "Japanese"
    Ukrainian = "Ukrainian"
    Korean = "Korean"
