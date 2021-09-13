from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import Usuario


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Entrar', id='submitLogin')

class RegistrationForm(FlaskForm):
    name = StringField('Nombre Completo', validators=[DataRequired()])
    username = StringField('Nombre Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repetir Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = Usuario.get_by_username(username)
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Usuario.get_by_email(email)
        if user is not None:
            raise ValidationError('Please use a different email address.')

class RecuperarPassForm(FlaskForm):    
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired()])    
    submit = SubmitField('Cambiar Password', id='submitLogin')

class SolicitarPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar email', id='submitLogin')