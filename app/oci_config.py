from oci.config import validate_config
from oci.config import from_file
from app import flask_app
import os
import logging

configuration = None


def get_oci_profile_name():
    return os.environ.get('OCI_CLI_PROFILE', 'DEFAULT')


def get_configuration():

    """
    get the config file
    typically expected in ~/.oci/config
    """

    global configuration
    if configuration is None:
        configuration = from_file(profile_name=get_oci_profile_name())
        logging.debug("configuration: {}".format(configuration))

    return configuration


def validate_configuration():
    config = get_configuration()
    validate_config(config)
    logging.debug("configuration validated")


def set_scope(key: str, value: str):
    global configuration
    configuration[key] = value

# ----------------------------
# Tenancy Scope
# ----------------------------

def get_tenancy_scope():
    return get_configuration().get('tenancy')

# ----------------------------
# Region Scope
# ----------------------------

def get_region_scope():
    return get_configuration().get('region')


# ----------------------------
# Compartment Scope
# ----------------------------

def get_compartment_scope():
    return flask_app.config.get('compartment_scope')


def set_compartment_scope(compartment):
    compartment = compartment if compartment is not None and len(compartment) > 0 else None
    flask_app.config['compartment_scope'] = compartment


def get_compartment_scope_from_cookie(request):
    ocid = request.cookies.get('compartment_scope')
    set_compartment_scope(compartment=ocid)
    return ocid


def set_compartment_scope_to_cookie(resp):
    update_cookie(resp, 'compartment_scope', get_compartment_scope())

# ----------------------------
# VCN Scope
# ----------------------------

def set_vcn_scope(vcn):
    vcn = vcn if vcn is not None and len(vcn) > 0 else None
    flask_app.config['vcn_scope'] = vcn


def get_vcn_scope():
    return flask_app.config.get('vcn_scope')

# ----------------------------
# Log Group Scope
# ----------------------------

def get_log_group_scope():
    return flask_app.config.get('log_group_scope')


def set_log_group_scope(log_group_ocid):
    log_group_ocid = log_group_ocid if log_group_ocid is not None and len(log_group_ocid) > 0 else None
    flask_app.config['log_group_scope'] = log_group_ocid


def get_log_group_scope_from_cookie(request):
    ocid = request.cookies.get('log_group_scope')
    set_log_group_scope(log_group_ocid=ocid)
    return ocid


def set_log_group_scope_to_cookie(resp):
    update_cookie(resp, 'log_group_scope', get_log_group_scope())

# ----------------------------
# Log Scope
# ----------------------------

def get_log_scope():
    return flask_app.config.get('log_scope')


def set_log_scope(log_ocid):
    log_ocid = log_ocid if log_ocid is not None and len(log_ocid) > 0 else None
    flask_app.config['log_scope'] = log_ocid


def get_log_scope_from_cookie(request):
    ocid = request.cookies.get('log_scope')
    set_log_scope(log_ocid=ocid)
    return ocid


def set_log_scope_to_cookie(resp):
    update_cookie(resp, 'log_scope', get_log_scope())

# ----------------------------
# Helpers
# ----------------------------

def update_cookie(resp, key, value):
    if value:
        resp.set_cookie(key, value)
    else:
        resp.delete_cookie(key)
