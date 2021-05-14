from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, SelectField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField, SearchField
from wtforms.validators import (DataRequired, Length, Email, EqualTo, ValidationError)
from ..models import User, Creator, Song
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField("Nombre de Usuario",
                           validators=[DataRequired(message="Este campo es obligatorio"), Length(min=5, max=45, message="Su nombre de usuario debe estar entre 5 y 45")])
    full_name = StringField(u"Nombre Completo",
                            validators=[DataRequired(message="Este campo es obligatorio"), Length(min=3, max=60, message="Su nombre debe estar entre 3 y 60")])
    email = StringField(u"Correo Electronico",
                        validators=[DataRequired(message="Este campo es obligatorio"), Email(message="Ingrese un correo como example@example.com")], description="example@example.com")
    password = PasswordField(u"Clave de Usuario",
                             validators=[DataRequired(message="Este campo es obligatorio"), Length(min=5, max=45)])
    cfrm_password = PasswordField(u"Confirmar Clave de Usuario",
                                  validators=[DataRequired(message="Este campo es obligatorio"), EqualTo("password")])

    sex = SelectField("Genero", validators=[DataRequired(message="Este campo es obligatorio")], choices=['Seleccionar', 'Masculino', 'Femenino'])

    birth_date = DateField(u"Fecha de Nacimiento", validators=[DataRequired()])
    submit = SubmitField(u"Registrarse")

    def validate_special_character(self, full_name):
        if (full_name.data >= 33 and full_name.data <= 64) or (full_name.data >= 91 and full_name.data <= 96) or (full_name.data >= 123 and full_name.data <= 126):
            raise ValidationError("Nombre incorrecto, por favor evite usar numeros y simbolos.")

    def validate_sex(self, sex):
        if sex.data == "Seleccionar":
            raise ValidationError("Por favor seleccione su genero.")

    def validate_username(self, username):
        user_email = User.query.filter_by(username=username.data).first()
        if user_email:
            raise ValidationError("Nombre de usuario ya existe")

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        creator_email = Creator.query.filter_by(email=email.data).first()
        if user_email or creator_email:
            raise ValidationError("El correo electronico ya existe")


class UpdateForm(FlaskForm):
    username = StringField(u"Nombre de Usuario",
                           validators=[Length(min=5, max=45)])
    full_name = StringField(u"Nombre Completo",
                            validators=[Length(min=3, max=60)])
    email = StringField(u"Correo Electronico",
                        validators=[Email()], description="example@example.com")
    pfp = FileField(u"Foto de perfil",
                    validators=[FileAllowed(["jpg", "jpeg", "png"], u"Solo se permiten imagenes")])
    submit = SubmitField(u"Actualizar")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            creator = Creator.query.filter_by(username_c=username.data).first()
            if user or creator:
                raise ValidationError("Nombre de usuario ya existe")

    def validate_email(self, email):
        if email.data != current_user.email:
            user_email = User.query.filter_by(email=email.data).first()
            creator_email = Creator.query.filter_by(email=email.data).first()
            if user_email or creator_email:
                raise ValidationError("El correo electronico ya existe")
