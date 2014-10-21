
class SingleObject(object):

    def __init__(self, name, queryset):
        self.name = name
        self.queryset = queryset

    def __call__(self, state, context):
        if hasattr(state, 'object'):
            return state.object

        state.object = self.queryset.get(pk=context.kwargs[self.name])
        return state.object


class ObjectList(object):

    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, state, context):
        if hasattr(state, 'object_list'):
            return state.object_list

        state.object_list = self.queryset.all()
        return state.object_list


class AbsoluteUrl(object):

    def __call__(self, state, context):
        return state.object.get_absolute_url()


