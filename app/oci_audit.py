import oci
from datetime import datetime, timedelta
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


@exception_sentinel()
def list_audit_events(minutes_back=5):

    # agent needs to be rebuilt each time because region scope can change where it's pointed
    audit_client = oci.audit.AuditClient(config)

    now = get_now_utc()
    start_time = now - timedelta(minutes=minutes_back)
    end_time = now

    response = audit_client.list_events(
        compartment_id=get_compartment_scope(),
        start_time=start_time,
        end_time=end_time)

    return response.data


