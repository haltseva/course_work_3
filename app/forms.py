from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('EMAIL:', validators=[DataRequired(), Email()])
    password = PasswordField('ПАРОЛЬ:', validators=[DataRequired()])
    remember_me = BooleanField('ЗАПОМНИТЬ МЕНЯ')
    submit = SubmitField('ВОЙТИ')

class RegistrateForm(FlaskForm):
    name = StringField('ИМЯ*:', validators=[DataRequired()])
    email = StringField('EMAIL*:', validators=[DataRequired(), Email()])
    phone = StringField('ТЕЛЕФОН:')
    #birthday= DateField('ДАТА РОЖДЕНИЯ')
    password = PasswordField('ПАРОЛЬ*:', validators=[DataRequired()])
    submit = SubmitField('ЗАРЕГИСТРИРОВАТЬСЯ')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class BuyForm(FlaskForm):
    amont = IntegerField('Количество:')
    submit = SubmitField('КУПИТЬ')

class SortForm(FlaskForm):
    sort = SelectField('СОРТИВОТЬ', choices=[('1', 'от дешового к дорогому'), ('2', 'от дорогого к дешовому'), ('3', 'по названию') ])
