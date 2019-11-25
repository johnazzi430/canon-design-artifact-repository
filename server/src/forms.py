from wtforms import Form, BooleanField, StringField, validators, SubmitField
from flask_wtf import FlaskForm

class Persona_Input(FlaskForm):
    name = StringField('Name', validators =[validators.DataRequired()])
    title = StringField('Title')
    quote = StringField('Quote')
    jobFunction = StringField('Job Function')
    needs = StringField('User Needs')
    wants = StringField('User Wants')
    pain_point = StringField('Pain Points')
    persona_file =StringField('Uploaded File')
    submit = SubmitField('Submit')

class Persona_Edit(FlaskForm):
    name = StringField('Name', validators =[validators.DataRequired()])
    title = StringField('Title')
    quote = StringField('Quote')
    function = StringField('Job Function')
    needs = StringField('User Needs')
    wants = StringField('User Wants')
    pain_point = StringField('Pain Points')
    persona_file =StringField('Uploaded File')
    persona_file =StringField('version')
    submit = SubmitField('Submit')



    #
    # name = StringField('Name', [validators.Length(min=4, max=25)])
    # title = StringField('Title', [validators.Length(min=0, max=250)])
    # quote = StringField('Quote', [validators.Length(min=0, max=250)])
    # function = StringField('Job Function', [validators.Length(min=0, max=250)])
    # needs = StringField('User Needs', [validators.Length(min=0, max=250)])
    # wants = StringField('User Wants', [validators.Length(min=0, max=250)])
    # pain_point = StringField('Pain Points', [validators.Length(min=0, max=250)])
    # persona_file =StringField('Uploaded File', [validators.Length(min=0, max=250)])
    # submit = SubmitField('Submit')
