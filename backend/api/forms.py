from wtforms import Form, BooleanField, StringField, IntegerField, DateField, TextAreaField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25)])
    password = StringField('Password', [validators.Length(min=3, max=25)])


class SubmitTimeForm(Form):
    time_spent = IntegerField('Time Spent')
    ticket = IntegerField('Ticket', [validators.Optional()])
    date = DateField('Date/Time', render_kw={'type': 'date'})
    description = TextAreaField('Description')
