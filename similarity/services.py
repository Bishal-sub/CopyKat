import re
from langdetect import detect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from assignments.models import Assignment
from .extractors import extract_pdf_text, extract_docx_text


# Text lai compare garna sajilo hune gari common format ma lyaune
def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Document English language ma cha ki chaina check garne
def is_english(text):
    try:
        return detect(text) == "en"
    except Exception:
        return False


# File ko extension herera appropriate text extractor use garne
def get_text_from_file(file_path):
    file_path = str(file_path).lower()
    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)
    if file_path.endswith(".docx"):
        return extract_docx_text(file_path)
    raise ValueError("Only PDF and DOCX files are allowed.")


# Assignment valid chaina bhane resubmission ko lagi mark garne
def reject_assignment(assignment, reason):
    assignment.status = "resubmission_required"
    assignment.similarity_percentage = reason
    assignment.matched_assignment = None
    assignment.save(update_fields=["status", "similarity_percentage", "matched_assignment"])


# Dui ota document ko overall similarity percentage calculate garne
def calculate_similarity(text1, text2):
    if not text1 or not text2:
        return 0
    try:
        vectorizer = TfidfVectorizer(stop_words="english", lowercase=True, ngram_range=(1, 2))
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        similarity = round(similarity * 100, 2)
        return similarity if similarity >= 15 else 0
    except Exception:
        return 0


# Document lai sentence haru ma todne ra original text ko position pani save garne
def split_into_sentences(text):
    if not text:
        return []

    sentences = []
    pattern = re.compile(r".*?(?:[.!?](?=\s|$)|$)", re.DOTALL)

    for match in pattern.finditer(text):
        sentence = match.group().strip()
        if not sentence:
            continue

        leading_spaces = len(match.group()) - len(match.group().lstrip())
        trailing_spaces = len(match.group()) - len(match.group().rstrip())
        start = match.start() + leading_spaces
        end = match.end() - trailing_spaces

        sentences.append({
            "text": sentence,
            "start": start,
            "end": end,
        })

    return sentences


# Dui document ko similar sentence haru khojera dubai document ko position return garne
def find_matching_sentences(current_text, old_text):
    MATCH_THRESHOLD = 75

    current_sentences = split_into_sentences(current_text)
    old_sentences = split_into_sentences(old_text)

    current_valid = [(index, sentence) for index, sentence in enumerate(current_sentences) if len(sentence["text"].split()) >= 5]
    old_valid = [(index, sentence) for index, sentence in enumerate(old_sentences) if len(sentence["text"].split()) >= 5]

    if not current_valid or not old_valid:
        return []

    current_texts = [clean_text(sentence["text"]) for _, sentence in current_valid]
    old_texts = [clean_text(sentence["text"]) for _, sentence in old_valid]

    try:
        # Sabai sentence ko TF-IDF vector ekai choti banaune
        vectorizer = TfidfVectorizer(stop_words="english", lowercase=True, ngram_range=(1, 2))
        vectors = vectorizer.fit_transform(current_texts + old_texts)

        current_count = len(current_texts)
        current_vectors = vectors[:current_count]
        old_vectors = vectors[current_count:]

        # Sabai current ra old sentence ko similarity ekai choti calculate garne
        similarity_matrix = cosine_similarity(current_vectors, old_vectors)
    except Exception:
        return []

    sentence_matches = []
    used_old_positions = set()

    # Current document ko each sentence ko best unused old sentence khojne
    for current_position, (current_index, current_sentence) in enumerate(current_valid):
        similarities = similarity_matrix[current_position].copy()

        # Eutai old sentence lai dherai current sentence le use nagaros
        for used_position in used_old_positions:
            similarities[used_position] = -1

        best_old_position = similarities.argmax()
        best_similarity = similarities[best_old_position] * 100

        if best_similarity < MATCH_THRESHOLD:
            continue

        old_index, old_sentence = old_valid[best_old_position]
        used_old_positions.add(best_old_position)

        sentence_matches.append({
            "current_index": current_index,
            "old_index": old_index,
            "current_text": current_sentence["text"],
            "matched_text": old_sentence["text"],
            "start": current_sentence["start"],
            "end": current_sentence["end"],
            "matched_start": old_sentence["start"],
            "matched_end": old_sentence["end"],
            "similarity": round(best_similarity, 2),
        })

    # Current document ko order anusar matches sort garne
    sentence_matches.sort(key=lambda item: item["start"])

    matches = []

    # Each matched sentence ko separate highlight block return garne
    for match in sentence_matches:
        matches.append({
            "current_text": match["current_text"],
            "matched_text": match["matched_text"],
            "start": match["start"],
            "end": match["end"],
            "matched_start": match["matched_start"],
            "matched_end": match["matched_end"],
            "similarity": match["similarity"],
        })

    return matches


# Assignment ko complete similarity analysis handle garne
def analyze_assignment(assignment):
    try:
        # Uploaded file bata original/raw text nikalne
        raw_current_text = get_text_from_file(assignment.file.path)
        current_text = clean_text(raw_current_text)

        # File empty cha bhane reject garne
        if not current_text:
            reject_assignment(assignment, "Empty file")
            return {
                "similarity": 0,
                "document_text": raw_current_text,
                "matched_text": [],
                "matched_document_text": "",
                "matched_assignment": None,
                "reason": "Empty file",
            }

        # English document matra process garne
        if not is_english(current_text):
            reject_assignment(assignment, "Non-English")
            return {
                "similarity": 0,
                "document_text": raw_current_text,
                "matched_text": [],
                "matched_document_text": "",
                "matched_assignment": None,
                "reason": "Non-English",
            }

        # Dherai sano document ko similarity reliable nahuna sakcha
        if len(current_text.split()) < 50:
            reject_assignment(assignment, "Too Short")
            return {
                "similarity": 0,
                "document_text": raw_current_text,
                "matched_text": [],
                "matched_document_text": "",
                "matched_assignment": None,
                "reason": "Too Short",
            }

        highest_similarity = 0
        matched_assignment = None
        matched_text = []
        matched_document_text = ""

        # Same topic, semester ra subject ko previous assignments matra compare garne
        previous_assignments = Assignment.objects.filter(
            task__topic=assignment.task.topic,
            semester=assignment.semester,
            subject=assignment.subject,
        ).exclude(
            id=assignment.id
        ).exclude(
            student=assignment.student
        ).select_related(
            "student",
            "subject",
            "task",
        )

        # Purana assignments haru one by one compare garne
        for old_assignment in previous_assignments:
            try:
                if not old_assignment.file:
                    continue

                # Purano assignment ko original/raw text extract garne
                raw_old_text = get_text_from_file(old_assignment.file.path)
                old_text = clean_text(raw_old_text)

                if not old_text:
                    continue

                # Overall document similarity calculate garne
                similarity = calculate_similarity(current_text, old_text)

                # Highest similarity bhayeko document ko sentence matches matra store garne
                if similarity > highest_similarity:
                    sentence_matches = find_matching_sentences(raw_current_text, raw_old_text)
                    highest_similarity = similarity
                    matched_assignment = old_assignment
                    matched_text = sentence_matches
                    matched_document_text = raw_old_text

            except Exception:
                # Euta old file ma problem aaye pani aru file check garirakhne
                continue

        # Analysis ko result assignment ma save garne
        assignment.similarity_percentage = f"{highest_similarity}%"
        assignment.matched_assignment = matched_assignment
        assignment.save(update_fields=["similarity_percentage", "matched_assignment"])

        return {
            "similarity": highest_similarity,
            "document_text": raw_current_text,
            "matched_text": matched_text,
            "matched_document_text": matched_document_text,
            "matched_assignment": matched_assignment.id if matched_assignment else None,
        }

    except Exception:
        # Analysis ma unexpected error aaye assignment lai error status ma rakhne
        assignment.similarity_percentage = "Error"
        assignment.matched_assignment = None
        assignment.save(update_fields=["similarity_percentage", "matched_assignment"])

        return {
            "similarity": 0,
            "document_text": "",
            "matched_text": [],
            "matched_document_text": "",
            "matched_assignment": None,
            "reason": "Error",
        }