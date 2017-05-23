from expressions import Operators
from parse_sql import *

def _delete_fields(fields, delete_field):
    while True:
        try:
            fields.remove(delete_field)
        except Exception:
            break


class Index:
    def __init__(
            self,
            where_eq_fields=None,
            where_not_eq_fields=None,
            order_by_fields=None,
            table_name=None,
            columns_name=None,
    ):
        self.columns_name = columns_name
        self.table_name = table_name

        if order_by_fields is None:
            order_by_fields = []
        self.order_by_fields = order_by_fields

        if where_not_eq_fields is None:
            where_not_eq_fields = []
        self.where_not_eq_fields = where_not_eq_fields

        if where_eq_fields is None:
            where_eq_fields = []
        self.where_eq_fields = where_eq_fields

    def __repr__(self):
        fields = ', '.join(map(lambda x: self.columns_name[x.column_number], self.where_eq_fields + self.order_by_fields + self.where_not_eq_fields))

        if len(fields) == 0:
            return ""

        fields_for_name = ''.join(map(lambda x: self.columns_name[x.column_number], self.where_eq_fields + self.order_by_fields + self.where_not_eq_fields))
        index_name = "index_{}_{}".format(
            self.table_name,
            fields_for_name
        )

        return "create index {} on {}({});".format(
            index_name,
            self.table_name,
            fields
        )

    def delete_fields(self, delete_fields):
        for delete_field in delete_fields:
            _delete_fields(self.where_eq_fields, delete_field)
            _delete_fields(self.where_not_eq_fields, delete_field)
            _delete_fields(self.order_by_fields, delete_field)


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
            query = sql_query.lower()

            self.table_name = get_table_name(query)

            query = query.replace("{}.".format(self.table_name), "")
            self.columns_name = get_columns_name(query)
            self.where = get_where(query, self.columns_name)
            self.order_by = get_order_by(query, self.columns_name)
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

    def __repr__(self):
        return """SimpleQuery
        table_name: {table_name}
        columns_name: {columns_name}
        where: {where}
        order_by: {order_by} """.format(
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

        for where in self.where:
            if where.operator == Operators.e:
                index.where_eq_fields.append(where.field)
            elif where.operator == Operators.like and '%' not in where.arguments[0]:
                index.where_eq_fields.append(where.field)

        for order_by in self.order_by:
            if order_by.field not in index.where_eq_fields:
                index.order_by_fields.append(order_by.field)

        for where in self.where:
            if (where.operator in [Operators.g, Operators.ge, Operators.l, Operators.le, Operators.ne] or
                    (where.operator == Operators.like and where.args[0][-1] == '%')) and \
                    all(x.column_number != where.field.column_number for x in index.where_eq_fields) and \
                    all(x.column_number != where.field.column_number for x in index.order_by_fields):
                index.where_not_eq_fields.append(where.field)

        return index
