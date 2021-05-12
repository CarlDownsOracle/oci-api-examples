from oci.config import validate_config
from oci.config import from_file

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
