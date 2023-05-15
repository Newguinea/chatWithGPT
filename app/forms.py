from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileAllowed


class LoginForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')


class RegisterForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'confirmation', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register')

class LongtextForm(FlaskForm):
    final_prompt = TextAreaField('Final Prompt', validators=[DataRequired()])
    compress_prompt = TextAreaField('Compress Prompt', validators=[DataRequired()])
    file = FileField('File', validators=[DataRequired(), FileAllowed(['txt'], 'Text files only!')])

    def __init__(self, *args, **kwargs):
        super(LongtextForm, self).__init__(*args, **kwargs)
        if 'final_prompt' in kwargs:
            self.final_prompt.data = kwargs['final_prompt']
        if 'compress_prompt' in kwargs:
            self.compress_prompt.data = kwargs['compress_prompt']

