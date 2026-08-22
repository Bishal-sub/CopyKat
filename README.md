# CopyKat

[![Django](https://img.shields.io/badge/Django-6.0.7-darkgreen)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange)](https://www.mysql.com/)


 Assignment similarity detection platform leveraging machine learning algorithms for institutional similarity detection. Utilizes TF-IDF vectorization and cosine similarity metrics to identify copied submissions with sentence-level granularity.


## Overview

CopyKat is a Django-based web application designed for educational institutions to detect copied or duplicate assignments. The system performs sophisticated text analysis using machine learning techniques to identify similarities between student submissions against an institutional archive.

**Key Differentiators:**
- Sentence-level matching with 75% similarity threshold
- Multi-format document support (PDF, DOCX)
- Role-based access control (Student, Teacher, Admin)
- Persistent similarity cache for performance
- Real-time analysis with background processing capability
- Comprehensive audit trail for all submissions

## Core Features

### 📊 Similarity Detection Engine
- **TF-IDF Vectorization** - Term Frequency-Inverse Document Frequency analysis
- **Cosine Similarity Scoring** - 0-100% similarity percentage calculation
- **Sentence-Level Granularity** - Identifies specific matching text passages
- **Language Validation** - English-only document processing with langdetect
- **Minimum Content Validation** - Rejects documents under 50 words

### 🔐 Security & Authentication
- OAuth-ready JWT token structure
- OTP-based email verification (SendGrid/Gmail compatible)
- Secure password reset flow with time-limited tokens
- CSRF protection on all POST requests
- SQL injection prevention via Django ORM parameterization
- Rate limiting on authentication endpoints

### 👥 Multi-Role System
- **Students** - Submit assignments, track similarity scores, request resubmission
- **Teachers** - Create tasks, review submissions, generate similarity reports
- **Admins** - User management, department/level configuration, system analytics

### 📋 Assignment Management
- Dual submission system (initial + resubmission with deadline)
- Status workflow (not_submitted → pending_review → accepted/rejected)
- Teacher remarks and feedback integration
- Automatic deadline tracking and overdue notifications

### 🛠 Admin Dashboard
- Jazzmin-enhanced Django admin interface
- Custom user filtering and search capabilities
- Bulk assignment creation from CSV
- Real-time system statistics dashboard

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                       │
│        (Bootstrap 5 | Django Templates )                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 Django Application                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Accounts    │  │ Assignments  │  │  Dashboard   │   │
│  │  App         │  │  App         │  │  App         │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │      Similarity Detection Engine (Core)          │   │
│  │  ├─ Text Extraction (PDF/DOCX)                   │   │
│  │  ├─ Text Cleaning & Normalization                │   │
│  │  ├─ TF-IDF Vectorization                         │   │
│  │  ├─ Cosine Similarity Calculation                │   │
│  │  └─ Sentence Matching & Highlighting             │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           Data Persistence Layer                        │
│               MySQL Database                            │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

### Backend
- **Framework** - Django 6.0.7 with Django REST Framework ready
- **Database** - MySQL 8.0+ with connection pooling
- **ML/NLP** - scikit-learn 1.9.0, scipy 1.18.0
- **Document Processing** -  python-docx 1.2, PyMuPDF 1.28

### Additional Libraries
- **langdetect** 1.0.9 - Language detection (English validation)
- **python-decouple** 3.8 - Environment variable management
- **Pillow** 12.3.0 - Image processing for user avatars
- **regex** 2026.7.19 - Advanced pattern matching
- **jazzmin** 3.0.5 - Enhanced admin interface



## Installation

### Prerequisites
```
- Python 3.8+ (tested on 3.10, 3.11)
- MySQL Server 8.0+
- 2GB RAM minimum
- 500MB disk space for dependencies + uploads
```

### Step-by-Step Setup

**1. Clone & Environment Setup**
```bash
git clone https://github.com/Bishal-sub/CopyKat.git
cd CopyKat-main
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**2. Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**3. Environment Configuration**
```bash
cp .env.example .env
```

Edit `.env`:
```env
# Django Settings
SECRET_KEY=your-very-secure-random-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=copykat_production
DB_USER=copykat_user
DB_PASSWORD=strong-password-here
DB_HOST=localhost
DB_PORT=3306

# Email Configuration (Gmail/SendGrid)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# AWS S3 (Optional for file storage)
USE_S3=False
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket


```

**4. Database Setup**
```bash
# Create MySQL database
mysql -u root -p
> CREATE DATABASE copykat_production;
> CREATE USER 'copykat_user'@'localhost' IDENTIFIED BY 'strong-password-here';
> GRANT ALL PRIVILEGES ON copykat_production.* TO 'copykat_user'@'localhost';
> FLUSH PRIVILEGES;
> EXIT;

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser --username admin --email admin@example.com

# Collect static files
python manage.py collectstatic --noinput
```

**5. Testing Installation**
```bash
python manage.py test
python manage.py runserver
```

Visit `http://localhost:8000` and login with superuser credentials.

## Configuration

### Email Service Setup

**Gmail Configuration:**
```python
# Generate App Password at: https://myaccount.google.com/apppasswords
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-character-app-password'
DEFAULT_FROM_EMAIL = 'noreply@copykat.com'
```

**SendGrid Configuration:**
```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'SG.your-sendgrid-api-key'
```

### Database Connection Pooling

Add to `settings.py` for production:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

### Cache Configuration (Redis)

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## Similarity Algorithm

### Algorithm Flow

```
1. TEXT EXTRACTION
   ├─ PDF: PyMuPDF for fast extraction
   ├─ DOCX: python-docx for structured parsing
   └─ Error Handling: Fallback to PyPDF2

2. TEXT CLEANING
   ├─ Lowercase conversion
   ├─ Special character removal (keep spaces)
   ├─ Multiple space normalization
   └─ Whitespace trimming

3. VALIDATION
   ├─ Language Detection: langdetect (English only)
   ├─ Minimum Length: 50 words required
   └─ File Size: < 50MB

4. COMPARISON SCOPE
   ├─ Query: SELECT assignments WHERE
   │   - topic = current_task.topic
   │   - semester = current.semester
   │   - subject = current.subject
   │   - student != current.student
   └─ Limit: Last 100 submissions per task

5. VECTORIZATION
   ├─ TF-IDF Parameters:
   │   - stop_words: English
   │   - ngram_range: (1, 2)
   │   - max_features: 5000
   └─ Sparse matrix generation

6. SIMILARITY CALCULATION
   ├─ Cosine Similarity: cos(θ) = (A·B) / (||A|| ||B||)
   ├─ Score Range: 0.0 - 1.0
   └─ Percentage: score * 100 (floor)

7. SENTENCE MATCHING
   ├─ Sentence Splitting: Regex-based tokenization
   ├─ Filtering: Minimum 5 words per sentence
   ├─ Individual TF-IDF: Per-sentence vectorization
   ├─ Threshold: 75% similarity for match
   └─ Position Tracking: Character offsets preserved

8. RESULT STORAGE
   ├─ similarity_percentage: "34.5%"
   ├─ matched_assignment: Foreign key
   ├─ matching_text: JSON array of matches
   └─ Analysis Status: Complete/Error
```

## Contributing

### Development Setup
```bash
# Create feature branch
git checkout -b feature/your-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest --cov=copykat tests/

# Format code
black .
flake8 .

# Commit and push
git commit -m "feat: description"
git push origin feature/your-feature
```

### Code Style
- Follow PEP 8
- Use type hints for functions
- Document complex algorithms
- Write tests for new features (min 80% coverage)


## Author

**Bishal Subedi**
- GitHub: [@Bishal-sub](https://github.com/Bishal-sub)


**Support:** [Create an Issue](https://github.com/Bishal-sub/CopyKat/issues)