import oci
from app.utils import *
from app.oci_config import *

config = get_configuration()
# client = oci.resource_search.LogSearchClient(config)
# client = LogSearchClient(config)
client = oci.loggingsearch.LogSearchClient(config)

# see https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/using_the_api_searchlogs.htm

def search_logs(log_group_ocid, log_ocid):

    # search_query = "search \"{}/{}/{}\"".\
    #     format(get_compartment_scope(), log_group_ocid, log_ocid)

    search_query = "search \"{}/{}/{}\" | where data.action = 'ACCEPT'".\
        format(get_compartment_scope(), log_group_ocid, log_ocid)

    print(search_query)
    time_started = datetime.fromisoformat('2022-03-23')
    time_ended = datetime.fromisoformat('2022-03-25')

    details = oci.loggingsearch.models.SearchLogsDetails(
        time_start=time_started,
        time_end=time_ended,
        search_query=search_query,is_return_field_info=False)

    response = client.search_logs(search_logs_details=details,limit=10)

    return response.data
