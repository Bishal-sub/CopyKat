import fitz
from docx import Document


def extract_pdf_text(file_path):

    text = ""

    try:

        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

    except Exception:
        pass

    return text


def extract_docx_text(file_path):

    text = ""

    try:

        document = Document(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    except Exception:
        pass

    return text