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
        return """Index
        where_eq_fields: {}
        where_not_eq_fields: {}
        order_by_fields: {}
        sql: {}""".format(
            self.where_eq_fields,
            self.where_not_eq_fields,
            self.order_by_fields,
            self.sql()
        )

    def sql(self):
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
