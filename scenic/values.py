
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from conditions import AttrCondition


class SingleObject(object):

    def __init__(self, name, cache_name, queryset):
        # Double underscores to avoid __getattr__ conflicts
        self.__name = name
        self.__cache_name = cache_name
        self.__queryset = queryset

    def __call__(self, state, context):
        try:
            return getattr(state, self.__cache_name)
        except AttributeError:
            try:
                value = self.__queryset.get(pk=context.kwargs[self.__name])
            except ObjectDoesNotExist:
                raise Http404()
            setattr(state, self.__cache_name, value)
            return value

    def __getattr__(self, name):
        return AttrCondition(self, name)


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


class ReverseUrl(object):

    def __init__(self, name, args=None, kwargs=None):
        self.name = name
        self.args = args or []
        self.kwargs = kwargs or {}

    def __call__(self, state, context):

        reverse_args = []
        for entry in self.args:
            reverse_args.append(entry(state, context))

        return reverse(self.name, args=reverse_args)


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


class UserValue(object):

    def __call__(self, state, context):
        return context.request.user
