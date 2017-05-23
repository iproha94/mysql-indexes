from enum import Enum
from simple_query import *
from expressions import *

JoinType = Enum('JoinType', 'inner left right')


class JoinQuery:
    def __init__(
        self,
        tables_name=None,
        columns_name=None,
        join_type=JoinType.inner,
        on=None,
        where=None,
        order_by=None
    ):
        if columns_name is None:
            columns_name = []
        if order_by is None:
            order_by = []
        if where is None:
            where = []
        if on is None:
            on = []
        if tables_name is None:
            tables_name = []

        self.tables_name = tables_name
        self.columns_name = columns_name
        self.join_type = join_type
        self.on = on
        self.where = where
        self.order_by = order_by

    def get_optimization_join(self):
        if self.join_type == JoinType.left:
            if any(where.field.table_number == 1 for where in self.where):
                return JoinType.inner

        elif self.join_type == JoinType.right:
            if any(where.field.table_number == 0 for where in self.where):
                return JoinType.inner

        return self.join_type

    def get_fullscan_table(self):
        optimization_join = self.get_optimization_join()

        if optimization_join == JoinType.inner:
            if len(self.order_by) > 0:
                return self.order_by[0].field.table_number
            else:
                return None

        elif self.join_type == JoinType.left:
            return 0
        elif self.join_type == JoinType.right:
            return 1

        return None

    def get_simple_queries(self):
        return self._get_simple_query(0), self._get_simple_query(1)

    def _get_simple_query(self, table_number):
        fullscan_table = self.get_fullscan_table()

        query = SimpleQuery()
        for on in self.on:
            for field in on.fields:
                if field.table_number == table_number:
                    query.where.append(ConditionalExpression(
                        field=field,
                        operator=on.operator,
                        args=[Arg()],
                    ))

        for where in self.where:
            if where.field.table_number == table_number:
                query.where.append(where)

        for order_by in self.order_by:
            if order_by.field.table_number != fullscan_table:
                break

            if order_by.field.table_number == table_number:
                query.order_by.append(order_by)

        return query

    def get_indexes(self):
        fullscan_table = self.get_fullscan_table()

        indexes = []
        if fullscan_table is not None:
            indexes.append(self._get_simple_query(0).get_index())
            indexes.append(self._get_simple_query(1).get_index())

            for on in self.on:
                indexes[fullscan_table].delete_fields(filter(lambda x: x.table_number == fullscan_table, on.fields))
        else:
            indexes.append(self._get_simple_query(0).get_index())
            indexes.append(self._get_simple_query(1).get_index())
            indexes.append(self._get_simple_query(0).get_index())
            indexes.append(self._get_simple_query(1).get_index())

            for on in self.on:
                indexes[1].delete_fields(filter(lambda x: x.table_number == 1, on.fields))
                indexes[2].delete_fields(filter(lambda x: x.table_number == 0, on.fields))

        return indexes

    def __repr__(self):
        return """JoinQuery
        columns({t1}): {ct1}, columns({t2}): {ct2}
        {t1} {join_type} JOIN {t2} ON {on}
        where: {where}
        order_by: {order_by} """.format(
            t1=self.tables_name[0],
            ct1=self.columns_name[0],
            t2=self.tables_name[1],
            ct2=self.columns_name[1],
            join_type=self.join_type,
            on=self.on,
            where=self.where,
            order_by=self.order_by
        )


if __name__ == '__main__':
    from expressions import *
