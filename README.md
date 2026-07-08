# CopyKat

## A Web-Based Assignment Similarity Checker for Academic Institutions

CopyKat is a web-based assignment similarity detection system developed for academic institutions to identify similarities among student submissions. The system compares newly uploaded assignments with previously stored assignments and generates a similarity report using TF-IDF vectorization and Cosine Similarity.

The project aims to provide an affordable, institution-hosted alternative to commercial plagiarism detection systems by focusing on internal assignment comparisons rather than internet-wide plagiarism checks.

---

## Features

### Student Features

* Student registration and authentication
* Upload assignments in PDF and DOCX formats
* View submission history
* Resubmit rejected assignments

### Teacher Features

* View submitted assignments
* Review similarity reports
* Accept or reject assignments based on similarity analysis
* Monitor student submissions

### Administrator Features

* Manage students and teachers
* Manage uploaded assignments
* Access system statistics
* Maintain system data through Django Admin

### Similarity Detection Features

* Automatic text extraction from PDF and DOCX files
* Text preprocessing and cleaning
* TF-IDF vectorization
* Cosine Similarity calculation
* Similarity percentage generation
* Storage of comparison reports

---

## Technology Stack

### Backend

* Python 3.11+
* Django 4.2

### Database

* MySQL

### Frontend

* HTML5
* CSS3
* Bootstrap 5

### Machine Learning & NLP

* Scikit-learn
* TF-IDF Vectorizer
* Cosine Similarity

### File Processing

* PyPDF2
* python-docx

### Version Control

* Git
* GitHub

---

## Project Structure

```text
copykat/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── assignments/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── similarity/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── services/
│       ├── extractor.py
│       ├── preprocessing.py
│       └── similarity_engine.py
│
├── dashboard/
│   ├── views.py
│   └── urls.py
│
├── templates/
├── static/
├── media/
│
├── copykat/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/bishal/CopyKat.git
cd CopyKat
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create MySQL Database

```sql
CREATE DATABASE copykat_db;
```

### 5. Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key

DB_NAME=copykat_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 6. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

Admin Panel:

```text
http://127.0.0.1:8000/admin
```

---

## Similarity Detection Workflow

1. Student uploads PDF or DOCX assignment.
2. System extracts document text.
3. Text preprocessing is performed.
4. TF-IDF vectorization converts text into numerical vectors.
5. Cosine Similarity compares the uploaded assignment with all stored assignments.
6. Similarity percentage is calculated.
7. Similarity report is generated and stored.
8. Teacher reviews the report and accepts or rejects the submission.

---

## User Roles

### Student

* Upload assignments
* View submissions
* Resubmit assignments

### Teacher

* Review reports
* Accept assignments
* Reject assignments

### Administrator

* Manage users
* Manage assignments
* Access system administration

---

## Future Enhancements

* Vector database integration
* Semantic similarity detection using embeddings
* Assignment highlighting for matched text
* Department and course management
* Email notifications
* Similarity trend analytics
* AI-generated content detection



## License

This project is developed As My BCA 4th Semester project 

## Author
Bishal Subedi
