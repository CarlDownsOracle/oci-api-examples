import oci
from datetime import datetime
from app.utils import *
from app.oci_config import *

config = get_configuration()

def preserve_region_scope(fn):

    def wrapper(*args, **kwargs):
        current_region = get_region_scope()
        try:
            return fn(*args, **kwargs)
        finally:
            set_scope('region', current_region)
    return wrapper


@preserve_region_scope
def exec_cross_regional(regions: list, fn):

    combined = []
    for region in regions:
        set_scope('region', region)
        combined.append(fn())
    return combined


def list_audit_events():

    # agent needs to be rebuilt each time because region scope can change where it's pointed
    audit_client = oci.audit.AuditClient(config)

    start_time = datetime.fromisoformat('2022-05-01')
    # start_time=datetime.strptime(
    #     "2014-08-30T03:51:11.684Z",
    #     "%Y-%m-%dT%H:%M:%S.%fZ"),

    end_time = datetime.fromisoformat('2022-05-02')
    # end_time=datetime.strptime(
    #     "2028-11-21T23:41:29.262Z",
    #     "%Y-%m-%dT%H:%M:%S.%fZ"),

    response = audit_client.list_events(
        compartment_id=get_compartment_scope(),
        start_time=start_time,
        end_time=end_time)

    return response.data


