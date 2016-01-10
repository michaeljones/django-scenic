
from json import JSONEncoder

from django.http import HttpResponseRedirect, HttpResponse as DjangoHttpResponse
from django.contrib import messages


class HttpResponse(object):

    def __init__(self, status):
        self.status = status

    def __call__(self, state, context):
        return DjangoHttpResponse(status=self.status)


class RedirectResponse(object):

    def __init__(self, url, child):
        self.url = url
        self.child = child

    def __call__(self, state, context):
        self.child(state, context)
        return HttpResponseRedirect(self.url(state, context))


class NullAction(object):

    def __call__(self, state, context):
        pass


class SuccessMessage(object):

    def __init__(self, child):
        self.child = child

    def __call__(self, state, context):
        self.child(state, context)

        success_message = self.get_message(state, context)
        if success_message:
            messages.success(context.request, success_message)

    def get_message(self):
        raise NotImplementedError()


class TemplateResponse(object):

    def __init__(self, template, template_context):
        self.template = template
        self.template_context = template_context

    def __call__(self, state, context):
        template_context = {}

        for key, value in self.template_context:
            template_context[key] = value(state, context)

        return self.template.render_to_response(state, context, template_context)


class JsonResponse(object):

    def __init__(self, json_generator):
        self.json_generator = json_generator

    def __call__(self, state, context):
        data = self.json_generator(state, context)
        return DjangoHttpResponse(
            JSONEncoder().encode(data),
            content_type='application/json',
            )
