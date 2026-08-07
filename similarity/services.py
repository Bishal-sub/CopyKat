# regular expression use garna import gareko
import re

# document ko unique hash banauna import gareko
import hashlib

# document ko language detect garna import gareko
from langdetect import detect

# text lai numerical vector ma convert garna import gareko
from sklearn.feature_extraction.text import TfidfVectorizer

# dui text ko similarity calculate garna import gareko
from sklearn.metrics.pairwise import cosine_similarity

# Assignment database model import gareko
from assignments.models import Assignment

# PDF ra DOCX bata text extract garne functions import gareko
from .extractors import (
    extract_pdf_text,
    extract_docx_text,
)


# comparison agadi text clean garne function
def clean_text(text):

    # text chaina vane empty string return garne
    if not text:
        return ""

    # sabai text lai lowercase ma convert garne
    text = text.lower()

    # punctuation ra special characters hataune
    # example: hello! -> hello
    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    # dherai space lai euta space ma convert garne
    # example: hello     world -> hello world
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # suru ra last ko extra space hataune
    return text.strip()



# document English language ma xa ki xaina check garne function
def is_english(text):

    try:

        # language detect garera English xa vane True return garne
        return detect(text) == "en"

    except Exception:

        # language detect fail vayo vane False return garne
        return False



# exact duplicate document detect garna hash banaune function
def get_document_hash(text):

    # SHA256 use garera unique hash generate garne
    # same text ko same hash hunxa
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()



# file ko extension check garera text extract garne function
def get_text_from_file(file_path):

    # file path lowercase ma convert garne
    # PDF ra pdf lai same treat garna
    file_path = file_path.lower()


    # file PDF xa vane PDF extractor use garne
    if file_path.endswith(".pdf"):

        return extract_pdf_text(
            file_path
        )


    # file DOCX xa vane DOCX extractor use garne
    if file_path.endswith(".docx"):

        return extract_docx_text(
            file_path
        )


    # PDF ra DOCX bahek aru file accept nagarne
    raise ValueError(
        "Only PDF and DOCX files are allowed."
    )



# invalid assignment reject garne helper function
def reject_assignment(assignment, reason):

    # assignment status rejected banaune
    assignment.status = "rejected"

    # invalid document ma similarity percentage chaina
    # tesko satta reason display garne
    assignment.similarity_percentage = reason

    # analysis complete vayo vanera mark garne
    assignment.analysis_completed = True

    # reject hune reason save garne
    assignment.analysis_error = reason

    # database ma update garne
    assignment.save()



# TF-IDF ra cosine similarity bata similarity calculate garne function
def calculate_similarity(text1, text2):

    # kunai text empty xa vane compare garna mildaina
    if not text1 or not text2:

        return 0


    try:

        # TF-IDF vectorizer create garne
        # stop_words le common words remove garxa
        # ngram le single word ra phrase dubai compare garxa
        vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
            ngram_range=(1, 2)
        )


        # text lai numerical vector ma convert garne
        vectors = vectorizer.fit_transform(
            [
                text1,
                text2
            ]
        )


        # dui vector bich similarity calculate garne
        # 1 = same
        # 0 = different
        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]


        # decimal value lai percentage ma convert garne
        similarity = round(
            similarity * 100,
            2
        )


        # dherai sano similarity ignore garne
        # random common words le aako match hatauna
        if similarity < 15:

            return 0


        # final similarity return garne
        return similarity


    except Exception:

        # error aaye system crash nahos
        return 0
# assignment ko plagiarism analysis garne main function
def analyze_assignment(assignment):

    try:

        # uploaded file bata text extract garera clean garne
        current_text = clean_text(
            get_text_from_file(
                assignment.file.path
            )
        )


        # document bata readable text niskena vane reject garne
        if not current_text:

            reject_assignment(
                assignment,
                "Empty"
            )

            return "Empty"



        # English document matra allow garne
        if not is_english(current_text):

            reject_assignment(
                assignment,
                "Non-English"
            )

            return "Non-English"



        # 50 words bhanda sano document accurate hudaina
        if len(current_text.split()) < 50:

            reject_assignment(
                assignment,
                "Too Short"
            )

            return "Too Short"



        # current document ko hash banaune
        # exact duplicate chito detect garna use hunxa
        current_hash = get_document_hash(
            current_text
        )


        # highest similarity store garne variable
        highest_similarity = 0


        # kun purano assignment sanga match vayo store garne
        matched_assignment = None



        # same semester ra level ko assignment matra database bata lyaune
        previous_assignments = Assignment.objects.filter(
            semester=assignment.semester,
            level=assignment.level
        ).exclude(
            id=assignment.id
        )


        # purano sabai assignment sanga compare garne
        for old_assignment in previous_assignments:


            try:

                # purano assignment ma file chaina vane skip garne
                if not old_assignment.file:

                    continue



                # purano assignment ko text extract ra clean garne
                old_text = clean_text(
                    get_text_from_file(
                        old_assignment.file.path
                    )
                )



                # old document empty xa vane compare nagarne
                if not old_text:

                    continue



                # old document ko hash generate garne
                old_hash = get_document_hash(
                    old_text
                )



                # same hash vayo vane exact duplicate ho
                if current_hash == old_hash:

                    # duplicate lai 100% similarity mark garne
                    highest_similarity = 100

                    # kun assignment duplicate ho save garne
                    matched_assignment = old_assignment

                    # aru compare garnu pardaina
                    break



                # duplicate chaina vane TF-IDF similarity calculate garne
                similarity = calculate_similarity(
                    current_text,
                    old_text
                )



                # ahile samma ko highest similarity save garne
                if similarity > highest_similarity:

                    highest_similarity = similarity

                    matched_assignment = old_assignment



            except Exception:

                # euta old assignment ma problem aaye pani
                # baki assignment compare continue garne
                continue



        # exact duplicate bhetiyo vane reject garne
        if highest_similarity == 100:

            # status rejected banaune
            assignment.status = "rejected"


            # duplicate ko similarity 100% dekhaune
            assignment.similarity_percentage = "100%"


            # duplicate ko message save garne
            assignment.analysis_error = (
                "Duplicate document detected."
            )


        else:

            # normal similarity percentage save garne
            assignment.similarity_percentage = (
                f"{highest_similarity}%"
            )


            # previous error clear garne
            assignment.analysis_error = ""



        # matched assignment database ma save garne
        assignment.matched_assignment = matched_assignment


        # analysis complete mark garne
        assignment.analysis_completed = True


        # final result save garne
        assignment.save()


        # similarity return garne
        return highest_similarity



    except Exception as e:


        # unexpected error handle garne
        # system crash huna nadine
        assignment.similarity_percentage = "Error"


        # match assignment clear garne
        assignment.matched_assignment = None


        # analysis complete bhayena vanera mark garne
        assignment.analysis_completed = False


        # error message save garne
        assignment.analysis_error = str(e)


        # database update garne
        assignment.save()


        # error return garne
        return "Error"    