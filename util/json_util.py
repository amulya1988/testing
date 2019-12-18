from flask import jsonify
from sqlalchemy import inspect


def to_json(obj):
    return jsonify(to_dict(obj))


def object_as_dict(obj):
    if obj is not None:
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
    else:
        return None


def get_object_props(obj):
    return [c.key for c in inspect(obj).mapper.column_attrs]


def to_dict(obj):
    if type(obj) is list:
        return [object_as_dict(u) for u in obj]
    else:
        return object_as_dict(obj)
