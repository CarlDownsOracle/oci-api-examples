import oci
from app.utils import *
from app.oci_config import *
from datetime import datetime, timezone
import logging

config = get_configuration()

service_endpoint = 'https://telemetry-ingestion.' + get_region_scope() + '.oraclecloud.com'
monitoring_client = oci.monitoring.MonitoringClient(config, service_endpoint=service_endpoint)

# Send the request to service, some parameters are not required, see API
# doc for more info

@exception_sentinel()
def put_metric():

    namespace = 'utilities'
    metric_name = 'sample'
    resource_group = 'utilities'

    dimensions = {
        'something': 'wonderful'
    }

    metadata = {
        'meta-1': 'hello'
    }

    datapoint1 = oci.monitoring.models.Datapoint(timestamp=get_now_utc(),value=100,count=1)
    datapoint2 = oci.monitoring.models.Datapoint(timestamp=get_now_utc(),value=150,count=1)

    details = oci.monitoring.models.MetricDataDetails(
        namespace=namespace,
        compartment_id=get_compartment_scope(),
        name=metric_name,
        dimensions=dimensions,
        datapoints=[datapoint1, datapoint2],
        resource_group=resource_group,
        metadata=metadata)

    post_metric_data_details = oci.monitoring.models.PostMetricDataDetails(metric_data=[details])

    try:
        response = monitoring_client.post_metric_data(post_metric_data_details=post_metric_data_details)
        return response.data

    except BaseException as be:
        logging.error(str(be))
        return {'problem': str(be)}


"""
See https://docs.oracle.com/en-us/iaas/tools/python-sdk-examples/2.81.0/monitoring/post_metric_data.py.html
"""
# post_metric_data_response = monitoring_client.post_metric_data(
#     post_metric_data_details=oci.monitoring.models.PostMetricDataDetails(
#         metric_data=[
#             oci.monitoring.models.MetricDataDetails(
#                 namespace="EXAMPLE-namespace-Value",
#                 compartment_id="ocid1.test.oc1..<unique_ID>EXAMPLE-compartmentId-Value",
#                 name="EXAMPLE-name-Value",
#                 dimensions={
#                     'EXAMPLE_KEY_7xbR1': 'EXAMPLE_VALUE_sZLDjJB2x6UqvNMReIuJ'},
#                 datapoints=[
#                     oci.monitoring.models.Datapoint(
#                         timestamp=datetime.strptime(
#                             "2013-05-23T09:09:38.808Z",
#                             "%Y-%m-%dT%H:%M:%S.%fZ"),
#                         value=947.9934,
#                         count=293)],
#                 resource_group="EXAMPLE-resourceGroup-Value",
#                 metadata={
#                     'EXAMPLE_KEY_2Tpld': 'EXAMPLE_VALUE_Bgv1bNDUu6Mt5CPhiQvD'})],
#         batch_atomicity="NON_ATOMIC"),
#     opc_request_id="E78D1AGOKP0GYXL9LL9I<unique_ID>",
#     content_encoding="EXAMPLE-contentEncoding-Value")
#
# # Get the data from response
# print(post_metric_data_response.data)
