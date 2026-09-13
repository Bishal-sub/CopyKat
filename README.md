# CopyKat
[![Django](https://img.shields.io/badge/Django-6.0.7-darkgreen)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange)](https://www.mysql.com/)

 ## 📖 Overview

 **CopyKat** is a web-based academic assignment management and similarity detection platform built with Django.

 The platform allows students to submit assignments in **PDF** and **DOCX** formats and allows teachers to review those submissions for textual similarity against previous submissions.

 CopyKat uses classical NLP and machine-learning techniques, primarily:

 - TF-IDF vectorization
- Word and bigram features
- Cosine similarity
- Sentence-level similarity matching
- English-language validation
- Document text extraction

 The system identifies the previous submission with the highest textual similarity and presents the relationship to teachers during the review process.

 > **Important:** CopyKat provides similarity evidence for academic review. A similarity score does not by itself prove plagiarism or establish the direction of copying.

---

 ## ✨ Key Features

 ### 🔍 Assignment Similarity Detection

 CopyKat analyzes submitted assignments through a multi-stage pipeline:

 - PDF text extraction
- DOCX text extraction
- Text cleaning and normalization
- English-language validation
- Minimum content validation
- Comparable-submission selection
- TF-IDF vectorization
- Word and bigram analysis
- Cosine similarity
- Highest-match identification
- Sentence-level similarity detection
- Matching-text information
- Similarity result storage

---

 ### 👨‍🎓 Student Management

 Students can:

 - Register an account
- Verify their email through OTP
- Provide academic information
- Provide admission-year information
- Provide department and level information
- Provide student barcode information
- Upload a profile photo
- Log in securely
- Recover their password
- View available assignment tasks
- Submit PDF/DOCX assignments
- View submission status
- View similarity results
- View teacher feedback
- Use an allowed resubmission
- Submit a second attempt when permitted

---

 ### 👨‍🏫 Teacher Management

 Teachers can:

 - Create assignment tasks
- Define assignment topics
- Define assignment descriptions
- Select department
- Select level
- Select semester
- Select subject
- Configure assignment visibility
- Configure submission deadlines
- View assignment submissions
- Review student submissions
- Review similarity scores
- Identify the matched student submission
- Compare the current submission with the matched submission
- Inspect matching text
- Review sentence-level similarity
- Accept submissions
- Reject submissions
- Request permitted resubmissions
- Add teacher remarks
- Review resubmitted assignments

---

 ### 🔎 Identify Potential Copying Relationships

 CopyKat does more than display a single similarity percentage.

 When a submitted assignment has a sufficiently similar previous submission, the system stores the matched assignment and makes the associated student available to the teacher-review workflow.

 A review relationship can therefore look like:

```
Current Submission
       │
       │ 82% similarity
       ▼
Most Similar Previous Submission
       │
       ▼
Matched Student
```

 The teacher can investigate:

 - Current student
- Current submission
- Similarity percentage
- Matched student
- Matched previous submission
- Matching passages
- Sentence-level similarity
- Assignment context

 ### ⚠️ Important Interpretation

 The **matched student** is the student associated with the previous submission that produced the highest similarity according to CopyKat's algorithm.

 This does **not automatically prove** that:

```
Student A copied Student B
```

 or:

```
Student B copied Student A
```

 The algorithm establishes a **textual similarity relationship**. The teacher should determine the direction and academic significance of the copying after reviewing the submissions, timestamps, citations, context, and other evidence.

---

 ## 🧑‍🏫 Teacher Review Interface

 The teacher review page is a central part of CopyKat.

 The current review template provides a dedicated assignment-review interface and is designed around the similarity result produced for the submission.

 The review workflow can expose information including:

 - Assignment information
- Student information
- Submission information
- Similarity percentage
- Matched assignment
- Matched student's information
- Matching text
- Sentence-level matching
- Review actions
- Teacher remarks
- Submission status

 The interface is implemented as a Django template and uses the shared CopyKat Bootstrap-based frontend.  GitHub+1

---

 ## 🧠 Similarity Detection Pipeline

```
                Student
                   │
                   │ PDF / DOCX
                   ▼
          ┌──────────────────┐
          │ File Validation  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Text Extraction  │
          │ PDF / DOCX       │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Text Cleaning    │
          │ & Normalization  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Language &       │
          │ Content Check    │
          └────────┬─────────┘
                   │
                   ▼
       ┌──────────────────────────┐
       │ Find Comparable Previous  │
       │ Submissions               │
       └────────────┬─────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │ TF-IDF           │
          │ Vectorization    │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Cosine           │
          │ Similarity       │
          └────────┬─────────┘
                   │
                   ▼
       ┌──────────────────────────┐
       │ Highest Similarity Match │
       └────────────┬─────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │ Sentence-Level   │
          │ Matching         │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Store Result     │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Teacher Review   │
          └──────────────────┘
```

---

 ## 📄 Supported Documents

 CopyKat currently supports:

 | Format | Processing |
| --- | --- |
| PDF | Text extraction with PyMuPDF |
| DOCX | Paragraph extraction with python-docx |

 PyPDF2 is also included in the project's dependency set.

 The current implementation focuses on extracting textual content. It is not a complete OCR, image-analysis, or layout-aware document-analysis system.

---

 ## 🧹 Text Processing

 Before similarity calculation, extracted text is cleaned and normalized.

 The processing includes:

 - Lowercase conversion
- Special-character normalization
- Whitespace normalization
- Text cleanup
- Sentence extraction for detailed matching

 The goal is to reduce superficial formatting differences before comparison.

---

 ## ✅ Document Validation

 CopyKat validates submitted content before similarity analysis.

 The current similarity workflow includes:

 - Text extraction validation
- Empty-content detection
- English-language validation
- Minimum word-count validation
- File validation

 The similarity service requires sufficient textual content before performing comparison.

---

 ## 📚 Comparison Scope

 CopyKat does not simply compare a submission against unrelated documents in the entire database.

 Comparable submissions are selected according to the academic context of the assignment.

 The similarity engine considers previous submissions associated with the relevant:

 - Topic
- Semester
- Subject

 The current student's own submission is excluded from the comparison.

 This makes the comparison more relevant to the assignment being evaluated.

---

 ## 📊 TF-IDF Similarity

 CopyKat uses TF-IDF to represent assignment text numerically.

 The current vectorizer uses:

```
TfidfVectorizer(
    stop_words="english",
    lowercase=True,
    ngram_range=(1, 2)
)
```

 The `(1, 2)` n-gram configuration allows the system to consider:

 - Single words
- Two-word combinations

 For example:

```
machine
learning
machine learning
```

 can all contribute to the document representation.

---

 ## 📐 Cosine Similarity

 After TF-IDF vectorization, CopyKat compares document vectors using cosine similarity.

 Conceptually:

```
                     A · B
cosine(A, B) = ───────────────
               ||A|| × ||B||
```

 The resulting score is represented as a similarity percentage for teacher review.

---

 ## 📝 Sentence-Level Matching

 CopyKat also performs a more detailed comparison after identifying the strongest document-level match.

 The sentence-level process includes:

 1. Splitting documents into sentences
2. Filtering very short sentences
3. Creating TF-IDF representations
4. Comparing sentence vectors
5. Applying a similarity threshold
6. Recording matching passages
7. Presenting the matching information for teacher review

 The current sentence matching threshold is approximately:

```
75%
```

 This allows teachers to move from:

```
Overall similarity: 82%
```

 to:

```
Potential matching sentence
        ↕
Potential matching sentence

Sentence similarity: 91%
```

 This is particularly useful when investigating specific passages.

---

 ## 📈 Understanding Similarity Scores

 A similarity percentage represents textual similarity according to the implemented algorithm.

 For example:

```
Similarity: 82%
```

 means that CopyKat detected a high level of textual overlap between the compared submissions.

 It does not independently establish:

 - Plagiarism
- Intentional copying
- Original authorship
- Direction of copying
- Improper citation
- Academic misconduct

 A teacher or institution should make the final academic decision.

---

 ## 🔄 Assignment Lifecycle

```
Teacher creates assignment
            │
            ▼
Assignment becomes available
            │
            ▼
Student views assignment
            │
            ▼
Student submits PDF/DOCX
            │
            ▼
Document validation
            │
            ▼
Similarity analysis
            │
            ▼
Similarity result stored
            │
            ▼
Teacher reviews submission
            │
       ┌────┼───────────────┐
       │    │               │
       ▼    ▼               ▼
    Accept  Resubmit      Reject
             │
             ▼
      Student submits
       second attempt
             │
             ▼
      Similarity analysis
             │
             ▼
       Teacher review
```

 The application supports an initial submission and a permitted resubmission workflow.

---

 ## 👤 Authentication

 CopyKat uses a custom Django user system.

 The account interface includes pages for:

 - Login
- Registration
- Email verification
- Password recovery
- Reset OTP verification
- Password reset
- Teacher password change

 The frontend templates use a shared `base.html` layout with Bootstrap 5, Font Awesome, Google Fonts, and Django template inheritance.  GitHub+3

---

 ## 🔐 OTP Verification

 The account system uses OTP-based workflows for:

 - Email verification
- Password reset

 This allows student accounts to be verified before normal account usage and provides a separate verification step for password recovery.

---

 ## 🎨 User Interface

 CopyKat currently uses a Django server-rendered interface.

 The frontend is built with:

 - Django Templates
- HTML5
- CSS
- Bootstrap 5
- JavaScript
- Font Awesome
- Plus Jakarta Sans
- Playfair Display

 The shared base template loads Bootstrap 5.3.7, Font Awesome 6.7.2, and Google Fonts.  GitHub

 The homepage provides the public-facing CopyKat introduction and application entry points, while authenticated interfaces are separated according to the user's role.  GitHub

---

 ## 🗂️ Template Structure

 The repository currently contains Django templates covering authentication, assignment management, student submission, resubmission, assignment viewing, and teacher review.

 ### Account Templates

```
accounts/templates/
├── forgot_password.html
├── login.html
├── register.html
├── reset_password.html
├── teacher_change_password.html
├── verify_email.html
└── verify_reset_otp.html
```

 ### Assignment Templates

```
assignments/templates/
├── give_assignment.html
├── resubmit_assignment.html
├── submit_assignment.html
├── teacher_review.html
└── view_assignments.html
```

 ### Shared Templates

```
templates/
├── base.html
└── home.html
```

 The assignment templates cover teacher task creation, student submission, resubmission, assignment listing, and teacher review.  GitHub

---

 ## 🏗️ Project Structure

```
CopyKat/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   └── migrations/
│
├── assignments/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   └── migrations/
│
├── dashboard/
│   ├── views.py
│   └── urls.py
│
├── similarity/
│   ├── services.py
│   ├── extractors.py
│   ├── views.py
│   └── urls.py
│
├── copykat_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/
│   ├── base.html
│   └── home.html
│
├── manage.py
├── requirements.txt
└── README.md
```

---

 ## 🧩 Application Architecture

```
                         CopyKat
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
      Accounts          Assignments       Dashboard
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                   Similarity Engine
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
       Document Extraction          Text Processing
              │                           │
              └─────────────┬─────────────┘
                            │
                            ▼
                         TF-IDF
                            │
                            ▼
                   Cosine Similarity
                            │
                            ▼
                 Sentence-Level Matching
                            │
                            ▼
                     Teacher Review
                            │
                            ▼
                         MySQL
```

---

 ## 🗄️ Core Data Relationships

 Conceptually, the academic workflow is structured around:

```
Department
    │
    └── Subject
           │
           └── Teacher Task
                  │
                  └── Assignment
                        │
                        ├── Student
                        ├── Submission
                        └── Matched Assignment
```

 Similarity results connect a submitted assignment with its most similar previous assignment.

 This relationship allows the teacher-review interface to identify the matched submission and associated student.

---

 ## 🛠️ Technology Stack

 | Category | Technology |
| --- | --- |
| Backend | Python |
| Framework | Django 6.0.7 |
| Database | MySQL 8.0+ |
| ORM | Django ORM |
| Admin | Django Jazzmin |
| Frontend | Django Templates |
| UI Framework | Bootstrap 5 |
| Icons | Font Awesome |
| Fonts | Google Fonts |
| PDF Processing | PyMuPDF |
| PDF Library | PyPDF2 |
| DOCX Processing | python-docx |
| NLP | scikit-learn |
| Numerical Computing | NumPy |
| Scientific Computing | SciPy |
| Language Detection | langdetect |
| Regex Processing | regex |
| Image Processing | Pillow |
| Configuration | python-decouple / python-dotenv |

 The currently pinned dependencies include Django 6.0.7, django-jazzmin 3.0.5, scikit-learn 1.9.0, scipy 1.18.0, NumPy 2.5.1, PyMuPDF 1.28.0, python-docx 1.2.0, Pillow 12.3.0, and MySQL client 2.2.8.  GitHub

---

 ## 📋 Requirements

 ### Recommended Environment

 - Python 3.12+
- MySQL 8.0+
- Git
- pip
- Python virtual environment

 > The README badge intentionally shows `Python 3.8+` for project labeling, but the current pinned **Django 6.0.7** dependency should be used with a Python version supported by Django 6. For a new installation, Python 3.12\+ is recommended.

---

 ## 🚀 Installation

 ### 1\. Clone the Repository

```
git clone https://github.com/Bishal-sub/CopyKat.git
cd CopyKat
```

 ### 2\. Create a Virtual Environment

 #### Linux / macOS

```
python3 -m venv venv
source venv/bin/activate
```

 #### Windows

```
python -m venv venv
venv\Scripts\activate
```

 ### 3\. Upgrade pip

```
python -m pip install --upgrade pip
```

 ### 4\. Install Dependencies

```
pip install -r requirements.txt
```

---

 ## 🗄️ MySQL Configuration

 Create the database:

```
CREATE DATABASE copykat;
```

 Create a dedicated database user if required:

```
CREATE USER 'copykat_user'@'localhost'
IDENTIFIED BY 'your-secure-password';

GRANT ALL PRIVILEGES ON copykat.*
TO 'copykat_user'@'localhost';

FLUSH PRIVILEGES;
```

---

 ## 🔐 Environment Variables

 Create a `.env` file in the project root.

 Example:

```
SECRET_KEY=change-this-to-a-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=copykat
DB_USER=copykat_user
DB_PASSWORD=your-secure-password
DB_HOST=127.0.0.1
DB_PORT=3306

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

 Never commit real credentials or secret keys to Git.

 For production:

```
DEBUG=False
```

 Use a strong, randomly generated `SECRET_KEY`.

---

 ## 🔄 Database Migration

 Run:

```
python manage.py makemigrations
python manage.py migrate
```

---

 ## 👤 Create an Administrator

```
python manage.py createsuperuser
```

 Follow Django's prompts.

 Then access the Django administration interface:

```
http://127.0.0.1:8000/admin/
```

---

 ## ▶️ Run the Application

 Start the development server:

```
python manage.py runserver
```

 Open:

```
http://127.0.0.1:8000/
```

---

 ## 🧪 Testing

 Run Django's test suite:

```
python manage.py test
```

 Run Django configuration checks:

```
python manage.py check
```

 Recommended development workflow:

```
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver
```

---

 ## 📤 Assignment Submission

 The student submission process is:

```
Select Assignment
       │
       ▼
Upload PDF/DOCX
       │
       ▼
Validate File
       │
       ▼
Extract Text
       │
       ▼
Validate Content
       │
       ▼
Run Similarity Analysis
       │
       ▼
Save Similarity Result
       │
       ▼
Teacher Review
```

 The project has dedicated templates for both initial submissions and permitted resubmissions.  GitHub+2

---

 ## 🔁 Resubmission

 CopyKat supports a controlled resubmission workflow.

 A teacher can request a permitted resubmission when the first submission requires another attempt.

 The student can then:

 ## 🚀 Installation

 ### 1\. Clone the Repository

```
git clone https://github.com/Bishal-sub/CopyKat.git
cd CopyKat
```

 ### 2\. Create a Virtual Environment

 #### Linux / macOS

 1. Open the resubmission interface
2. Upload a new document
3. Submit the second attempt
4. Have the new submission analyzed
5. Receive another teacher review

 The resubmission process is represented by a dedicated Django template.  GitHub

---

 ## 👨‍🏫 Teacher Assignment Creation

 Teachers can create assignment tasks through the assignment-management interface.

 The task-creation interface supports academic information and assignment configuration such as:

 - Department
- Level
- Semester
- Subject
- Topic
- Description
- Visibility
- Deadline

 The corresponding template is `give_assignment.html`.  GitHub

---

 ## 👨‍🎓 Student Assignment View

 Students have a dedicated assignment-view interface for seeing assignments available to them.

 The assignment list separates the student-facing task discovery and submission workflow from teacher-side assignment management.  GitHub

---

 ## 📁 File Handling

 Assignment files are uploaded through Django's file-handling system.

 Supported assignment formats:

```
.pdf
.docx
```

 Uploaded academic documents should:

 - Not be committed to Git
- Be stored securely
- Be validated before processing
- Have reasonable upload-size restrictions
- Never be treated as executable files

---

 ## ⚠️ Current Limitations

 ### 1\. TF-IDF Is Lexical

 TF-IDF primarily measures word and phrase overlap.

 It may fail to recognize strongly paraphrased content where the wording is substantially different.

 For example:

```
Machine learning improves prediction accuracy.
```

 and:

```
Machine learning can increase predictive performance.
```

 may have lower lexical similarity despite being semantically related.

---

 ### 2\. Similarity Does Not Prove Plagiarism

 A high score is an indicator for investigation, not an automatic academic judgment.

---

 ### 3\. Direction of Copying Is Not Automatically Proven

 CopyKat can identify:

```
Current Student
      ↓
Most Similar Previous Submission
      ↓
Matched Student
```

 but similarity alone cannot prove which student was the original author.

 The teacher must make that determination.

---

 ### 4\. English-Focused Analysis

 The current similarity workflow is designed around English-language validation.

 Multilingual similarity detection is a future improvement.

---

 ### 5\. Document Text Only

 The similarity engine focuses on extracted textual content.

 Images, scanned pages, complex layouts, diagrams, and other non-textual information are not fully represented by the current text-comparison pipeline.

---

 ### 6\. Synchronous Similarity Analysis

 Similarity processing is currently closely coupled to assignment submission.

 For a large institutional deployment, long-running analysis should eventually move to background processing.

---

 ## 🚧 Future Roadmap

 ### Phase 1 — Current System

 - [x] Django web application
- [x] Student accounts
- [x] Teacher accounts
- [x] Admin management
- [x] OTP email verification
- [x] Password recovery
- [x] Assignment creation
- [x] Assignment listing
- [x] PDF submission
- [x] DOCX submission
- [x] Resubmission workflow
- [x] Teacher review
- [x] Similarity percentage
- [x] Matched student identification
- [x] Matching-text analysis
- [x] Sentence-level similarity
- [x] TF-IDF
- [x] Cosine similarity
- [x] Django admin
- [x] MySQL support

 ### Phase 2 — Backend Improvements

 - [ ] Improve service-layer separation
- [ ] Improve database query performance
- [ ] Improve upload validation
- [ ] Expand automated tests
- [ ] Improve OTP protection
- [ ] Add rate limiting
- [ ] Improve audit logging
- [ ] Improve similarity-result modeling

 ### Phase 3 — REST API

 - [ ] Django REST Framework
- [ ] `/api/v1/`
- [ ] JWT authentication
- [ ] Role-based API permissions
- [ ] User endpoints
- [ ] Assignment endpoints
- [ ] Task endpoints
- [ ] Similarity endpoints
- [ ] Pagination
- [ ] Filtering
- [ ] API documentation

 ### Phase 4 — Asynchronous Processing

 Potential architecture:

```
Student Submission
       │
       ▼
Save Assignment
       │
       ▼
Queue Analysis
       │
       ▼
Background Worker
       │
       ├── Extract Text
       ├── Validate
       ├── Calculate Similarity
       ├── Find Matches
       └── Store Result
```

 Potential technologies:

 - Celery
- Redis

 ### Phase 5 — Advanced Similarity

 Potential future improvements:

 - Sentence embeddings
- Semantic similarity
- Hybrid TF-IDF \+ semantic scoring
- Paraphrase detection
- Vector search
- Precomputed document vectors
- Similarity caching
- Advanced visualization

 ### Phase 6 — Production

 Potential production architecture:

```
                    Internet
                       │
                       ▼
                 Reverse Proxy
                       │
               ┌───────┴───────┐
               │               │
            Django          Static/Media
               │
        ┌──────┴──────┐
        │             │
      Web UI          API
        │             │
        └──────┬──────┘
               │
       Application Services
               │
       ┌───────┴────────┐
       │                │
     MySQL             Redis
                          │
                        Celery
                          │
                 Similarity Workers
```

---

 ## 🔒 Security Considerations

 CopyKat handles student accounts and academic documents, so production deployments should apply appropriate security controls.

 Recommended practices include:

 - Use `DEBUG=False` in production
- Use a strong `SECRET_KEY`
- Keep credentials in environment variables
- Never commit `.env`
- Configure `ALLOWED_HOSTS`
- Use HTTPS
- Restrict uploaded file types
- Enforce upload-size limits
- Store uploaded documents securely
- Protect authentication endpoints
- Apply OTP rate limiting
- Maintain audit logs
- Restrict teacher access to authorized submissions
- Restrict administrative functions
- Maintain secure database backups

---

 ## 🧪 Recommended Test Coverage

 The project should maintain automated tests covering:

 ### Authentication

 - Registration
- Login
- Logout
- Email OTP verification
- Password reset
- Invalid OTP
- Expired OTP
- Unauthorized access

 ### Student Workflow

 - Assignment listing
- Assignment submission
- Invalid file submission
- Empty document
- Unsupported document
- Similarity analysis
- Resubmission

 ### Teacher Workflow

 - Assignment creation
- Assignment editing
- Submission review
- Similarity review
- Matched student display
- Accept submission
- Reject submission
- Resubmission request
- Teacher remarks

 ### Similarity Engine

 - PDF extraction
- DOCX extraction
- Text normalization
- Language validation
- Minimum content validation
- TF-IDF calculation
- Cosine similarity
- Highest-match selection
- Sentence matching
- Matching-text storage

---

 ## 🤝 Contributing

 Contributions are welcome.

 ### 1\. Fork the Repository

 Create your own fork of CopyKat.

 ### 2\. Clone Your Fork

```
git clone https://github.com/YOUR_USERNAME/CopyKat.git
cd CopyKat
```

 ### 3\. Create a Feature Branch

```
git checkout -b feature/your-feature
```

 ### 4\. Install Dependencies

```
pip install -r requirements.txt
```

 ### 5\. Run Checks

```
python manage.py check
python manage.py test
```

 ### 6\. Commit Your Changes

```
git add .
git commit -m "feat: describe your change"
```

 ### 7\. Push Your Branch

```
git push origin feature/your-feature
```

 ### 8\. Open a Pull Request

 Please include:

 - What was changed
- Why it was changed
- How it was tested
- Any database migrations
- Any configuration changes
- Any security considerations

---

 ## 📌 Project Status

 **Active Development**

 CopyKat currently provides a Django server-rendered academic assignment platform with:

 - Student authentication
- Teacher assignment management
- Assignment submission
- PDF/DOCX processing
- TF-IDF similarity
- Cosine similarity
- Sentence-level matching
- Matched-student identification
- Teacher review
- Resubmission workflow
- Django administration

 The following are **planned rather than currently implemented**:

 - Django REST Framework API
- JWT API authentication
- Celery
- Redis
- Background similarity workers
- Semantic embeddings
- Vector database/search
- Hybrid semantic similarity

---

 ## 📄 License

 A license has not yet been selected for the project.

 Until a license is added to the repository, users should not assume that CopyKat may be freely redistributed, modified, or used commercially.

---

 ## 👨‍💻 Author

 **Bishal Subedi**

 GitHub: @Bishal-sub

---

 ## ⭐ Support

 If you find CopyKat useful:

 - ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest improvements
- 🔧 Contribute features
- 📖 Improve documentation

---

 \<p align="center"\> \<strong\>CopyKat\</strong\>\<br\> Detect Similarity. Protect Originality. \</p\> :::