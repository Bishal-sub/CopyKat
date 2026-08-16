# CopyKat

### Web-Based Assignment Similarity Checker

CopyKat is a web-based assignment similarity detection system built for academic institutions. It allows teachers to create assignments, students to submit PDF/DOCX files, and the system to compare submissions with previous submissions using **TF-IDF vectorization** and **Cosine Similarity**.

CopyKat also performs **exact duplicate detection using SHA-256 hashing** and stores the highest similarity match for teacher review.

> **Note:** CopyKat is a similarity analysis tool, not a definitive plagiarism detector. Similarity results should be reviewed by teachers or academic staff before making any academic decision.

---

## Features

### 👨‍🎓 Student

- Student authentication and role-based access
- View assignments assigned to their batch
- Submit assignments
- Upload PDF and DOCX files
- Prevent duplicate submissions for the same task
- View submission and similarity status
- Resubmit an assignment when the teacher requests resubmission
- One resubmission attempt with a two-day deadline

### 👨‍🏫 Teacher

- Teacher dashboard
- Create assignments for specific batches and subjects
- View submitted assignments
- Review student submissions
- View similarity percentages
- View matched assignments
- Add teacher remarks
- Accept or reject submissions
- Request resubmission after the first rejection
- Final rejection after a second failed submission

### 👨‍💼 Administrator

- Django Admin interface
- Manage users and system data
- Manage subjects
- Manage assignments and submissions
- Maintain application data through Django Admin

### 🔍 Similarity Detection

- PDF and DOCX text extraction
- Text cleaning and normalization
- English-language validation
- Minimum 50-word document validation
- SHA-256 exact duplicate detection
- TF-IDF vectorization
- Unigram and bigram comparison
- Cosine Similarity calculation
- Similarity percentage calculation
- 15% minimum similarity threshold
- Highest matching assignment detection
- Matched assignment storage
- Same topic, semester, and subject comparison
- Student's own previous submissions excluded from comparison

---

## 🛠️ Technology Stack

| Category        | Technology                            |
| --------------- | ------------------------------------- |
| Backend         | Python 3.11+, Django 6.0.7            |
| Database        | MySQL                                 |
| Frontend        | HTML5, CSS3, Bootstrap                |
| Similarity      | Scikit-learn                          |
| NLP             | TF-IDF, Cosine Similarity, langdetect |
| PDF Processing  | PyMuPDF                               |
| DOCX Processing | python-docx                           |
| Admin Interface | Django Jazzmin                        |
| Version Control | Git, GitHub                           |

---

## 📁 Project Structure

```text
CopyKat/
│
├── accounts/              # User authentication and account management
│
├── assignments/           # Assignment creation, submission and review
│
├── dashboard/             # Student and teacher dashboards
│
├── similarity/            # Assignment similarity analysis
│   ├── extractors.py      # PDF and DOCX text extraction
│   ├── services.py        # Text processing and similarity analysis
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── copykat_project/       # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/             # HTML templates
├── static/                # CSS, JavaScript and static assets
├── media/                 # Uploaded assignment files
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Bishal-sub/CopyKat.git
cd CopyKat
```

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create MySQL Database

```sql
CREATE DATABASE copykat_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key

DB_NAME=copykat_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Make sure the database configuration in `settings.py` reads these environment variables correctly.

### 6. Apply Migrations

```bash
python manage.py migrate
```

If you have modified models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create an Admin Account

```bash
python manage.py createsuperuser
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

---

## 🔎 Similarity Detection Workflow

```text
Student Uploads Assignment
            │
            ▼
     File Type Check
            │
            ▼
     Text Extraction
            │
            ▼
      Text Cleaning
            │
            ▼
    Language Validation
            │
            ▼
      50 Word Check
            │
            ▼
    SHA-256 Duplicate Check
            │
            ▼
 Same Topic + Semester + Subject
            │
            ▼
      TF-IDF Vectorization
            │
            ▼
     Cosine Similarity
            │
            ▼
 Highest Similarity Selected
            │
            ▼
       Save Result
            │
            ▼
      Teacher Review
```

### Process

1. A student uploads an assignment.
2. The system extracts text from the PDF or DOCX file.
3. The extracted text is converted to lowercase and cleaned.
4. The system checks whether the document is written in English.
5. Documents containing fewer than 50 words are rejected.
6. A SHA-256 hash is generated for exact duplicate detection.
7. The submission is compared only with assignments having the same:
   - Topic
   - Semester
   - Subject

8. The student's own previous submissions are excluded.
9. TF-IDF converts the documents into numerical vectors.
10. Cosine Similarity calculates the similarity between documents.
11. Similarity below 15% is treated as `0%`.
12. The highest similarity result is stored.
13. If an exact duplicate is detected, the similarity becomes `100%` and the assignment requires resubmission.
14. The teacher can review the result and accept, reject, or request resubmission.

---

## 📊 Similarity Calculation

CopyKat uses **TF-IDF** and **Cosine Similarity** for text comparison.

The system uses:

```text
TF-IDF
    +
Unigrams and Bigrams
    +
Cosine Similarity
    =
Similarity Percentage
```

The similarity result is stored as a percentage.

For example:

```text
Similarity: 72.45%
```

Similarity below **15%** is treated as:

```text
0%
```

An exact text duplicate is detected using SHA-256 and receives:

```text
100%
```

---

## 🎯 Assignment Comparison Rules

CopyKat does not compare every assignment against every other assignment.

A submission is compared only against previous assignments matching:

```text
Same Topic
     +
Same Semester
     +
Same Subject
```

The student's own previous submissions are excluded.

This helps prevent unrelated assignments from producing misleading similarity results.

---

## 👥 User Roles

### Student

Students can:

- View assignments for their admission batch
- Submit assignments
- View submission status
- View similarity results
- Resubmit assignments when required

### Teacher

Teachers can:

- Create assignments
- Select subjects they teach
- Assign tasks to specific batches
- View student submissions
- Review similarity results
- View matched assignments
- Add remarks
- Accept submissions
- Reject submissions
- Request resubmission

### Administrator

Administrators can:

- Manage users
- Manage subjects
- Manage assignments
- Manage submissions
- Manage application data
- Access Django Admin

---

## 📄 Supported Files

CopyKat currently supports:

```text
.pdf
.docx
```

PDF files are processed using **PyMuPDF**.

DOCX files are processed using **python-docx**.

> **Important:** The submission form currently allows `.doc` files in its browser `accept` attribute, but the similarity extraction service supports only **PDF and DOCX**. Therefore, `.doc` files should not be considered fully supported unless DOC extraction is added to the extraction service.

Scanned or image-only PDFs may not produce useful text because OCR is not currently implemented.

---

## 🔄 Resubmission System

When a teacher rejects a student's first submission, CopyKat can set the assignment to:

```text
resubmission_required
```

The student receives a **two-day resubmission deadline**.

Only one resubmission is allowed.

The second submission is marked as:

```text
submission_attempt = 2
```

If the second attempt is rejected, the assignment becomes:

```text
final_rejected
```

When a student resubmits:

- The previous uploaded file is removed.
- The new file is stored.
- The teacher remark is cleared.
- The previous review time is cleared.
- Similarity is reset.
- The matched assignment is cleared.
- Similarity analysis runs again.

---

## ⚠️ Limitations

- CopyKat performs **text-based similarity analysis**.
- It does not search the entire internet for plagiarism.
- Only PDF and DOCX files are supported by the extraction service.
- Scanned/image-only PDFs may require OCR.
- Documents must contain at least 50 words for analysis.
- The current language validation allows English documents only.
- Similarity is calculated using TF-IDF and Cosine Similarity rather than semantic embeddings.
- Similarity below 15% is treated as 0%.
- Similarity scores are indicators and are not proof of plagiarism.
- Large datasets may require additional performance optimization.
- Text formatting, images, diagrams, and other non-text content are not analyzed.
- Exact duplicate detection depends on the cleaned extracted text.

---

## 🔮 Future Enhancements

- Semantic similarity using Transformer/embedding models
- Highlight matching sentences and paragraphs
- Side-by-side document comparison
- OCR support for scanned documents
- Email notifications
- Similarity analytics and reports
- Celery + Redis background processing
- Vector database integration
- Multilingual similarity detection
- Full `.doc` file support
- AI-assisted academic integrity analysis

---

## 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/your-feature
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a Pull Request.

---

## 📜 License

No open-source license has currently been specified for this project.

---

## 👨‍💻 Author

**Bishal-sub**

**CopyKat — Assignment Similarity Checker**

Repository:

https://github.com/Bishal-sub/CopyKat

---

## ⭐ Support

If you find CopyKat useful, consider giving the repository a ⭐ on GitHub.

> **CopyKat — Submit. Compare. Review.**
