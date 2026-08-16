import re
import hashlib

from langdetect import detect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from assignments.models import Assignment
from .extractors import extract_pdf_text, extract_docx_text


# Similarity check agadi text lai same format ma lyaune
def clean_text(text):
    if not text:
        return ""

    # Capital ra small letter ko farak hataune
    text = text.lower()

    # Punctuation ra unwanted characters hataune
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Extra spaces lai single space ma lyaune
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# Document English ma cha ki chaina check garne
def is_english(text):
    try:
        return detect(text) == "en"
    except Exception:
        # Language detect huna nasake document accept nagarne
        return False


# Exact duplicate check ko lagi document ko hash banaune
def get_document_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# File ko extension herera text extract garne
def get_text_from_file(file_path):
    file_path = file_path.lower()

    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)

    if file_path.endswith(".docx"):
        return extract_docx_text(file_path)

    raise ValueError("Only PDF and DOCX files are allowed.")


# Invalid assignment lai resubmission ko lagi mark garne
def reject_assignment(assignment, reason):
    assignment.status = "resubmission_required"
    assignment.similarity_percentage = reason
    assignment.save()


# Dui document bich ko similarity calculate garne
def calculate_similarity(text1, text2):
    if not text1 or not text2:
        return 0

    try:
        # Single word ra two-word phrase dubai compare garne
        vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
            ngram_range=(1, 2),
        )

        vectors = vectorizer.fit_transform([text1, text2])

        # Dui document ko vector similarity nikalne
        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2],
        )[0][0]

        similarity = round(similarity * 100, 2)

        # Sano similarity lai meaningful match namanne
        return similarity if similarity >= 15 else 0

    except Exception:
        return 0


# Document lai sentence haru ma divide garne
def split_into_sentences(text):
    if not text:
        return []

    sentences = re.split(r"[.!?]+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# Dui document ma similar sentences haru khojne
def find_matching_sentences(current_text, old_text):
    MATCH_THRESHOLD = 70
    matches = []

    current_sentences = split_into_sentences(current_text)
    old_sentences = split_into_sentences(old_text)

    for current_sentence in current_sentences:
        best_similarity = 0
        best_old_sentence = ""

        # Current sentence lai purano document ko sabai sentence sanga compare garne
        for old_sentence in old_sentences:
            similarity = calculate_similarity(
                clean_text(current_sentence),
                clean_text(old_sentence),
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_old_sentence = old_sentence

        # Threshold pugyo bhane matching sentence result ma rakhne
        if best_similarity >= MATCH_THRESHOLD:
            matches.append(
                {
                    "current_text": current_sentence,
                    "matched_text": best_old_sentence,
                    "similarity": round(best_similarity, 2),
                }
            )

    return matches


# Assignment ko overall plagiarism check handle garne
def analyze_assignment(assignment):
    try:
        # Uploaded file bata text nikalera clean garne
        current_text = clean_text(
            get_text_from_file(assignment.file.path)
        )

        if not current_text:
            reject_assignment(assignment, "Empty file")
            return "Empty file"

        # English document matra process garne
        if not is_english(current_text):
            reject_assignment(assignment, "Non-English")
            return "Non-English"

        # Dherai sano document ko result reliable nahuna sakcha
        if len(current_text.split()) < 50:
            reject_assignment(assignment, "Too Short")
            return "Too Short"

        # Current document ko hash banaune
        current_hash = get_document_hash(current_text)

        highest_similarity = 0
        matched_assignment = None

        # Same task, semester ra subject ko purano submissions matra compare garne
        previous_assignments = (
            Assignment.objects
            .filter(
                task__topic=assignment.task.topic,
                semester=assignment.semester,
                subject=assignment.subject,
            )
            .exclude(id=assignment.id)
            .exclude(student=assignment.student)
        )

        for old_assignment in previous_assignments:
            try:
                if not old_assignment.file:
                    continue

                # Purano assignment ko text extract garne
                old_text = clean_text(
                    get_text_from_file(old_assignment.file.path)
                )

                if not old_text:
                    continue

                old_hash = get_document_hash(old_text)

                # Hash same bhaye document exact duplicate ho
                if current_hash == old_hash:
                    highest_similarity = 100
                    matched_assignment = old_assignment
                    break

                # Exact duplicate nabhaye normal similarity check garne
                similarity = calculate_similarity(
                    current_text,
                    old_text,
                )

                # Ahile samma ko highest score store garne
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    matched_assignment = old_assignment

            except Exception:
                # Euta file process nabhaye aru file check gardai jane
                continue

        # Exact duplicate bhaye resubmission ko lagi pathaune
        if highest_similarity == 100:
            assignment.status = "resubmission_required"
            assignment.similarity_percentage = "100%"
        else:
            assignment.similarity_percentage = f"{highest_similarity}%"

        assignment.matched_assignment = matched_assignment
        assignment.save()

        return highest_similarity

    except Exception:
        # Unexpected error aaye assignment ko error state ma save garne
        assignment.similarity_percentage = "Error"
        assignment.matched_assignment = None
        assignment.save()

        return "Error"
