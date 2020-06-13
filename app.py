from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField
from wtforms.validators import InputRequired, Length, AnyOf, Email
import email_validator


app = Flask(__name__)
app.config['SECRET_KEY'] = "MoiSecretivo!"
app.config['WTF_CSRF_SECRET_KEY'] = "MoiSecretivo##"  # Defaults to SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 20  # CSRF Token expiration time. Defaults to 3600


class TelephoneForm(Form):  # Inherit from Form, not FlaskForm
    country_code = IntegerField('Country Code')
    area_code = IntegerField('Area Code')
    number = StringField('Phone Number')


class LoginForm(FlaskForm):  # <-- One FlaskForm per form
    username = StringField('User Name', validators=[InputRequired('A username is required!'), Length(min=4,max=8,message='Length must be between 4 and 8 letters')])
    password = PasswordField('Password', validators=[InputRequired('A password is required!'), AnyOf(values=['secret', 'password'])])
    age = IntegerField('Your Age', default=30)
    email = StringField('Email (@)', validators=[Email('Email format')])
    home_phone = FormField(TelephoneForm)


class NameForm(LoginForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')


class User():
    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email


@app.route('/', methods=['GET', 'POST'])
def index():
    myuser = User('JohnDoe', 23, 'john.doe@dodomail.com')
    form = NameForm(obj=myuser)

    if form.validate_on_submit():
        return "<h1>UserName : {}, Password : {}, Age = {}, Email = {}</h1>".format(form.username.data, form.password.data, form.age.data, form.email.data)

    return render_template('index.html', form=form)


@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    class DynamicForm(FlaskForm):
        pass

    DynamicForm.name = StringField('name')

    names = ['middle_name', 'last_name', 'nick_name']

    for name in names:
        setattr(DynamicForm, name, StringField(name))
    
    form = DynamicForm()

    if form.validate_on_submit():
        return '<h1>Form validated! Name = {}</h1>'.format(form.name.data)
    
    return render_template('dynamic.html', form=form, names=names)


if __name__ == "__main__":
    app.run(debug=True)