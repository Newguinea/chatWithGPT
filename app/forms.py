from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileAllowed

# LoginForm class inherits from FlaskForm, and contains username and password fields.
# Validators are used to check that the input data is valid before it is processed.
class LoginForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

# RegisterForm class also inherits from FlaskForm. It contains username, password,
# and password confirmation fields. The EqualTo validator is used to check that the
# password and confirmation fields match.
class RegisterForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'confirmation', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register')

# LongtextForm class allows user to submit a text file and two prompts.
# Validators check that these fields are not empty and that the submitted file
# is a text file.
class LongtextForm(FlaskForm):
    final_prompt = TextAreaField('Final Prompt', validators=[DataRequired()])
    compress_prompt = TextAreaField('Compress Prompt', validators=[DataRequired()])
    file = FileField('File', validators=[DataRequired(), FileAllowed(['txt'], 'Text files only!')])

    # The constructor method is overridden to allow initializing the form with existing data.
    def __init__(self, *args, **kwargs):
        super(LongtextForm, self).__init__(*args, **kwargs)
        if 'final_prompt' in kwargs:
            self.final_prompt.data = kwargs['final_prompt']
        if 'compress_prompt' in kwargs:
            self.compress_prompt.data = kwargs['compress_prompt']

