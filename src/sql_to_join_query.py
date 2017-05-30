from expressions import *

import sqlparse
from sqlparse.sql import Where, Comparison, IdentifierList, Identifier


def get_tables_name(query):
    query_tokens = sqlparse.parse(query)[0].tokens

    tables_name = []
    for token in query_tokens:
        if len(tables_name) == 2:
            break

        if token.ttype is None:
            tables_name.append(token.value)

    return tables_name


def _get_columns_table(query, tables_name):
    columns_name = set()
    query_tokens = sqlparse.parse(query)[0].tokens

    was_order = False

    for token in query_tokens:
        if isinstance(token, Comparison):
            if token.left.tokens[0].value == tables_name:
                columns_name.add(token.left.tokens[2].value)
            if token.right.tokens[0].value == tables_name:
                columns_name.add(token.right.tokens[2].value)

        if isinstance(token, Where):
            for token2 in token.tokens:
                if isinstance(token2, Comparison):
                    if token2.left.tokens[0].value == tables_name:
                        columns_name.add(token2.left.tokens[2].value)

        if isinstance(token, IdentifierList):
            for token2 in token.tokens:
                if isinstance(token2, Identifier) and \
                        isinstance(token2.tokens[0], Identifier) and \
                        tables_name == token2.tokens[0].tokens[0].value:
                    columns_name.add(token2.tokens[0].tokens[2].value)
                elif isinstance(token2, Identifier) and tables_name == token2.tokens[0].value:
                    columns_name.add(token2.tokens[2].value)

        if token.value == "order":
            was_order = True

        if was_order:
            if isinstance(token, Identifier) and \
                    isinstance(token.tokens[0], Identifier) and \
                    tables_name == token.tokens[0].tokens[0].value:
                columns_name.add(token.tokens[0].tokens[2].value)
            elif isinstance(token, Identifier) and tables_name == token.tokens[0].value:
                columns_name.add(token.tokens[2].value)

    columns_name = list(columns_name)
    columns_name.sort()
    return columns_name


def get_columns_name(query, tables_name):
    return [_get_columns_table(query, tables_name[0]), _get_columns_table(query, tables_name[1])]


def get_join_type(query):
    if query.find("left join") != -1:
        return JoinType.left
    elif query.find("right join") != -1:
        return JoinType.right
    else:
        return JoinType.inner


def get_on(query, tables_name, columns_name):
    on = []
    query_tokens = sqlparse.parse(query)[0].tokens

    for token in query_tokens:
        if isinstance(token, Comparison):
            t1 = tables_name.index(token.left.tokens[0].value)
            c1 = columns_name[t1].index(token.left.tokens[2].value)

            t2 = tables_name.index(token.right.tokens[0].value)
            c2 = columns_name[t2].index(token.right.tokens[2].value)

            on.append(
                OnExpression(
                    fields=[
                        Field(t1, c1),
                        Field(t2, c2),
                    ],
                    operator=OperatorbySymbol[token.tokens[2].value]
                )
            )

    return on


def get_where(query, tables_name, columns_name):
    where = []
    query_tokens = sqlparse.parse(query)[0].tokens

    tokens = []
    for token in query_tokens:
        if isinstance(token, Where):
            tokens = token.tokens
            break

    for token in tokens:
        if isinstance(token, Comparison):
            t = tables_name.index(token.left.tokens[0].value)
            c = columns_name[t].index(token.left.tokens[2].value)

            where.append(
                ConditionalExpression(
                    field=Field(t, c),
                    operator=OperatorbySymbol[token.tokens[2].value],
                    args=[Arg(type=ArgType.value, value=token.tokens[4].value)]
                )
            )

    return where


def get_order_by(query, tables_name, columns_name):
    order_by = []
    query_tokens = sqlparse.parse(query)[0].tokens

    tokens = []
    for token in query_tokens:
        if isinstance(token, IdentifierList):
            tokens = token.tokens
            break

    for token in tokens:
        if isinstance(token, Identifier):
            asc = True
            if isinstance(token.tokens[0], Identifier):
                t = tables_name.index(token.tokens[0].tokens[0].value)
                c = columns_name[t].index(token.tokens[0].tokens[2].value)
                asc = False if token.tokens[2].value == "desc" else True
            else:
                t = tables_name.index(token.tokens[0].value)
                c = columns_name[t].index(token.tokens[2].value)

            order_by.append(
                OrderByExpression(
                    field=Field(t, c),
                    asc=asc
                )
            )

    if len(tokens) == 0:
        was_order = False

        for token in query_tokens:
            if token.value == "order":
                was_order = True

            if was_order and isinstance(token, Identifier):
                asc = True
                if isinstance(token.tokens[0], Identifier):
                    t = tables_name.index(token.tokens[0].tokens[0].value)
                    c = columns_name[t].index(token.tokens[0].tokens[2].value)
                    asc = False if token.tokens[2].value == "desc" else True
                else:
                    t = tables_name.index(token.tokens[0].value)
                    c = columns_name[t].index(token.tokens[2].value)

                order_by.append(
                    OrderByExpression(
                        field=Field(t, c),
                        asc=asc
                    )
                )

    return order_by
