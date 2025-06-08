from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class DataCollectionForm(FlaskForm):
    age_group = RadioField('Age Group', choices=[
        ('18-20', '18 - 20'),
        ('21-22', '21 - 22'),
        ('23-25', '23 - 25'),
        ('25+', '25 or older')
    ], validators=[DataRequired()])
    
    gender = RadioField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], validators=[DataRequired()])
    
    income = RadioField('Monthly Income', choices=[
        ('<3m', 'Less than 3 million VND'),
        ('3m-5m', '3 million - 5 million VND'),
        ('5m-10m', '5 million - 10 million VND'),
        ('10m-20m', '10 million - 20 million VND'),
        ('>20m', '20 million VND or above')
    ], validators=[DataRequired()])
    
    stock_market = RadioField('Stock Market Participation', choices=[
        ('none', 'I do not invest in the stock market'),
        ('once_twice', 'I have invested once or twice'),
        ('occasionally', 'I occasionally invest'),
        ('regularly', 'I invest regularly'),
        ('actively', 'I trade actively')
    ], validators=[DataRequired()])
    
    financial_knowledge = RadioField('Financial Knowledge', choices=[
        ('very_low', 'Very low'),
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('very_high', 'Very high')
    ], validators=[DataRequired()])
    
    game_version = RadioField('Game Version', choices=[
        ('cat', '🐱 version'),
        ('dog', '🐶 version')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Continue') 