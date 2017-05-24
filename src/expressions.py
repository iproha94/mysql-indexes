from enum import Enum

JoinType = Enum('JoinType', 'inner left right')
Operators = Enum('Operators', 'g ge e ne le l like')

OperatorbySymbol = {
    ">": Operators.g,
    ">=": Operators.ge,
    "=": Operators.e,
    "<>": Operators.ne,
    "<=": Operators.le,
    "<": Operators.l,
    "like": Operators.like,
}

ArgType = Enum('ArgType', 'value const null')


class Field:
    def __init__(
        self,
        table_number=None,
        column_number=None,
    ):
        self.table_number = table_number
        self.column_number = column_number

    def __repr__(self):
        return "{t}.{c}".format(
            t=self.table_number,
            c=self.column_number,
        )


class Arg:
    def __init__(
        self,
        type=ArgType.const,
        value=None,
    ):
        self.value = value
        self.type = type

    def __repr__(self):
        return "{}".format(self.value if self.type == ArgType.value else self.type)


class ConditionalExpression:
    def __init__(
        self, 
        field=None,
        operator=Operators.e,
        args=None,
    ):
        if args is None:
            args = []

        self.field = field
        self.operator = operator
        self.args = args

    def __repr__(self):
        return "{f} {op} {args}".format(
            f=self.field,
            op=self.operator,
            args=self.args
        )


class OnExpression:
    def __init__(
        self,
        fields=None,
        operator=Operators.e,
    ):
        if fields is None:
            fields = []

        self.operator = operator
        self.fields = fields

    def __repr__(self):
        return "{f1} {op} {f2}".format(
            f1=self.fields[0],
            f2=self.fields[1],
            op=self.operator,
        )


class OrderByExpression:
    def __init__(
        self, 
        field=None,
        asc=True,
    ):
        self.field = field
        self.asc = asc

    def __repr__(self):
        return "{f} {sort}".format(
            f=self.field,
            sort='asc' if self.asc else 'desc'
        )
