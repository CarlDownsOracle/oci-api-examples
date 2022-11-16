from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class CompartmentForm(FlaskForm):
    compartment_field = StringField('Compartment OCID to Search')
    compartment_field.data = 'ok'
    submit = SubmitField('Submit')

class LogGroupForm(FlaskForm):
    log_group_field = StringField('Log Group OCID to Search')
    log_group_field.data = 'ok'
    submit = SubmitField('Submit')

class LogForm(FlaskForm):
    log_field = StringField('Log OCID to Search')
    log_field.data = 'ok'
    submit = SubmitField('Submit')
