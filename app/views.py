from flask import render_template, url_for
from werkzeug.utils import redirect
from app.forms import *
from app.utils import *
from app.oci_client import *
from app.oci_config import *


@app.route('/')
@app.route('/index')
def default_route():
    context = {'compartment_scope': get_compartment_scope()}
    return render_template('home.html', context=context)


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
        set_compartment_scope(choice.data)
        return redirect(url_for('default_route'))

    return render_template('form.html', context=context, form=form)


@app.route('/validate')
def validate_route():
    validate_configuration()
    return 'Configuration is valid'


@app.route('/user')
def get_oci_user_route():
    data = get_oci_user()
    return serialize_response(data)


@app.route('/compute')
def get_compute_route():
    data = get_compute_instances()
    return serialize_response(data)


@app.route('/attachments')
def get_vnic_attachments_route():
    data = get_vnic_attachments()
    return serialize_response(data)


@app.route('/vcns')
def get_vcns_route():
    data = get_vcns()
    return serialize_response(data)


@app.route('/subnets')
def get_subnets_route():
    data = get_subnets()
    return serialize_response(data)


@app.route('/vcn_with_attached_compute')
def get_vcn_compute_digest_route():
    data = vcn_with_attached_compute()
    return serialize_response(data)


def serialize_response(data):
    serialized = json.dumps(data, indent=2, cls=CustomJSONEncoder)
    response = app.response_class(
        response=serialized,
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()

