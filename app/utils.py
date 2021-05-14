import os
from PIL import Image
from secrets import token_hex
from werkzeug.utils import secure_filename


def generate_id(id_type):
    return f"{id_type}{token_hex(6)}".upper()


def isType(start_code, type_id):
    return type_id.startswith(start_code)


def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(r'D:\Python_Projects\AloneMelody\app\static\img\pfp', picture_fn)

    output_size = (600, 600)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_cover(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(r'D:\Python_Projects\AloneMelody\app\static\img\cover', picture_fn)

    output_size = (600, 600)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_song(form_file, user_id, filename):
    form_file.save(f"D:\\Python_Projects\\AloneMelody\\app\\static\\music\\{user_id}\\{filename}.mp3")
