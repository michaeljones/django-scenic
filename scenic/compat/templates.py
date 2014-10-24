
from ..values import StateValue

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
