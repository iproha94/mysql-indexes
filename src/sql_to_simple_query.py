import sqlparse
from sqlparse.tokens import Keyword, Name
from sqlparse.sql import Where, Comparison

from expressions import *


def get_table_name(query):
    try:
        query_tokens = sqlparse.parse(query)[0].tokens

        table_name = None
        was_keyword_from = False
        for token in query_tokens:
            if not was_keyword_from and token.ttype is not Keyword:
                continue

            was_keyword_from = True

            if token.ttype is not None:
                continue

            table_name = str(token)
            break

        return table_name
    except Exception:
        return None


def get_columns_name(query):
    try:
        columns_name_where = _get_columns_name_for_where(query)
        columns_name_order_by = _get_columns_name_for_order_by(query)

        arr = list(columns_name_where | columns_name_order_by)
        arr.sort()

        return arr
    except Exception:
        return []


def _get_columns_name_for_where(query):
    try:
        query_tokens = sqlparse.parse(query)[0].tokens

        where_tokens = None
        for token in query_tokens:
            if isinstance(token, Where):
                where_tokens = token.tokens
                break

        columns_name_where = set()
        for token in where_tokens:
            if isinstance(token, Comparison):
                columns_name_where.add(str(token.left.tokens[0]))

        return columns_name_where
    except Exception:
        return set()


def _get_columns_name_for_order_by(query):
    try:
        query_tokens = sqlparse.parse(query)[0].tokens

        order_tokens = None
        i = 0
        while i < len(query_tokens):
            token = query_tokens[i]

            if token.value == "order":
                order_tokens = query_tokens[i + 4].tokens
                break

            i += 1

        columns_name_order_by = set()
        for token in order_tokens:
            if token.ttype is None or token.ttype is Name:
                columns_name_order_by.add(token.value.split()[0])

        return columns_name_order_by
    except Exception:
        return set()


def get_where(query, columns_name):
    try:
        query_tokens = sqlparse.parse(query)[0].tokens

        where_tokens = None
        for token in query_tokens:
            if isinstance(token, Where):
                where_tokens = token.tokens
                break

        where = []
        for token in where_tokens:
            if isinstance(token, Comparison):
                comparison = str(token).split()
                where.append(ConditionalExpression(
                    field=Field(column_number=columns_name.index(comparison[0])),
                    operator=OperatorbySymbol[comparison[1]],
                    args=[Arg(type=ArgType.value, value=comparison[2])]
                ))

        return where
    except Exception:
        return []


def get_order_by(query, columns_name):
    try:
        query_tokens = sqlparse.parse(query)[0].tokens

        order_tokens = None
        i = 0
        while i < len(query_tokens):
            token = query_tokens[i]

            if token.value == "order":
                order_tokens = query_tokens[i + 4].tokens
                break

            i += 1

        order_by = []
        for token in order_tokens:
            if token.ttype is None or token.ttype is Name:
                order_by.append(OrderByExpression(
                    field=Field(column_number=columns_name.index(token.value.split()[0])),
                    asc=False if len(token.value.split()) > 1 and token.value.split()[1] == "desc" else True
                ))
            elif token.ttype is Keyword.Order:
                order_by[-1].asc = False if token.value == "desc" else True

        return order_by
    except Exception:
        return []
