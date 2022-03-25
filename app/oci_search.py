import oci
from app.utils import *
from app.oci_config import *

config = get_configuration()
search_client = oci.resource_search.ResourceSearchClient(config)

#  SAMPLE QUERIES
# https://docs.cloud.oracle.com/en-us/iaas/Content/Search/Concepts/queryoverview.htm
# https://docs.cloud.oracle.com/en-us/iaas/Content/Search/Concepts/samplequeries.htm
# https://console.us-ashburn-1.oraclecloud.com/search?


def search_by_ocid(ocid):

    if ocid is None:
        return []

    print("=========================================================")
    print("find {}".format(ocid))

    structured_search = oci.resource_search.models.StructuredSearchDetails(
            query="query all resources where identifier = '{}'".format(ocid),
            matching_context_type=oci.resource_search.models.SearchDetails.MATCHING_CONTEXT_TYPE_NONE,
            type='Structured')

    resources = search_client.search_resources(structured_search)

    if hasattr(resources, 'data'):
        return summarize(resources.data)
    else:
        return []
