import json
from datetime import datetime, timezone


def exception_sentinel():
    """
    Catches any exceptions raised in decorated functions, returning a dict which can be displayed to the user via HTML
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseException as err:
                return {'problem':err}
        return wrapper
    return decorator


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


def get_now_timestamp():
    return datetime.now().timestamp()

def datetime_to_logging_service_iso_format(value: datetime):
    return value.isoformat()[:-3] + "Z"


def datetime_to_iso_format(value: datetime):
    iso_format = value.isoformat()
    return iso_format.replace("+00:00", "Z")

def get_now_utc():
    return datetime.now(timezone.utc)
