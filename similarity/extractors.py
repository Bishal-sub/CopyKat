import fitz
from docx import Document


# PDF ko text analysis ko lagi extract garna
def extract_pdf_text(file_path: str) -> str:
    try:
        # PDF safely open garera pages access garna
        with fitz.open(file_path) as pdf:
            # Sabai valid page ko text temporarily store garna
            text_parts = []

            # PDF ko each page bata text collect garna
            for page in pdf:
                # Page ko unnecessary spaces hataera clean text lina
                page_text = page.get_text().strip()

                # Empty page lai final text ma include nagarna
                if page_text:
                    text_parts.append(page_text)

        # Sabai page ko text euta string ma combine garna
        extracted_text = "\n".join(text_parts)

        # Empty PDF bhaye empty string return garera caller lai handle garna dina
        return extracted_text

    except Exception as e:
        # PDF corrupt/readable nabhaye clear error provide garna
        raise RuntimeError(f"PDF extraction failed: {e}") from e


# DOCX ko text analysis ko lagi extract garna
def extract_docx_text(file_path: str) -> str:
    try:
        # DOCX document ko paragraphs access garna
        document = Document(file_path)

        # Valid paragraphs ko text temporarily store garna
        text_parts = []

        # Document ko each paragraph bata text collect garna
        for paragraph in document.paragraphs:
            # Paragraph ko unnecessary spaces hataera clean text lina
            paragraph_text = paragraph.text.strip()

            # Empty paragraph lai final text ma include nagarna
            if paragraph_text:
                text_parts.append(paragraph_text)

        # Sabai paragraphs ko text euta string ma combine garna
        extracted_text = "\n".join(text_parts)

        # Empty DOCX bhaye empty string return garera caller lai handle garna dina
        return extracted_text

    except Exception as e:
        # DOCX corrupt/readable nabhaye clear error provide garna
        raise RuntimeError(f"DOCX extraction failed: {e}") from e