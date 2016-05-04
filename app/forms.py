from wtforms import Form, BooleanField, StringField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25)])
    password = StringField('Password', [validators.Length(min=3, max=25)])

