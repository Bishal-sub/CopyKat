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
    file_path = file_path.lower()

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
    assignment.save()


# Dui ota document ko overall similarity percentage calculate garne
def calculate_similarity(text1, text2):
    if not text1 or not text2:
        return 0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
            ngram_range=(1, 2),
        )

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

    # Original/raw text ko exact position preserve garera sentence split garne
    pattern = re.compile(r".*?(?:[.!?](?=\s|$)|$)", re.DOTALL)

    for match in pattern.finditer(text):
        sentence = match.group().strip()

        if sentence:
            # Strip bhayeko text ko actual start/end position calculate garne
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


# Dui document ko similar sentence haru khojne
def find_matching_sentences(current_text, old_text):
    MATCH_THRESHOLD = 75

    current_sentences = split_into_sentences(current_text)
    old_sentences = split_into_sentences(old_text)
    sentence_matches = []

    # Current document ko each sentence check garne
    for current_index, current_sentence in enumerate(current_sentences):
        current_sentence_text = current_sentence["text"]

        if len(current_sentence_text.split()) < 5:
            continue

        best_similarity = 0
        best_old_index = None
        best_old_sentence = None

        # Current sentence lai old document ko sabai sentence sanga compare garne
        for old_index, old_sentence in enumerate(old_sentences):
            old_sentence_text = old_sentence["text"]

            if len(old_sentence_text.split()) < 5:
                continue

            similarity = calculate_similarity(
                clean_text(current_sentence_text),
                clean_text(old_sentence_text),
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_old_index = old_index
                best_old_sentence = old_sentence

        # 75% bhanda mathi ko matching sentence matra rakhne
        if best_similarity >= MATCH_THRESHOLD and best_old_index is not None:
            sentence_matches.append({
                "current_index": current_index,
                "old_index": best_old_index,
                "current_text": current_sentence_text,
                "matched_text": best_old_sentence["text"],
                "start": current_sentence["start"],
                "end": current_sentence["end"],
                "similarity": round(best_similarity, 2),
            })

    # Consecutive matching sentences lai एउटै block ma combine garne
    matching_blocks = []
    current_block = None

    for match in sentence_matches:
        if current_block is None:
            current_block = {
                "current_start": match["current_index"],
                "current_end": match["current_index"],
                "old_start": match["old_index"],
                "old_end": match["old_index"],
                "text_start": match["start"],
                "text_end": match["end"],
                "current_text": [match["current_text"]],
                "matched_text": [match["matched_text"]],
                "similarities": [match["similarity"]],
            }
            continue

        is_consecutive = (
            match["current_index"] == current_block["current_end"] + 1
            and match["old_index"] == current_block["old_end"] + 1
        )

        if is_consecutive:
            current_block["current_end"] = match["current_index"]
            current_block["old_end"] = match["old_index"]
            current_block["text_end"] = match["end"]
            current_block["current_text"].append(match["current_text"])
            current_block["matched_text"].append(match["matched_text"])
            current_block["similarities"].append(match["similarity"])
        else:
            matching_blocks.append(current_block)

            current_block = {
                "current_start": match["current_index"],
                "current_end": match["current_index"],
                "old_start": match["old_index"],
                "old_end": match["old_index"],
                "text_start": match["start"],
                "text_end": match["end"],
                "current_text": [match["current_text"]],
                "matched_text": [match["matched_text"]],
                "similarities": [match["similarity"]],
            }

    if current_block is not None:
        matching_blocks.append(current_block)

    matches = []

    # Only matched sentence/block return garne
    for block in matching_blocks:
        matches.append({
            "current_text": " ".join(block["current_text"]),
            "matched_text": " ".join(block["matched_text"]),
            "start": block["text_start"],
            "end": block["text_end"],
            "similarity": round(
                sum(block["similarities"]) / len(block["similarities"]),
                2,
            ),
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
                "matched_assignment": None,
                "reason": "Too Short",
            }

        highest_similarity = 0
        matched_assignment = None
        matched_text = []

        # Same topic, semester ra subject ko previous assignments matra compare garne
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

                # Matched sentence ko lagi raw text use garne
                sentence_matches = find_matching_sentences(
                    raw_current_text,
                    raw_old_text,
                )

                # Highest similarity bhayeko assignment ko result store garne
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    matched_assignment = old_assignment
                    matched_text = sentence_matches

            except Exception:
                # Euta old file ma problem aaye pani aru file check garirakhne
                continue

        assignment.similarity_percentage = f"{highest_similarity}%"
        assignment.matched_assignment = matched_assignment
        assignment.save()

        return {
            "similarity": highest_similarity,
            "document_text": raw_current_text,
            "matched_text": matched_text,
            "matched_assignment": matched_assignment.id if matched_assignment else None,
        }

    except Exception:
        assignment.similarity_percentage = "Error"
        assignment.matched_assignment = None
        assignment.save()

        return {
            "similarity": 0,
            "document_text": "",
            "matched_text": [],
            "matched_assignment": None,
            "reason": "Error",
        }