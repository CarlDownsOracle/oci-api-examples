import json
from datetime import datetime


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            result = obj.__dict__
            return result

        if isinstance(obj, datetime):
            result = obj.strftime("%m/%d/%Y, %H:%M:%S")
            return result

        return {}


def summarize(data):
    summary = list()

    if data is None:
        return summary

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
