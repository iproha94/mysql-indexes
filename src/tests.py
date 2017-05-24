from expressions import *
from join_query import *

jq1 = JoinQuery(
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

jq2 = JoinQuery(
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

jq3 = JoinQuery(
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

jq4 = JoinQuery(
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

jq5 = JoinQuery(
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

sq1 = SimpleQuery(
    table_name='t1',
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

sq2 = SimpleQuery(
    table_name='t2',
    columns_name=['a', 'b', 'c', 'd'],
    where=[
        ConditionalExpression(
            field=Field(column_number=0),
            operator=Operators.g,
            args=[Arg(type=ArgType.value, value=5)]
        ),
        ConditionalExpression(
            field=Field(column_number=2),
            operator=Operators.g,
            args=[Arg(type=ArgType.value, value=5)]
        ),
    ],
    order_by=[
        OrderByExpression(
            field=Field(column_number=0)
        ),
        OrderByExpression(
            field=Field(column_number=1)
        ),
    ]
)

def test_get_fullscan_table():
    print("get_fullscan_table: %s" % ([
        jq1.get_fullscan_table() is None,
        jq2.get_fullscan_table() == 0,
        jq3.get_fullscan_table() == 1,
        jq4.get_fullscan_table() == 0
    ]))


def test_print_join_query(query):
    print(query)
    print(list(map(lambda x: x.sql(), query.get_indexes())))


def test_print_simple_query(query):
    print(query)
    print(query.get_index())


def test_get_simple_queries_for_join_query(query):
    sq1, sq2 = query.get_simple_queries()

    print(sq1)
    print(sq2)


def test_get_index_for_join_query(query):
    print(query.get_indexes())


def test_simple_query_by_sql(sql):
    query = SimpleQuery(sql_query=sql)
    print(query)
    print(query.get_index())


def test_join_query_by_sql(sql):
    query = JoinQuery(sql_query=sql)
    # print(query)
    print(list(map(lambda x: x.sql(), query.get_indexes())))


# test_get_fullscan_table()
# test_print_simple_query(sq2)
# test_print_join_query(jq1)
# test_simple_query_by_sql("select * from t2 where a > 5 and b > 5 order by c, d desc;")

test_join_query_by_sql("select * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t1.b > 1 AND t2.c = 5")
test_join_query_by_sql("select * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t1.b = 5000 AND t1.c > 3 ORDER BY t2.c , t2.d")
test_join_query_by_sql("select * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t2.b = 5000 AND t2.c > 3 ORDER BY t2.c, t2.d")
test_join_query_by_sql("select * FROM t1 LEFT JOIN t2 ON t2.a = t1.a ORDER BY t2.b")
test_join_query_by_sql("select * FROM t1 INNER JOIN t2 ON t1.a = t2.a WHERE t1.b = 5 ORDER BY t1.c")


