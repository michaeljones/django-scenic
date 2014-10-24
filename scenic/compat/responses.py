
from django.contrib import messages


class SaveForm(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, state, context):
        setattr(state, self.name, state.form.save())


class SimpleSuccessMessage(object):

    def __init__(self, message, child):
        self.child = child
        self.message = message

    def __call__(self, state, context):
        self.child(state, context)

        message = self.message.format(**state.form.cleaned_data)
        messages.success(context.request, message)
