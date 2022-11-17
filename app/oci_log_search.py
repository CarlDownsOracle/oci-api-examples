import oci
from datetime import timedelta
from app.utils import *
from app.oci_config import *
import logging

config = get_configuration()
client = oci.loggingsearch.LogSearchClient(config)

# see https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/using_the_api_searchlogs.htm

@exception_sentinel()
def search_logs(log_group_ocid, log_ocid, minutes_back=60, where_clause=None):

    search_scope = 'search "{}"'.format(get_compartment_scope())
    log_group_ocid = log_group_ocid.strip() if log_group_ocid else None
    log_ocid = log_ocid.strip() if log_ocid else None

    if log_group_ocid:
        search_scope = 'search "{}/{}"'.format(get_compartment_scope(), log_group_ocid)

        if log_ocid:
            search_scope = 'search "{}/{}/{}"'.format(get_compartment_scope(), log_group_ocid, log_ocid)

    if where_clause:
        search_query = '{}|{}'.format(search_scope, where_clause)
    else:
        search_query = search_scope

    logging.info(search_query)

    now = get_now_utc()
    start_time = now - timedelta(minutes=minutes_back)
    end_time = now

    details = oci.loggingsearch.models.SearchLogsDetails(
        time_start=start_time,
        time_end=end_time,
        search_query=search_query,
        is_return_field_info=False)

    response = client.search_logs(search_logs_details=details,limit=10)

    return response.data
