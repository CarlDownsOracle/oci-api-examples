from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class CompartmentForm(FlaskForm):
    compartment_field = StringField('Compartment OCID to Search:')
    compartment_field.data = 'ok'
    submit = SubmitField('Submit')

class LogGroupForm(FlaskForm):
    log_group_field = StringField('Log Group OCID to Search:')
    log_group_field.data = 'ok'
    submit = SubmitField('Submit')

class LogForm(FlaskForm):
    log_field = StringField('Log OCID to Search:')
    log_field.data = 'ok'
    submit = SubmitField('Submit')

class LogSearchForContentForm(FlaskForm):
    log_content_field = StringField('Enter an optional content term to search for:')
    log_content_field.data = 'ok'
    submit = SubmitField('Submit')

class LogSearchWindowForm(FlaskForm):
    log_content_day_starting_offset = StringField('Enter the number of days prior to today to start from:')
    log_content_day_starting_offset.data = 'ok'
    submit = SubmitField('Submit')

class SearchForOcidForm(FlaskForm):
    ocid_field = StringField('Enter an OCID to Search For:')
    ocid_field.data = 'ok'
    submit = SubmitField('Submit')
