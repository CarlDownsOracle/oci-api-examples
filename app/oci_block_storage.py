import oci
from app.utils import *
from app.oci_config import *

# Initialize service client with default config file
core_client = oci.core.BlockstorageClient(config = get_configuration())

@exception_sentinel()
def list_volumes(compartment_id):

    # Send the request to service, some parameters are not required, see API
    # doc for more info
    list_volumes_response = core_client.list_volumes(
        compartment_id=compartment_id,
        # availability_domain="EXAMPLE-availabilityDomain-Value",
        # limit=94,
        # page="EXAMPLE-page-Value",
        # display_name="EXAMPLE-displayName-Value",
        # sort_by="TIMECREATED",
        # sort_order="ASC",
        # volume_group_id="ocid1.test.oc1..<unique_ID>EXAMPLE-volumeGroupId-Value",
        # lifecycle_state="FAULTY"
    )

    return list_volumes_response.data
