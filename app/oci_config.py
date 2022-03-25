from oci.config import validate_config
from oci.config import from_file
from app import flask_app
import os

configuration = None


def get_configuration():

    """
    get the config file
    typically expected in ~/.oci/config
    """

    global configuration
    if configuration is None:
        configuration = from_file(profile_name=get_oci_profile_name())
        # print("configuration: {}".format(configuration))

    return configuration


def validate_configuration():
    config = get_configuration()
    validate_config(config)
    # print("configuration validated")


def set_compartment_scope(compartment):
    compartment = compartment if compartment is not None and len(compartment) > 0 else None
    flask_app.config['compartment_scope'] = compartment


def get_tenancy_scope():
    return get_configuration().get('tenancy')


def get_compartment_scope():
    return flask_app.config.get('compartment_scope')


def get_compartment_scope_from_cookie(request):
    ocid = request.cookies.get('oci-utilities-comp-ocid')
    set_compartment_scope(compartment=ocid)


def set_compartment_scope_to_cookie(resp):
    resp.set_cookie('oci-utilities-comp-ocid', get_compartment_scope())


def set_vcn_scope(vcn):
    vcn = vcn if vcn is not None and len(vcn) > 0 else None
    flask_app.config['vcn_scope'] = vcn


def get_vcn_scope():
    return flask_app.config.get('vcn_scope')

def get_oci_profile_name():
    return os.environ.get('OCI_CLI_PROFILE', 'DEFAULT')

