import re

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from assignments.models import Assignment

from .extractors import (
    extract_pdf_text,
    extract_docx_text,
)


def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def get_text_from_file(file_path):

    file_path = file_path.lower()

    if file_path.endswith(".pdf"):

        return extract_pdf_text(
            file_path
        )

    elif file_path.endswith(".docx"):

        return extract_docx_text(
            file_path
        )

    return ""


def calculate_similarity(
    text1,
    text2
):

    if not text1 or not text2:
        return 0

    documents = [
        text1,
        text2,
    ]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100,2)


def analyze_assignment(
    assignment
):

    current_text = get_text_from_file(
        assignment.file.path
    )

    current_text = clean_text(
        current_text
    )

    if not current_text:

        assignment.similarity_percentage = 0

        assignment.save()

        return 0

    highest_similarity = 0

    previous_assignments = (
        Assignment.objects.exclude(
            id=assignment.id
        )
    )

    for old_assignment in previous_assignments:

        try:

            if not old_assignment.file:
                continue

            old_text = get_text_from_file(
                old_assignment.file.path
            )

            old_text = clean_text(
                old_text
            )

            similarity = calculate_similarity(
                current_text,
                old_text,
            )

            if similarity > highest_similarity:

                highest_similarity = similarity

        except Exception:

            continue

    assignment.similarity_percentage = (
        highest_similarity
    )

    assignment.save()

    return highest_similarity