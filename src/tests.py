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
        СonditionalExpression(
            field=Field(0, 1),
            operator=Operators.g,
            arguments=[1],
        ),
        СonditionalExpression(
            field=Field(1, 2),
            operator=Operators.e,
            arguments=[5],
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
        СonditionalExpression(
            field=Field(0, 1),
            operator=Operators.e,
            arguments=[5000],
        ),
        СonditionalExpression(
            field=Field(0, 2),
            operator=Operators.g,
            arguments=[3],
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
        СonditionalExpression(
            field=Field(1, 1),
            operator=Operators.e,
            arguments=[5000],
        ),
        СonditionalExpression(
            field=Field(1, 2),
            operator=Operators.g,
            arguments=[3],
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

simple_query1 = SimpleQuery(
        columns_name=['a', 'b', 'c', 'd'],
        where=[
            СonditionalExpression(
                field=Field(column_number=0),
                operator=Operators.e,
                arguments=[None]
            ),
            СonditionalExpression(
                field=Field(column_number=1),
                operator=Operators.e,
                arguments=[5000]
            ),
            СonditionalExpression(
                field=Field(column_number=2),
                operator=Operators.g,
                arguments=[3]
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


def test_print_join_query():
    print(query_ex3)


def test_print_simple_query():
    print(simple_query1)


def test_get_simple_query():
    print(query_ex3.get_simple_query(0))


test_print_simple_query()
test_print_join_query()
test_get_fullscan_table()
test_get_simple_query()
