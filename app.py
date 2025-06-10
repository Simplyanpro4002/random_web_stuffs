from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import RadioField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, Optional
from forms import DataCollectionForm
from scoring import calculate_raw_score, calculate_standard_score, get_risk_profile
from questions_temp import QUESTIONS
from questions_cat import QUESTIONS_CAT
from questions_dog import QUESTIONS_DOG
from flask_mail import Mail, Message
import os
import requests
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  # Set this in your environment
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')  # Set this in your environment
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')

# Initialize extensions
csrf = CSRFProtect(app)
mail = Mail(app)

class IntroForm(FlaskForm):
    submit = SubmitField('Begin Journey')

class QuestionForm(FlaskForm):
    answer = RadioField('Answer', validators=[DataRequired()])
    submit = SubmitField('Next')

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Send Results')

@app.route('/', methods=['GET', 'POST'])
def introduction():
    form = IntroForm()
    if form.validate_on_submit():
        return redirect(url_for('data_collection'))
    return render_template('introduction.html', form=form)

@app.route('/data-collection', methods=['GET', 'POST'])
def data_collection():
    form = DataCollectionForm()
    
    if form.validate_on_submit():
        # Store the collected data in the session
        session['user_data'] = {
            'age_group': form.age_group.data,
            'gender': form.gender.data,
            'income': form.income.data,
            'stock_market': form.stock_market.data,
            'financial_knowledge': form.financial_knowledge.data,
            'game_version': form.game_version.data
        }
        # Initialize answers dictionary and current question
        session['answers'] = {}
        session['current_question'] = 0
        return redirect(url_for('index'))
    
    return render_template('data_collection.html', form=form)

@app.route('/questions', methods=['GET', 'POST'])
def index():
    # If no current question or user data, redirect to introduction
    if 'current_question' not in session or 'user_data' not in session:
        return redirect(url_for('introduction'))

    if request.args.get('action') == 'prev':
        if session.get('current_question', 0) > 0:
            session['current_question'] -= 1
            return redirect(url_for('index'))
        else:
            # If on first question, go back to data collection
            return redirect(url_for('data_collection'))
    
    # Get the appropriate questions based on game version
    game_version = session.get('user_data', {}).get('game_version', 'cat')
    questions = QUESTIONS_DOG if game_version == 'dog' else QUESTIONS_CAT
    
    if session['current_question'] >= len(questions):
        return redirect(url_for('results'))
    
    question = questions[session['current_question']]
    form = QuestionForm()
    form.answer.choices = [(choice[0], choice[1]) for choice in question['options']]
    
    if form.validate_on_submit():
        session['answers'][str(question['id'])] = form.answer.data
        session['current_question'] += 1
        return redirect(url_for('index'))
    
    if str(question['id']) in session.get('answers', {}):
        form.answer.data = session['answers'][str(question['id'])]
    
    # Add image paths for the slideshow
    if question['id'] > 0:  # Skip for introduction page
        image_paths = []
        i = 1
        while True:
            # Determine the image directory based on game version
            image_dir = 'images_dog' if game_version == 'dog' else 'images_cat'
            
            # Construct the full path to the image file
            image_filename = f'image_{i}.png'
            image_path = os.path.join('static', image_dir, f'question_{question["id"]}', image_filename)
            
            # Check if the image exists using os.path.exists
            if not os.path.exists(image_path):
                break
                
            # If image exists, add its URL path
            image_paths.append(url_for('static', filename=f'{image_dir}/question_{question["id"]}/{image_filename}'))
            i += 1
        question['image_paths'] = image_paths
    
    # Use the appropriate template based on game version
    template = 'questions_dog.html' if game_version == 'dog' else 'questions_cat.html'
    print(template)
    return render_template(template, 
                         question=question,
                         form=form,
                         progress=session['current_question'],
                         total_questions=len(questions))

@app.route('/results')
def results():
    if 'answers' not in session or 'user_data' not in session:
        return redirect(url_for('index'))
    
    # Calculate scores
    raw_score = calculate_raw_score(session['answers'])
    standard_score = calculate_standard_score(raw_score)
    risk_profile = get_risk_profile(standard_score)
    
    # Store results in session for email functionality
    session['raw_score'] = raw_score
    session['standard_score'] = standard_score
    session['risk_profile'] = risk_profile

    try:
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Save to CSV file in the data directory
        csv_filename = os.path.join(data_dir, 'results.csv')
        file_exists = os.path.exists(csv_filename)
        
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'timestamp',
                'game_version',
                'age_group',
                'gender',
                'income',
                'stock_market',
                'financial_knowledge',
                'raw_score',
                'standard_score',
                'risk_group'
            ]
            
            # Add question answer fields
            for i in range(1, 16):  # Assuming 15 questions
                fieldnames.append(f'question_{i}_answer')
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            # Prepare row data
            row_data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'game_version': session['user_data'].get('game_version', ''),
                'age_group': session['user_data'].get('age_group', ''),
                'gender': session['user_data'].get('gender', ''),
                'income': session['user_data'].get('income', ''),
                'stock_market': session['user_data'].get('stock_market', ''),
                'financial_knowledge': session['user_data'].get('financial_knowledge', ''),
                'raw_score': raw_score,
                'standard_score': standard_score,
                'risk_group': risk_profile['group']
            }
            
            # Add question answers
            for i in range(1, 16):
                row_data[f'question_{i}_answer'] = session['answers'].get(str(i), '')
            
            writer.writerow(row_data)
            
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
    
    answers = session['answers']
    user_data = session['user_data']
    session.clear()

    # Create form instance for email
    form = EmailForm()

    return render_template(
        'results.html',
        answers=answers,
        questions=QUESTIONS,
        raw_score=raw_score,
        standard_score=standard_score,
        risk_profile=risk_profile,
        form=form,
        user_data=user_data,
        game_version=user_data.get('game_version', 'cat')  # Add game_version to template context
    )

@app.route('/send_results_email', methods=['POST'])
def send_results_email():
    # print("hello")
    email = request.form.get('email')
    # print(email)
    # if not email:
    #     flash('Please provide an email address')
    #     return redirect(url_for('results'))
    
    # Get the results from the session
    raw_score = session.get('raw_score')
    standard_score = session.get('standard_score')
    risk_profile = session.get('risk_profile')
    
    # if not all([raw_score, standard_score, risk_profile]):
    #     flash('Results not found. Please take the assessment again.')
    #     return redirect(url_for('index'))
    
    # Create email content
    msg = Message(
        # 'Your Pawfolio Profile Results',
        recipients=[email],
        subject='Your Pawfolio Profile Results!',
                  sender=app.config['MAIL_USERNAME'],
                  body='Hello, this is a test email sent from Flask-Mail.'
    )
    
    # Format the email body
    msg.body = f"""Your Pawfolio Profile Results


Thank you for taking the Pawfolio Assessment!
"""
    
    try:
        mail.send(msg)
        flash('Results have been sent to your email!')
    except Exception as e:
        flash('Failed to send email. Please try again later.')
        print(f"Email error: {e}")
    
    return redirect(url_for('results'))

if __name__ == '__main__':
    app.run(debug=True) 