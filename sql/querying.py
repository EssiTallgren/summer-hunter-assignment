from dataclasses import asdict, dataclass
from typing import List, Optional

import pandas as pd
from config import DEFAULT_TABLE, logger
from jinja2 import PackageLoader
from jinjasql import JinjaSql

from sql.database import db_connection


@dataclass
class QueryParams:
    """Available query parameters.

    Take a look at ./templates/basic_query.sql.jinja
    to see where each field goes in the query if needed.
    """

    dimensions: List[str]
    table: str = DEFAULT_TABLE
    condition: Optional[str] = None
    group_by: Optional[List] = None
    order_by: Optional[List] = None


def query_db_to_df(query_params: QueryParams, result_columns: list) -> pd.DataFrame:
    """Query our db and get result as a dataframe."""
    query = _apply_sql_template(query_params)
    logger.info(
        f"Querying database with following query:"
        f"\n\n === YOUR SQL QUERY === {query} \n === SQL QUERY ENDS ==="
    )
    db_cursor = db_connection.cursor()
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return pd.DataFrame(result, columns=result_columns, index=None)


def _apply_sql_template(query_params: QueryParams) -> str:
    """Create SQL query from a jinja template given query parameters."""
    j = JinjaSql(param_style="qmark")
    j.env.loader = PackageLoader("sql", "templates")
    template = j.env.get_template("basic_query.sql.jinja")
    query, bind_params = j.prepare_query(template, asdict(query_params))
    for param in bind_params:
        query = query.replace("?", param, 1)
    return query
