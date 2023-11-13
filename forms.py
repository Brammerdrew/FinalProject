from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("Email already in use. Pick another one.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()

class UpdateUserForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo('password')])
    submit = SubmitField()
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("Email already in use. Pick another one.")

class AddDog(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()]) # 'M' or 'F
    age = StringField('Age', validators=[DataRequired()])
    breed = StringField('Breed', validators=[DataRequired()])
    submit = SubmitField()