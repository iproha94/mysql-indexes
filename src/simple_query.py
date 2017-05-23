from expressions import Operators


class Index:
    def __init__(
        self,
        fields=None,
    ):
        if fields is None:
            fields = []

        self.fields = fields

    def __repr__(self):
        return """index fields:
        {}""".format(
            self.fields
        )


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
        self.where = where #массив связанных объектов СonditionalExpression условием AND
        self.order_by = order_by #содержит элементы OrderByExpression

    def __repr__(self):
        return """SimpleQuery
        columns_name: {columns_name}
        where: {where}
        order_by: {order_by} """.format(
            columns_name=self.columns_name,
            where=self.where,
            order_by=self.order_by
        )

    def get_indexes(self):
        index = Index()

        index.fields.append(set())
        for where in self.where:
            if where.operator == Operators.e:
                index.fields[-1].add(where.field)

            elif where.operator == Operators.like and '%' not in where.arguments[0]:
                index.fields[-1].add(where.field)

        index.fields.append([])
        for order_by in self.order_by:
            index.fields[-1].append(order_by.field)

        # for where in self.where:
        #     elif where.operator == Operators.like and '%' in where.arguments[0] and  where.arguments[0][-1] == '%':
        #         index.fix_fields.append(where.column_name)

        #     elif where.operator != Operators.like:

        return index


if __name__ == '__main__':
    from expressions import *

