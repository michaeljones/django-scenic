
from itertools import chain

from django.template.response import TemplateResponse as DjangoTemplateResponse

from .values import StateValue


class DictContext(object):

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return self.data.iteritems()


class NullContext(object):

    def __iter__(self):
        # Iterate nothing, maybe just raise StopIteration error?
        return iter([])


class StateFormContext(object):

    def __init__(self, name=None):
        self.name = name

    def __iter__(self):

        context = {}
        if self.name:
            context['{name}_form'.format(name=self.name)] = StateValue('form')
        else:
            context['form'] = StateValue('form')

        return context.iteritems()


class FormValue(object):

    def __init__(self, form_factory):
        self.form_factory = form_factory

    def __call__(self, state, context):
        return self.form_factory.get(state, context)


class NamedFormContext(object):

    def __init__(self, named_forms):
        self.named_forms = named_forms

    def __iter__(self):

        context = {}
        for form in self.named_forms:
            context['{name}_form'.format(name=form.name)] = FormValue(form.form_factory)

        return context.iteritems()


class FormContext(object):

    def __init__(self, forms):
        self.forms = forms

    def __iter__(self):

        context = {}
        for name, form_factory in self.forms.iteritems():
            context['{name}_form'.format(name=name)] = FormValue(form_factory)

        return context.iteritems()


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
