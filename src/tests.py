from expressions import *
from join_query import *

query_ex1 = JoinQuery(
    tables_name=['t1', 't2'],
    columns_name=[['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']],
    join_type=JoinType.left,
    on=[
        OnExpression(
            fields=[Field(0, 0), Field(1, 0)],
            operator=Operators.e,
        ),
    ],
    where=[
        ConditionalExpression(
            field=Field(0, 1),
            operator=Operators.g,
            args=[Arg(type=ArgType.value, value=1)],
        ),
        ConditionalExpression(
            field=Field(1, 2),
            operator=Operators.e,
            args=[Arg(type=ArgType.value, value=5)],
        ),
    ],
)

query_ex2 = JoinQuery(
    tables_name=['t1', 't2'],
    columns_name=[['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']],
    join_type=JoinType.left,
    on=[
        OnExpression(
            fields=[Field(0, 0), Field(1, 0)],
            operator=Operators.e,
        ),
    ],
    where=[
        ConditionalExpression(
            field=Field(0, 1),
            operator=Operators.e,
            args=[Arg(type=ArgType.value, value=5000)],
        ),
        ConditionalExpression(
            field=Field(0, 2),
            operator=Operators.g,
            args=[Arg(type=ArgType.value, value=3)],
        ),
    ],
    order_by=[
        OrderByExpression(
            field=Field(1, 2),
        ),
        OrderByExpression(
            field=Field(1, 3),
        ),
    ]
)

query_ex3 = JoinQuery(
    tables_name=['t1', 't2'],
    columns_name=[['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']],
    join_type=JoinType.left,
    on=[
        OnExpression(
            fields=[Field(0, 0), Field(1, 0)],
            operator=Operators.e,
        ),
    ],
    where=[
        ConditionalExpression(
            field=Field(1, 1),
            operator=Operators.e,
            args=[Arg(type=ArgType.value, value=5000)],
        ),
        ConditionalExpression(
            field=Field(1, 2),
            operator=Operators.g,
            args=[Arg(type=ArgType.value, value=3)],
        ),
    ],
    order_by=[
        OrderByExpression(
            field=Field(1, 2),
        ),
        OrderByExpression(
            field=Field(1, 3),
        ),
    ]
)

query_ex4 = JoinQuery(
    tables_name=['t1', 't2'],
    columns_name=[['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']],
    join_type=JoinType.left,
    on=[
        OnExpression(
            fields=[Field(0, 0), Field(1, 0)],
            operator=Operators.e,
        ),
    ],
    order_by=[
        OrderByExpression(
            field=Field(1, 1),
        )
    ]
)

query_ex5 = JoinQuery(
    tables_name=['t1', 't2'],
    columns_name=[['a', 'b', 'c'], ['a', 'b', 'c']],
    join_type=JoinType.inner,
    on=[
        OnExpression(
            fields=[Field(0, 0), Field(1, 0)],
            operator=Operators.e,
        ),
    ],
    where=[
        ConditionalExpression(
            field=Field(0, 1),
            operator=Operators.e,
            args=[Arg()],
        ),
    ],
    order_by=[
        OrderByExpression(
            field=Field(0, 2),
        ),
    ]
)

simple_query1 = SimpleQuery(
        columns_name=['a', 'b', 'c', 'd'],
        where=[
            ConditionalExpression(
                field=Field(column_number=0),
                operator=Operators.e,
                args=[Arg()]
            ),
            ConditionalExpression(
                field=Field(column_number=1),
                operator=Operators.e,
                args=[Arg(type=ArgType.value, value=5000)]
            ),
            ConditionalExpression(
                field=Field(column_number=2),
                operator=Operators.g,
                args=[Arg(type=ArgType.value, value=3)]
            ),
        ],
        order_by=[
            OrderByExpression(
                field=Field(column_number=2)
            ),
            OrderByExpression(
                field=Field(column_number=3)
            ),
        ]
    )


def test_get_fullscan_table():
    print("get_fullscan_table: %s" % ([
        query_ex1.get_fullscan_table() is None,
        query_ex2.get_fullscan_table() == 0,
        query_ex3.get_fullscan_table() == 1,
        query_ex4.get_fullscan_table() == 0
    ]))


def test_print_join_query(query):
    print(query)


def test_print_simple_query(query):
    print(query)


def test_get_simple_queries_for_join_query(query):
    sq1, sq2 = query.get_simple_queries()

    print(sq1)
    print(sq2)


def test_get_index_for_join_query(query):
    i1, i2 = query.get_indexes()
    print(i1)
    print(i2)

test_print_simple_query(simple_query1)
test_print_join_query(query_ex3)

test_get_fullscan_table()

test_get_index_for_join_query(query_ex5)

