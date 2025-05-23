from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired
from models import db, User, Result
from forms import LoginForm, RegistrationForm
from scoring import calculate_raw_score, calculate_standard_score, get_risk_profile
from flask_migrate import Migrate
from questions_temp import QUESTIONS
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///risk_assessment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class IntroForm(FlaskForm):
    submit = SubmitField('Begin Journey')

class QuestionForm(FlaskForm):
    answer = RadioField('Answer', validators=[DataRequired()])
    submit = SubmitField('Next')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('introduction'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('introduction'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/introduction', methods=['GET', 'POST'])
@login_required
def introduction():
    form = IntroForm()  # Use the simpler form for introduction
    intro_text = '''You\'ve just received a <strong class="black-bold">paw-sealed letter</strong>. It reads:<br>
<strong><em>\"Dearest,
If you are reading this, I, Grandmother Cat, have departed to the Great Catnap. My legacy is too grand for mere pawprints — I\'ve crafted 7 Pawfolios, each for a different kind of feline. But only the right grandkitten may claim the one meant for them. Begin by understanding yourself, you must first remember who you are, before you decide who you might become.\"</em></strong><br>
You are now on a journey to find out <strong class="black-bold">what kind of investor you are.</strong>'''
    
    if form.validate_on_submit():
        session['current_question'] = 0
        session['answers'] = {}
        return redirect(url_for('index'))
        
    return render_template('question.html',
                        question={'id': 0, 'narrative': intro_text, 'question_text': ''},
                        form=form,
                        progress=0,
                        total_questions=len(QUESTIONS))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:   
        return redirect(url_for('introduction'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
            return render_template('register.html', form=form)
        
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Log the user in after registration
        login_user(user)
        return redirect(url_for('introduction'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # If no current question, redirect to introduction
    if 'current_question' not in session:
        return redirect(url_for('introduction'))

    if request.args.get('action') == 'prev' and session.get('current_question', 0) > 0:
        session['current_question'] -= 1
        return redirect(url_for('index'))
    
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
    
    return render_template('question.html', 
                         question=question,
                         form=form,
                         progress=session['current_question'],
                         total_questions=len(QUESTIONS))

@app.route('/results')
@login_required
def results():
    if 'answers' not in session:
        return redirect(url_for('index'))
    
    # Calculate scores
    raw_score = calculate_raw_score(session['answers'])
    standard_score = calculate_standard_score(raw_score)
    risk_profile = get_risk_profile(standard_score)
    
    # Save results to database
    result = Result(
        user_id=current_user.id,
        answers=session['answers'],
        raw_score=raw_score,
        standard_score=standard_score,
        risk_group=risk_profile['group']
    )
    db.session.add(result)
    db.session.commit()
    
    answers = session['answers']
    session.clear()
    return render_template(
        'results.html',
        answers=answers,
        questions=QUESTIONS,
        raw_score=raw_score,
        standard_score=standard_score,
        risk_profile=risk_profile
    )

if __name__ == '__main__':
    app.run(debug=True) 