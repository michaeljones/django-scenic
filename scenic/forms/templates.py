
from ..values import LiteralValue, StateValue

from .base import FormDisplay, build_form_state

class FormValue(object):

    def __init__(self, form):
        self.form = form

    def __call__(self, state, context):
        form_state = build_form_state(state, context, self.form)
        return FormDisplay(self.form, form_state)


class NamedFormContext(object):

    def __init__(self, named_forms):
        self.named_forms = named_forms

    def __iter__(self):

        context = {}
        for form in self.named_forms:
            context['{name}_form'.format(name=form.name)] = FormValue(form.form)
            context['{name}_helper'.format(name=form.name)] = LiteralValue(form.helper)

        return context.iteritems()

class FormDisplayValue(object):

    def __call__(self, state, context):
        return FormDisplay(state.form, state.form_state)


class StateFormContext(object):

    def __init__(self, name=None):
        self.name = name

    def __iter__(self):

        context = {}
        if self.name:
            context['{name}_form'.format(name=self.name)] = FormDisplayValue()
        else:
            context['form'] = StateValue('form')

        return context.iteritems()

