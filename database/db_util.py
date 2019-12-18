import re

import inflect
import pandas as pd
from sqlalchemy.ext.automap import generate_relationship
from sqlalchemy.orm import interfaces




def get_db_data_frame(sql, con):
    """

    Args:
        sql:
        con:

    Returns:

    """
    df = pd.read_sql_query(sql=sql, con=con)
    return df


def get_db_session_data_frame(sql, session):
    """

    Args:
        sql:
        session:

    Returns:

    """
    df = pd.read_sql_query(sql=sql, con=session.bind)
    return df


def data_frame(query, columns):
    """
    Takes a sqlalchemy query and a list of columns, returns a dataframe.
    """

    def make_row(x):
        return dict([(c, getattr(x, c)) for c in columns])

    return pd.DataFrame([make_row(x) for x in query])


def camelize_classname(base, tablename, table):
    """Produce a 'camelized' class name, e.g. """
    "'words_and_underscores' -> 'WordsAndUnderscores'"
    if tablename.rfind("v2_") > 0:
        tablename = tablename[tablename.rfind("v2_") + 3:]
    return str(tablename[0].upper() + \
               re.sub(r'_([a-z])', lambda m: m.group(1).upper(), tablename[1:]))


_pluralizer = inflect.engine()


def gen_relationship(base, direction, return_fn,
                     attrname, local_cls, referred_cls, **kw):
    if direction is interfaces.ONETOMANY:
        kw['cascade'] = 'all, delete-orphan'
        kw['passive_deletes'] = True
        # kw['single_parent'] = True

    # make use of the built-in function to actually return
    # the result.
    return generate_relationship(base, direction, return_fn,
                                 attrname, local_cls, referred_cls, **kw)
