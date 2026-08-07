import fitz
from docx import Document


# PDF file bata text extract garne function
def extract_pdf_text(file_path: str) -> str:

    try:

        # PDF file open garne
        with fitz.open(file_path) as pdf:

            # sabai page ko text store garna list
            text_parts = []

            # PDF ko harek page ma loop chalaune
            for page in pdf:

                # page ko text nikalera extra space hataune
                page_text = page.get_text().strip()

                # khali page ignore garne
                if page_text:
                    text_parts.append(page_text)

        # sabai page ko text combine garne
        extracted_text = "\n".join(text_parts)

        # empty PDF ko case ma empty string return garne
        # analyze_assignment() le yo handle garxa
        return extracted_text

    except Exception as e:

        # PDF read garna error aayo vane exception throw garne
        raise RuntimeError(
            f"PDF extraction failed: {e}"
        ) from e


# DOCX file bata text extract garne function
def extract_docx_text(file_path: str) -> str:

    try:

        # DOCX file open garne
        document = Document(file_path)

        # paragraph haru ko text store garna list
        text_parts = []

        # document ko harek paragraph ma loop chalaune
        for paragraph in document.paragraphs:

            # paragraph ko text nikalera extra space hataune
            paragraph_text = paragraph.text.strip()

            # khali paragraph ignore garne
            if paragraph_text:
                text_parts.append(paragraph_text)

        # sabai paragraph ko text combine garne
        extracted_text = "\n".join(text_parts)

        # empty DOCX ko case ma empty string return garne
        # analyze_assignment() le yo handle garxa
        return extracted_text

    except Exception as e:

        # DOCX read garna error aayo vane exception throw garne
        raise RuntimeError(
            f"DOCX extraction failed: {e}"
        ) from e