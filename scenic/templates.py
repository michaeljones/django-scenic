
from itertools import chain

from django.template.response import TemplateResponse as DjangoTemplateResponse


class DictContext(object):

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return iter(self.data.items())


class NullContext(object):

    def __iter__(self):
        # Iterate nothing, maybe just raise StopIteration error?
        return iter([])


class MergeContext(object):

    def __init__(self, *children):
        self.children = children

    def __iter__(self):
        return iter(chain(*self.children))


class Template(object):

    def __init__(self, path, render_context):
        self.path = path
        self.render_context = render_context

    def render_to_response(self, state, context, render_dict, **response_kwargs):

        template_context = {}
        for key, value in self.render_context:
            template_context[key] = value(state, context)

        template_context.update(render_dict)

        response_kwargs.setdefault('content_type', None)
        return DjangoTemplateResponse(
            request=context.request,
            template=[self.path],
            context=template_context,
            **response_kwargs
        )


class TemplateFactory(object):

    def __init__(self, base):
        self.base = base

    def __call__(self, suffix, render_dict):
        return Template("{base}_{suffix}.html".format(base=self.base, suffix=suffix), render_dict)
