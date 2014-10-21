
class SingleObject(object):

    def __init__(self, name, cache_name, queryset):
        self.name = name
        self.cache_name = cache_name
        self.queryset = queryset

    def __call__(self, state, context):
        try:
            return getattr(state, self.cache_name)
        except AttributeError:
            value = self.queryset.get(pk=context.kwargs[self.name])
            setattr(state, self.cache_name, value)
            return value


class ObjectList(object):

    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, state, context):
        if hasattr(state, 'object_list'):
            return state.object_list

        state.object_list = self.queryset.all()
        return state.object_list


class AbsoluteUrl(object):

    def __init__(self, object):
        self.object = object

    def __call__(self, state, context):
        object = self.object(state, context)
        return object.get_absolute_url()


class StateValue(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, state, context):
        return getattr(state, self.name)


class AttrValue(object):

    def __init__(self, object, name):
        self.object = object
        self.name = name

    def __call__(self, state, context):
        object = self.object(state, context)
        return getattr(object, self.name)


class LiteralValue(object):

    def __init__(self, value):
        self.value = value

    def __call__(self, state, context):
        return self.value
