from flask_wtf import FlaskForm
from wtforms import StringField, DateField ,IntegerField ,PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Авторизироваться')

class SearchItemForm(FlaskForm):
    search = StringField('Поиск препарата', validators=[DataRequired()])
    submit_search = SubmitField('Поиск')

class RegistrationForm(FlaskForm):
    username = StringField('Логин',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')
    print = SubmitField('print')

class addItemForm(FlaskForm):
    itemName=StringField('Название препарата',validators=[DataRequired()])
    pkdDate=DateField('Дата упаковки', validators=[DataRequired()])
    expDate=DateField('Срок годности', validators=[DataRequired()])
    quantity=IntegerField('Количество',validators=[DataRequired()])
    price=IntegerField('Цена',validators=[DataRequired()])
    description=StringField('Описание', validators=[DataRequired()])
    add = SubmitField('Добавить')
class billItemForm(FlaskForm):
    itemName=StringField('Название препарата', validators=[DataRequired()])
    quantity=IntegerField('Количество',validators=[DataRequired()])
    price = IntegerField('Цена',validators=[DataRequired()])
    enter=SubmitField('Добавить')
    clear=SubmitField('Очистить')
