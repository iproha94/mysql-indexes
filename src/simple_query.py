from expressions import *
from index import Index
import sql_to_simple_query as sql_to_sq


class SimpleQuery:
    def __init__(
            self,
            sql_query=None,
            table_name=None,
            columns_name=None,
            where=None,
            order_by=None
    ):
        if sql_query is not None:
            self._init_from_sql(sql_query)
        else:
            self.table_name = table_name

            if order_by is None:
                order_by = []
            self.order_by = order_by  # содержит элементы OrderByExpression

            if where is None:
                where = []
            self.where = where  # массив связанных объектов СonditionalExpression условием AND

            if columns_name is None:
                columns_name = []
            self.columns_name = columns_name

    def _init_from_sql(self, sql):
        sql = sql.lower()

        self.table_name = sql_to_sq.get_table_name(sql)

        sql = sql.replace("{}.".format(self.table_name), "")
        self.sql_query = sql

        self.columns_name = sql_to_sq.get_columns_name(sql)

        if len(self.columns_name) == 0:
            self.where = []
            self.order_by = []
        else:
            self.where = sql_to_sq.get_where(sql, self.columns_name)
            self.order_by = sql_to_sq.get_order_by(sql, self.columns_name)

    def __repr__(self):
        return """SimpleQuery
        sql: {sql}
        table_name: {table_name}
        columns_name: {columns_name}
        where: {where}
        order_by: {order_by} """.format(
            sql=self.sql_query,
            table_name=self.table_name,
            columns_name=self.columns_name,
            where=self.where,
            order_by=self.order_by
        )

    def get_index(self):
        index = Index(
            table_name=self.table_name,
            columns_name=self.columns_name,
        )

        for order_by in self.order_by:
            # if all(x.column_number != order_by.field.column_number for x in index.where_eq_fields):
            index.order_by_fields.append(order_by.field)

        for where in self.where:
            if (where.operator == Operators.e or \
                    (where.operator == Operators.like and '%' not in where.arguments[0])) and \
                    all(x.column_number != where.field.column_number for x in index.order_by_fields):
                index.where_eq_fields.append(where.field)

        for where in self.where:
            if (where.operator in [Operators.g, Operators.ge, Operators.l, Operators.le, Operators.ne] or
                    (where.operator == Operators.like and where.args[0][-1] == '%')) and \
                    all(x.column_number != where.field.column_number for x in index.where_eq_fields) and \
                    all(x.column_number != where.field.column_number for x in index.order_by_fields):
                index.where_not_eq_fields.append(where.field)

        return index


if __name__ == '__main__':
    import sys

    sql = str(sys.argv[1])
    query = SimpleQuery(sql_query=sql)
    print(query)
    print(query.get_index().sql())
