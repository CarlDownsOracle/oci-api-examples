from flask import render_template, url_for, request
from werkzeug.utils import redirect
from app.forms import *
from app.utils import *

from app.oci_compute_networking import *
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


@flask_app.route('/choose-compartment', methods=['GET', 'POST'])
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


@flask_app.route('/compartment-details')
def get_compartment_details():
    get_cookies(req=request)
    data = search_by_ocid(get_compartment_scope())
    return serialize_response(data)


@flask_app.route('/validate')
def get_validate_route():
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

@flask_app.route('/compute-details')
def get_compute_route():
    get_cookies(req=request)
    data = get_compute_instances_details()
    return serialize_response(data)


@flask_app.route('/compute-status')
def get_compute_status_route():
    get_cookies(req=request)
    data = get_compute_instances_status()
    return serialize_response(data)


@flask_app.route('/compute-start')
def start_compute_route():
    get_cookies(req=request)
    data = start_all_compute_instances()
    return serialize_response(data)


@flask_app.route('/compute-stop')
def stop_compute_route():
    get_cookies(req=request)
    data = stop_all_compute_instances()
    return serialize_response(data)

# ========================
# Block Storage
# ========================

@flask_app.route('/block-volumes')
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


@flask_app.route('/vcn-with-attached-compute')
def get_vcn_compute_digest_route():
    get_cookies(req=request)
    data = vcn_with_attached_compute()
    return serialize_response(data)


@flask_app.route('/vcn-topology/<vcn>')
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


@flask_app.route('/search-for-ocid', methods=['GET', 'POST'])
def get_search_for_ocid_form_route():
    get_cookies(req=request)

    context = {}
    form = SearchForOcidForm()

    if form.validate_on_submit():
        choice = form.ocid_field
        resp = redirect(url_for('get_search_for_ocid_exec_route', ocid=choice.data))
        return resp

    return render_template('form.html', context=context, form=form)


@flask_app.route('/search-for-ocid/<ocid>')
def get_search_for_ocid_exec_route(ocid):
    get_cookies(req=request)
    data = search_by_ocid(ocid)
    return serialize_response(data)


# ========================
# Logging
# ========================

@flask_app.route('/choose-log-group', methods=['GET', 'POST'])
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

@flask_app.route('/clear-log-group')
def clear_log_group_scope_route():
    set_log_group_scope(None)
    resp = redirect(url_for('default_route'))
    set_log_group_scope_to_cookie(resp)
    return resp


@flask_app.route('/choose-log', methods=['GET', 'POST'])
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


@flask_app.route('/clear-log')
def clear_log_scope_route():
    set_log_scope(None)
    resp = redirect(url_for('default_route'))
    set_log_scope_to_cookie(resp)
    return resp


# ========================
# Log Search
# ========================

@flask_app.route('/search-logs')
def get_search_logs_route():
    get_cookies(req=request)
    log_group_ocid = get_log_group_scope()
    log_ocid = get_log_scope()

    data = search_logs(log_group_ocid, log_ocid)
    return serialize_response(data)


@flask_app.route('/search-logs-for-content-form', methods=['GET', 'POST'])
def get_search_logs_for_content_form_route():
    get_cookies(req=request)

    context = {}
    form = LogSearchForContentForm()

    if form.validate_on_submit():
        choice = form.log_content_field

        # handle case where user provides a search term (or not)
        if len(choice.data):
            resp = redirect(url_for('get_search_logs_for_content_exec_route', content=choice.data))
        else:
            resp = redirect(url_for('get_search_logs_route'))

        return resp

    return render_template('form.html', context=context, form=form)


@flask_app.route('/search-logs-for-content/<content>')
def get_search_logs_for_content_exec_route(content):
    get_cookies(req=request)
    log_group_ocid = get_log_group_scope()
    log_ocid = get_log_scope()

    where_clause = "logContent='*{}*' ".format(content)
    data = search_logs(log_group_ocid, log_ocid, where_clause=where_clause)
    return serialize_response(data)


@flask_app.route('/search-log-window-form', methods=['GET', 'POST'])
def get_search_logs_window_form_route():
    get_cookies(req=request)

    context = {}
    form = LogSearchWindowForm()

    if form.validate_on_submit():
        choice = form.log_content_day_starting_offset

        # handle case where user provides aa window
        if len(choice.data):
            resp = redirect(url_for('get_search_logs_window_route', days=choice.data))
        else:
            resp = redirect(url_for('get_search_logs_route'))

        return resp

    message = 'The Search API supports a maximum 14 day search "window".  Enter some value > 14 to see the effect.'
    return render_template('form.html', context=context, form=form, message=message)


@flask_app.route('/search-log-window/<days>')
def get_search_logs_window_route(days):
    get_cookies(req=request)
    log_group_ocid = get_log_group_scope()
    log_ocid = get_log_scope()

    # The search API supports a maximum 14 day window.
    window_in_minutes = 60 * 24 * 14
    starting_offset_in_minutes = 60 * 24 * int(days)
    ending_offset_in_minutes = starting_offset_in_minutes - window_in_minutes

    data = search_logs(log_group_ocid,
                       log_ocid,
                       start_minutes_back=starting_offset_in_minutes,
                       end_minutes_back=ending_offset_in_minutes)

    return serialize_response(data)


# ========================
# Custom Metrics
# ========================

@flask_app.route('/put-custom-metric')
def put_custom_metric_route():
    get_cookies(req=request)
    data = put_metric()
    return serialize_response(data)


# ========================
# Audit Events
# ========================

@flask_app.route('/list-audit')
def get_audit_events_route():
    get_cookies(req=request)
    data = list_audit_events()
    return serialize_response(data)


@flask_app.route('/list-audit-cross-regional')
def get_audit_events_across_regions_route():
    get_cookies(req=request)
    data = exec_cross_regional(['us-phoenix-1','us-ashburn-1'], list_audit_events)
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

