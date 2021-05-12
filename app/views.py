from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect

from app.forms import CompartmentForm
from app.utils import *
from app.oci_client import *
from app.oci_config import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Flask-WTF requires an encryption key - the string can be anything'

# Flask-Bootstrap requires this line
Bootstrap(app)


@app.route('/')
@app.route('/index')
def default_route():
    context = {'compartment_scope': app.config.get('compartment_scope')}
    return render_template('base.html', context=context)


@app.route('/config')
def get_config_route():
    response = get_configuration()
    return response


@app.route('/choose_compartment', methods=['GET', 'POST'])
def get_compartment_scope_route():

    context = {}
    form = CompartmentForm()

    if form.validate_on_submit():
        choice = form.compartment_field
        app.config['compartment_scope'] = choice.data
        return redirect(url_for('default_route'))

    return render_template('form.html', context=context, form=form)


@app.route('/validate')
def validate_route():
    validate_configuration()
    return 'Configuration is valid'


@app.route('/user')
def get_oci_user_route():
    user = get_oci_user()
    serialized = json.dumps(user, indent=2, cls=CustomJSONEncoder)
    response = app.response_class(
        response=serialized,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/compute')
def get_compute_route():
    data = get_compute_instances()
    serialized = json.dumps(data, indent=2, cls=CustomJSONEncoder)
    response = app.response_class(
        response=serialized,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/attachments')
def get_vnic_attachments_route():
    data = get_vnic_attachments()
    serialized = json.dumps(data, indent=2, cls=CustomJSONEncoder)
    response = app.response_class(
        response=serialized,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/vcns')
def get_vcns_route():
    data = get_vcns()
    serialized = json.dumps(data, indent=2, cls=CustomJSONEncoder)
    response = app.response_class(
        response=serialized,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/subnets')
def get_subnets_route():
    data = get_subnets()
    serialized = json.dumps(data, indent=2, cls=CustomJSONEncoder)
    response = app.response_class(
        response=serialized,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/vcn_with_attached_compute')
def get_vcn_compute_digest_route():
    data = vcn_with_attached_compute()
    serialized = json.dumps(data, indent=2, cls=CustomJSONEncoder)
    response = app.response_class(
        response=serialized,
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()

