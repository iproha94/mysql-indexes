from expressions import Operators


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
    ):
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
        return "Index: {} {} {}".format(
            self.where_eq_fields,
            self.where_not_eq_fields,
            self.order_by_fields
        )

    def delete_fields(self, delete_fields):
        for delete_field in delete_fields:
            _delete_fields(self.where_eq_fields, delete_field)
            _delete_fields(self.where_not_eq_fields, delete_field)
            _delete_fields(self.order_by_fields, delete_field)

    def get_sql_query_create_index(self, tables_name, columns_name):
        pass


class SimpleQuery:
    def __init__(
            self,
            columns_name=None,
            where=None,
            order_by=None
    ):
        if order_by is None:
            order_by = []

        if where is None:
            where = []

        if columns_name is None:
            columns_name = []

        self.columns_name = columns_name
        self.where = where  # массив связанных объектов СonditionalExpression условием AND
        self.order_by = order_by  # содержит элементы OrderByExpression

    def __repr__(self):
        return """SimpleQuery
        columns_name: {columns_name}
        where: {where}
        order_by: {order_by} """.format(
            columns_name=self.columns_name,
            where=self.where,
            order_by=self.order_by
        )

    def get_index(self):
        index = Index()

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
