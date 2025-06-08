from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import RadioField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, Optional
from models import db, Result
from forms import RegistrationForm, DataCollectionForm
from scoring import calculate_raw_score, calculate_standard_score, get_risk_profile
from flask_migrate import Migrate
from questions_temp import QUESTIONS
from flask_mail import Mail, Message
import os
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/risk_assessment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  # Set this in your environment
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')  # Set this in your environment
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')

# Initialize extensions
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Create tables with the correct schema
with app.app_context():
    db.drop_all()  # Drop all existing tables
    db.create_all()  # Create tables with the new schema

class IntroForm(FlaskForm):
    submit = SubmitField('Begin Journey ✨')

class QuestionForm(FlaskForm):
    answer = RadioField('Answer', validators=[DataRequired()])
    submit = SubmitField('Next')

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Send Results')

@app.route('/introduction', methods=['GET', 'POST'])
def introduction():
    form = IntroForm()  # Use the simpler form for introduction
    intro_text = '''You\'ve just received a <strong class="black-bold">paw-sealed letter</strong>. It reads:<br>
<strong><em>\"Dearest,
If you are reading this, I, Grandmother Cat, have departed to the Great Catnap. My legacy is too grand for mere pawprints — I\'ve crafted 7 Pawfolios, each for a different kind of feline. But only the right grandkitten may claim the one meant for them. Begin by understanding yourself, you must first remember who you are, before you decide who you might become.\"</em></strong><br>
You are now on a journey to find out <strong class="black-bold">what kind of investor you are.</strong>'''
    
    if form.validate_on_submit():
        session['current_question'] = 1  # Set to 1 to start with the first question
        session['answers'] = {}
        return redirect(url_for('data_collection'))
        
    return render_template('question.html',
                        question={'id': 0, 'narrative': intro_text, 'question_text': ''},
                        form=form,
                        progress=0,
                        total_questions=len(QUESTIONS))

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
        # Set current_question to 0 to start from the first question
        session['current_question'] = 0
        return redirect(url_for('index'))
    
    return render_template('data_collection.html', form=form)

@app.route('/', methods=['GET', 'POST'])
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
    
    if session['current_question'] >= len(QUESTIONS):
        return redirect(url_for('results'))
    
    question = QUESTIONS[session['current_question']]
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
            image_dir = 'images_dog' if session.get('user_data', {}).get('game_version') == 'dog' else 'images'
            
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
    
    return render_template('question.html', 
                         question=question,
                         form=form,
                         progress=session['current_question'],
                         total_questions=len(QUESTIONS))

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
        # Save results to database
        result = Result(
            answers=session['answers'],
            raw_score=raw_score,
            standard_score=standard_score,
            risk_group=risk_profile['group'],
            user_data=session['user_data']  # Add user data to the result
        )
        db.session.add(result)
        db.session.commit()
    except Exception as e:
        # If there's an error saving to database, just log it and continue
        print(f"Error saving results to database: {e}")
        db.session.rollback()
    
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
        user_data=user_data
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
        subject='Test Mail from Flask',
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