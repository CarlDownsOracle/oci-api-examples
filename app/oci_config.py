from oci.config import validate_config
from oci.config import from_file
from app import app

configuration = None


def get_configuration():

    """
    get the config file
    typically expected in ~/.oci/config
    """

    global configuration
    if configuration is None:
        configuration = from_file()
        # print("configuration: {}".format(configuration))

    return configuration


def validate_configuration():
    config = get_configuration()
    validate_config(config)
    # print("configuration validated")


def set_compartment_scope(compartment):
    compartment = compartment if compartment is not None and len(compartment) > 0 else None
    app.config['compartment_scope'] = compartment


def get_compartment_scope():
    return app.config.get('compartment_scope')

