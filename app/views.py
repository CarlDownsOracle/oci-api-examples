from flask import render_template, url_for, request
from werkzeug.utils import redirect
from app.forms import *
from app.utils import *

from app.oci_client import *
from app.oci_config import *
from app.oci_usage import *
from app.oci_search import *
from app.oci_audit import *
from app.oci_block_storage import *
from app.oci_log_search import *
from app.oci_monitoring import *

from app import flask_app
import logging

logging_level = os.getenv('LOGGING_LEVEL', 'DEBUG')
loggers = [logging.getLogger()] + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
[logger.setLevel(logging.getLevelName(logging_level)) for logger in loggers]

@flask_app.route('/')
@flask_app.route('/index')
def default_route():
    get_cookies(req=request)
    context = {
        'compartment_scope': get_compartment_scope(),
        'log_group_scope': get_log_group_scope_from_cookie(request),
        'log_scope': get_log_scope_from_cookie(request),
    }
    return render_template('home.html', context=context)


@flask_app.route('/config')
def get_config_route():
    get_cookies(req=request)
    response = get_configuration()
    return response


@flask_app.route('/choose_compartment', methods=['GET', 'POST'])
def get_compartment_scope_route():
    get_cookies(req=request)
    context = {}
    form = CompartmentForm()

    if form.validate_on_submit():
        choice = form.compartment_field
        set_compartment_scope(choice.data)
        resp = redirect(url_for('default_route'))
        set_compartment_scope_to_cookie(resp)
        return resp

    return render_template('form.html', context=context, form=form)


@flask_app.route('/show_compartment_details')
def get_compartment_details():
    get_cookies(req=request)
    data = search_by_ocid(get_compartment_scope())
    return serialize_response(data)


@flask_app.route('/validate')
def validate_route():
    get_cookies(req=request)
    validate_configuration()
    return 'Configuration is valid'


@flask_app.route('/user')
def get_oci_user_route():
    get_cookies(req=request)
    data = get_oci_user()
    return serialize_response(data)

# ========================
# Compute
# ========================

@flask_app.route('/compute_details')
def get_compute_route():
    get_cookies(req=request)
    data = get_compute_instances_details()
    return serialize_response(data)


@flask_app.route('/compute_status')
def get_compute_status_route():
    get_cookies(req=request)
    data = get_compute_instances_status()
    return serialize_response(data)


@flask_app.route('/compute_start')
def start_compute_route():
    get_cookies(req=request)
    data = start_all_compute_instances()
    return serialize_response(data)


@flask_app.route('/compute_stop')
def stop_compute_route():
    get_cookies(req=request)
    data = stop_all_compute_instances()
    return serialize_response(data)

# ========================
# Block Storage
# ========================

@flask_app.route('/block_volumes')
def get_block_volumes_route():
    get_cookies(req=request)
    data = list_volumes(get_compartment_scope())
    return serialize_response(data)


# ========================
# Networking
# ========================

# @app.route('/public_ip/<ip_address>')
# def get_public_ip_route(ip_address):
#     data = get_public_ip(ip_address)
#     return serialize_response(data)


@flask_app.route('/attachments')
def get_vnic_attachments_route():
    get_cookies(req=request)
    data = get_vnic_attachments()
    return serialize_response(data)


@flask_app.route('/vcns')
def get_vcns_route():
    get_cookies(req=request)
    data = get_vcns()
    return serialize_response(data)


@flask_app.route('/subnets')
def get_subnets_route():
    get_cookies(req=request)
    data = get_subnets()
    return serialize_response(data)


@flask_app.route('/vcn_with_attached_compute')
def get_vcn_compute_digest_route():
    get_cookies(req=request)
    data = vcn_with_attached_compute()
    return serialize_response(data)


@flask_app.route('/vcn_topology/<vcn>')
def get_vcn_topology_route(vcn):
    get_cookies(req=request)
    set_vcn_scope(vcn)
    data = get_vcn_topology()
    return serialize_response(data)

# ========================
# Usage
# ========================


@flask_app.route('/usage')
def get_usage_report():
    get_cookies(req=request)
    data = retrieve_usage_report()
    return serialize_response(data)


# ========================
# Generic Search
# ========================


@flask_app.route('/search/<ocid>')
def get_ocid_search_result(ocid):
    get_cookies(req=request)
    data = search_by_ocid(ocid)
    return serialize_response(data)


# ========================
# Logging
# ========================

@flask_app.route('/choose_log_group', methods=['GET', 'POST'])
def get_log_group_scope_route():
    get_cookies(req=request)
    context = {}
    form = LogGroupForm()

    if form.validate_on_submit():
        choice = form.log_group_field
        set_log_group_scope(choice.data)
        resp = redirect(url_for('default_route'))
        set_log_group_scope_to_cookie(resp)
        return resp

    return render_template('form.html', context=context, form=form)


@flask_app.route('/choose_log', methods=['GET', 'POST'])
def get_log_scope_route():
    get_cookies(req=request)
    context = {}
    form = LogForm()

    if form.validate_on_submit():
        choice = form.log_field
        set_log_scope(choice.data)
        resp = redirect(url_for('default_route'))
        set_log_scope_to_cookie(resp)
        return resp

    return render_template('form.html', context=context, form=form)


# ========================
# Log Search
# ========================

@flask_app.route('/search-logs')
def get_search_logs_route():
    get_cookies(req=request)
    log_group_ocid = get_log_group_scope()
    log_ocid = get_log_scope()

    if log_group_ocid is None or log_ocid is None:
        raise UserWarning('need to set both log group OCID and log OCID')

    data = search_logs(log_group_ocid, log_ocid)
    return serialize_response(data)


@flask_app.route('/search-logs/where/{where_clause}')
def get_search_logs_where_route(where_clause):
    get_cookies(req=request)
    log_group_ocid = get_log_group_scope()
    log_ocid = get_log_scope()

    if log_group_ocid is None or log_ocid is None:
        raise UserWarning('need to set both log group OCID and log OCID')

    data = search_logs(log_group_ocid, log_ocid, where_clause=where_clause)
    return serialize_response(data)


# ========================
# Custom Metrics
# ========================

@flask_app.route('/put_custom_metric')
def put_custom_metric_route():
    get_cookies(req=request)
    data = put_metric()
    return serialize_response(data)


# ========================
# Audit Events
# ========================

@flask_app.route('/audit')
def get_audit_events():
    get_cookies(req=request)
    data = list_audit_events()
    return serialize_response(data)

# ========================
# Cross Regional
# ========================

@flask_app.route('/search-cross-regional')
def get_search_cross_regional():
    get_cookies(req=request)
    data = exec_cross_regional(['us-phoenix-1','ap-chuncheon-1'], list_audit_events)
    return serialize_response(data)

# ========================
# Helper
# ========================

def get_cookies(req):
    get_compartment_scope_from_cookie(req)


def serialize_response(data):
    serialized = json.dumps(data, indent=2, cls=CustomJSONEncoder)
    response = flask_app.response_class(
        response=serialized,
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    flask_app.run()

