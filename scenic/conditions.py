
class Condition(object):

    def __invert__(self):
        return Invert(self)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)


class Invert(Condition):

    def __init__(self, cond):
        self.cond = cond

    def __call__(self, state, context):
        return not self.cond(state, context)


class And(Condition):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, state, context):
        return self.a(state, context) and self.b(state, context)


class Or(Condition):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, state, context):
        return self.a(state, context) or self.b(state, context)
