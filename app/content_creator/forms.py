from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SelectField, SubmitField, TextAreaField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField
from wtforms.validators import (DataRequired, Length, EqualTo, Email, ValidationError)
from ..models import Creator, User, Song
from flask_login import current_user


class RegisterForm(FlaskForm):
    username = StringField(u"Nombre de Usuario",
                           validators=[DataRequired(message="Este campo es obligatorio"), Length(min=5, max=45, message="Su nombre de usuario debe estar entre 5 y 45")])
    full_name = StringField(u"Nombre de la Banda o Artista:",
                            validators=[DataRequired(message="Este campo es obligatorio"), Length(min=3, max=60, message="Su nombre completo debe estar entre 3 y 60")])

    disco = StringField(u"Nombre de la discografica:",
                        validators=[DataRequired(message="Este campo es obligatorio"), Length(min=3, max=60)])
    email = StringField(u"Correo Electronico",
                        validators=[DataRequired(message="Este campo es obligatorio"), Email(message="Ingrese un correo de tipo example@example.com")], description="example@example.com")
    password = PasswordField(u"Contrasena",
                             validators=[DataRequired(message="Este campo es obligatorio"), Length(min=5, max=45)])
    cfrm_password = PasswordField(u"Confirmar Contrasena",
                                  validators=[DataRequired(message="Este campo es obligatorio"), EqualTo("password")])

    creation_date = DateField(u"Fecha de Creacion", validators=[DataRequired()])
    submit = SubmitField(u"Registrarse")

    def validate_special_character(self, full_name):
        if (full_name.data >= 33 and full_name.data <= 64) or (full_name.data >= 91 and full_name.data <= 96) or (full_name.data >= 123 and full_name.data <= 126):
            raise ValidationError("Nombre incorrecto, por favor evite usar numeros y simbolos.")

    def validate_username(self, username):
        creator_username = Creator.query.filter_by(username_c=username.data).first()
        user_username = User.query.filter_by(username=username.data).first()
        if creator_username or user_username:
            raise ValidationError("Nombre de usuario ya existe")

    def validate_email(self, email):
        creator_email = Creator.query.filter_by(email=email.data).first()
        user_email = User.query.filter_by(email=email.data).first()
        if creator_email or user_email:
            raise ValidationError("El correo electronico ya existe")


class UpdateForm(FlaskForm):
    username = StringField(u"Nombre de Usuario",
                           validators=[Length(min=5, max=45, message="Su nombre de usuario debe estar entre 5 y 45")])

    disco = StringField(u"Nombre de la discografica:",
                        validators=[Length(min=3, max=60)])

    email = StringField(u"Correo Electronico",
                        validators=[Email(message="Ingrese un correo de tipo example@example.com")], description="example@example.com")

    pfp = FileField(u"Foto de perfil",
                    validators=[FileAllowed(["jpg", "jpeg", "png"], u"Solo se permiten imagenes")])

    description = TextAreaField(u"Descripcion")

    submit = SubmitField(u"Actualizar")

    def validate_special_character(self, full_name):
        if (full_name.data >= 33 and full_name.data <= 64) or (full_name.data >= 91 and full_name.data <= 96) or (full_name.data >= 123 and full_name.data <= 126):
            raise ValidationError("Nombre incorrecto, por favor evite usar numeros y simbolos.")

    def validate_username(self, username):
        if username.data != current_user.username_c:
            creator_username = Creator.query.filter_by(username_c=username.data).first()
            user_username = User.query.filter_by(username=username.data).first()
            if creator_username or user_username:
                raise ValidationError("Nombre de usuario ya existe")

    def validate_email(self, email):
        if email.data != current_user.email:
            creator_email = Creator.query.filter_by(email=email.data).first()
            user_email = User.query.filter_by(email=email.data).first()
            if creator_email or user_email:
                raise ValidationError("El correo electronico ya existe")


class SongForm(FlaskForm):
    song_cover = FileField(u"Portada", validators=[FileAllowed(["jpg", "jpeg", "png"], u"Solo se permiten imagenes")])
    song_title = StringField(u"Titulo de la Cancion", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=5, max=60, message="Su nombre de usuario debe estar entre 5 y 60")])
    song_genre = StringField(u"Genero de la cancion", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=3, max=60, message="Su nombre de usuario debe estar entre 3 y 25")])
    disco = StringField(u"Casa Disografica", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=5, max=30, message="Su nombre de usuario debe estar entre 5 y 30")])
    save_song = FileField(u"Cancion", validators=[FileAllowed(["mp3"], u"Solo se permiten archivos mp3")])
    submit = SubmitField(u"Agregar Cancion")

