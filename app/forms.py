from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class CompartmentForm(FlaskForm):
    compartment_field = StringField('Compartment OCID to Search')
    compartment_field.data = 'ok'
    submit = SubmitField('Submit')
