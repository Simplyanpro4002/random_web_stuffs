PAWFOLIO PROFILER: YOUR RISK PURRSONALITY REVIEW!

## Setup Instructions

1. Ensure you have Python 3.11.9 installed on your system.

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python app.py
```

## Features
- Personality Test Presentation
- Response Capture and Scoring
- Results Generation and Email Automation

## Project Structure

```
risk-assessment/
├── app.py              # Main application file
├── forms.py            # Form definitions
├── models.py           # Database models
├── scoring.py          # Risk scoring logic
├── questions_cat.py    # Cat-specific questions
├── questions_dog.py    # Dog-specific questions
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel deployment configuration
├── static/            # Static assets (CSS, JS, images)
├── templates/         # HTML templates
│   ├── base.html      # Base template with common elements
│   ├── introduction.html  # Introduction page
│   ├── question.html  # Template for displaying questions
│   ├── questions_cat.html # Cat-specific questions template
│   ├── questions_dog.html # Dog-specific questions template
│   ├── results.html   # Template for showing results
│   ├── data_collection.html # Data collection form
│   ├── login.html     # User login page
│   └── register.html  # User registration page
├── data/             # Data storage directory
├── instance/         # Instance-specific files
└── migrations/       # Database migrations
```
