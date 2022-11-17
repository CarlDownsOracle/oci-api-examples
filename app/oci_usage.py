from oci.usage_api import UsageapiClientCompositeOperations
from oci.usage_api.models import CreateQueryDetails

import oci
from datetime import datetime, date
from app.oci_config import *
from app.utils import *

config = get_configuration()
usage_api_client = oci.usage_api.UsageapiClient(config)

@exception_sentinel()
def retrieve_usage_report():

    try:
        data = _perform_api_call()
        return _summarize(data)

    except Exception as e:
        return {"problem encountered": e.__repr__()}


def _summarize(data):
    summary = list()

    # for each UsageSummary object, show any non-None attributes
    # filtering out swagger types, the attribute map and tags

    for usage_summary in data.items:
        usage_summary_dict = usage_summary.__dict__
        line2 = dict()

        for key, value in usage_summary_dict.items():
            # filter out the metadata and tags
            if key in ['swagger_types', 'attribute_map', '_tags']:
                continue

            if value is not None:
                line2[key] = value

        summary.append(line2)

    return summary


def _perform_api_call():

    """
    """

    time_usage_started = datetime.fromisoformat('2021-07-01')
    time_usage_ended = datetime.fromisoformat('2021-09-03')

    time_forecast_started = datetime.fromisoformat('2021-10-01')
    time_forecast_ended = datetime.fromisoformat('2021-12-31')

    # group_by_tag = [
    #     oci.usage_api.models.Tag(
    #         namespace="EXAMPLE-namespace-Value",
    #         key="EXAMPLE-key-Value",
    #         value="EXAMPLE-value-Value")
    # ]

    dimensions = [
        oci.usage_api.models.Dimension(
            key="compartmentId",
            value=get_compartment_scope())
    ]

    # tags = [
    #     oci.usage_api.models.Tag(
    #         namespace="EXAMPLE-namespace-Value",
    #         key="EXAMPLE-key-Value",
    #         value="EXAMPLE-value-Value")
    # ]

    # usage_filter = oci.usage_api.models.Filter(
    #     operator="OR",
    #     dimensions=dimensions,
    #     tags=tags)

    usage_filter = oci.usage_api.models.Filter(
        operator="OR",
        dimensions=dimensions)

    request_summarized_usages_details = oci.usage_api.models.RequestSummarizedUsagesDetails(
        tenant_id=get_tenancy_scope(),
        time_usage_started=time_usage_started,
        time_usage_ended=time_usage_ended,
        granularity="DAILY",
        # granularity="MONTHLY",
        is_aggregate_by_time=True,
        # forecast=forecast,
        query_type="USAGE",
        # group_by=["EXAMPLE--Value"],
        # group_by_tag=group_by_tag,
        compartment_depth=1,
        filter=usage_filter)

    request_summarized_usages_response = usage_api_client.request_summarized_usages(
        request_summarized_usages_details)

    # Get the data from response
    # print(request_summarized_usages_response.data)
    return request_summarized_usages_response.data


def api_usage_example():

    """
    Send the request to service, some parameters are not required, see API doc for more info
    see https://docs.oracle.com/en-us/iaas/api/#/en/usage/20200107/UsageSummary/RequestSummarizedUsages
    """

    request_summarized_usages_response = usage_api_client.request_summarized_usages(
        request_summarized_usages_details=oci.usage_api.models.RequestSummarizedUsagesDetails(
            tenant_id="ocid1.test.oc1..<unique_ID>EXAMPLE-tenantId-Value",
            time_usage_started=datetime.strptime(
                "2009-01-07T11:52:04.982Z",
                "%Y-%m-%dT%H:%M:%S.%fZ"),
            time_usage_ended=datetime.strptime(
                "2033-04-12T09:10:32.375Z",
                "%Y-%m-%dT%H:%M:%S.%fZ"),
            granularity="TOTAL",
            is_aggregate_by_time=True,
            forecast=oci.usage_api.models.Forecast(
                        time_forecast_ended=datetime.strptime(
                            "2022-12-07T08:50:55.612Z",
                            "%Y-%m-%dT%H:%M:%S.%fZ"),
                forecast_type="BASIC",
                time_forecast_started=datetime.strptime(
                            "2013-04-14T22:37:06.489Z",
                            "%Y-%m-%dT%H:%M:%S.%fZ")),
            query_type="EXPIREDCREDIT",
            group_by=["EXAMPLE--Value"],
            group_by_tag=[
                oci.usage_api.models.Tag(
                    namespace="EXAMPLE-namespace-Value",
                    key="EXAMPLE-key-Value",
                    value="EXAMPLE-value-Value")],
            compartment_depth=2.434209,
            filter=oci.usage_api.models.Filter(
                operator="OR",
                dimensions=[
                    oci.usage_api.models.Dimension(
                        key="EXAMPLE-key-Value",
                        value="EXAMPLE-value-Value")],
                tags=[
                    oci.usage_api.models.Tag(
                        namespace="EXAMPLE-namespace-Value",
                        key="EXAMPLE-key-Value",
                        value="EXAMPLE-value-Value")])),
        opc_request_id="IN8FUBLH8NUNSHVZUVIS<unique_ID>",
        page="EXAMPLE-page-Value",
        limit=873)

    # Get the data from response
    print(request_summarized_usages_response.data)
