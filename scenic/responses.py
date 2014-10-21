
from django.http import HttpResponseRedirect
from django.contrib import messages


class SaveForm(object):

    def __call__(self, state, context):
        state.object = state.form.save()


class RedirectResponse(object):

    def __init__(self, url, child):
        self.url = url
        self.child = child

    def __call__(self, state, context):
        self.child(state, context)
        return HttpResponseRedirect(self.url(state, context))


class SuccessMessage(object):

    def __init__(self, child):
        self.child = child

    def __call__(self, state, context):
        self.child(state, context)

        success_message = self.get_message(state, context)
        if success_message:
            messages.success(context.request, success_message)


class SimpleSuccessMessage(object):

    def __init__(self, message, child):
        self.child = child
        self.message = message

    def __call__(self, state, context):
        self.child(state, context)

        message = self.message.format(**state.form.cleaned_data)
        messages.success(context.request, message)


class TemplateResponse(object):

    def __init__(self, template):
        self.template = template

    def __call__(self, state, context):
        return self.template.render_to_response(state, context, {'form': state.form})


