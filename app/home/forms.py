from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SelectField, SubmitField)
from wtforms.fields.html5 import DateField
from wtforms.validators import (DataRequired, Length, EqualTo, Email, ValidationError)


class LoginForm(FlaskForm):
    email = StringField(u"Correo Electonico",
                        validators=[DataRequired(), Email()])
    password = PasswordField(u"Clave de Usuario",
                             validators=[DataRequired()])
    remember_me = BooleanField(u"Recordarme")
    submit = SubmitField(u"Entrar")
