import fitz

from docx import Document


def extract_pdf_text(file_path):

    try:

        pdf = fitz.open(
            file_path
        )

        text = ""

        for page in pdf:

            text += page.get_text()

        pdf.close()

        if not text.strip():

            raise Exception(
                "PDF contains no readable text."
            )

        return text

    except Exception as e:

        raise Exception(
            f"PDF extraction failed: {str(e)}"
        )


def extract_docx_text(file_path):

    try:

        document = Document(
            file_path
        )

        text = "\n".join(

            paragraph.text

            for paragraph in document.paragraphs

        )

        if not text.strip():

            raise Exception(
                "DOCX contains no readable text."
            )

        return text

    except Exception as e:

        raise Exception(
            f"DOCX extraction failed: {str(e)}"
        ) 