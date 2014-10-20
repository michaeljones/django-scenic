
from django.template.response import TemplateResponse as DjangoTemplateResponse
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf.urls import url
from django import http


class UrlFactory(object):

    def __init__(self, lookup):
        self.lookup = lookup

    def __call__(self, pattern, name):

        return url(pattern, self.lookup[name], name=name)


class Template(object):

    def __init__(self, path, render_dict):
        self.path = path
        self.render_dict = render_dict

    def render_to_response(self, state, context, render_dict, **response_kwargs):
        for key, value in self.render_dict.iteritems():
            render_dict[key] = value(state, context)

        response_kwargs.setdefault('content_type', None)
        return DjangoTemplateResponse(
            request=context.request,
            template=[self.path],
            context=render_dict,
            **response_kwargs
            )


class TemplateFactory(object):

    def __init__(self, base):
        self.base = base

    def __call__(self, suffix, render_dict):
        return Template("{base}_{suffix}.html".format(base=self.base, suffix=suffix), render_dict)


class RequestContext(object):

    def __init__(self, request, args, kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs


class Empty(object):
    pass


class BaseView(object):

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __call__(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        state = Empty()
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(state, RequestContext(request, args, kwargs))

    def http_method_not_allowed(self, state, context):
        return http.HttpResponseNotAllowed(self._allowed_methods())

    def options(self, state, context):
        """
        Handles responding to requests for the OPTIONS HTTP verb.
        """
        response = http.HttpResponse()
        response['Allow'] = ', '.join(self._allowed_methods())
        response['Content-Length'] = '0'
        return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]


class View(BaseView):

    def __init__(self, get_handler=None, post_handler=None):
        self.get_handler = get_handler
        self.post_handler = post_handler

    def get(self, state, context):
        return self.get_handler.process(state, context)

    def post(self, state, context):
        return self.post_handler.process(state, context)


class LoginRequiredView(BaseView):

    def __init__(self, child):
        self.child = child

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(
                    request.get_full_path()
                    )

        return self.child(request, *args, **kwargs)


class UserArg(object):

    def __call__(self, state, context, args, kwargs):
        args.append(context.request.user)


class InstanceKwarg(object):

    def __init__(self, single_object):
        self.single_object = single_object

    def __call__(self, state, context, args, kwargs):
        kwargs['instance'] = self.single_object(state, context)


class InitialKwarg(object):

    def __init__(self, initial_data):
        self.initial_data = initial_data

    def __call__(self, state, context, args, kwargs):
        kwargs['initial'] = self.initial_data.copy()


class PostDataArgs(object):

    def __call__(self, state, context, args, kwargs):
        kwargs.update({
            'data': context.request.POST,
            'files': context.request.FILES,
        })


class FormArgsFactory(object):

    def __init__(self, *args):
        self.args = args

    def __call__(self, state, context):
        args, kwargs = [], {}
        for entry in self.args:
            entry(state, context, args, kwargs)
        return args, kwargs


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
        if hasattr(state, 'objects'):
            return state.objects

        state.objects = self.queryset.all()
        return state.objects


class PostFormHandler(object):

    def __init__(self, form_factory, valid_response, invalid_response):
        self.form_factory = form_factory
        self.valid_response = valid_response
        self.invalid_response = invalid_response

    def process(self, state, context):
        state.form = self.form_factory(state, context)
        if state.form.is_valid():
            return self.valid_response(state, context)
        else:
            return self.invalid_response(state, context)


class GetFormHandler(object):

    def __init__(self, form_factory, template):
        self.form_factory = form_factory
        self.template = template

    def process(self, state, context):
        form = self.form_factory(state, context)
        return self.template.render_to_response(state, context, {'form': form})


class TemplateHandler(object):

    def __init__(self, template):
        self.template = template

    def process(self, state, context):
        return self.template.render_to_response(state, context, {})


class AbsoluteUrl(object):

    def __call__(self, state, context):
        return state.object.get_absolute_url()


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


class SaveForm(object):

    def __call__(self, state, context):
        state.object = state.form.save()


class TemplateResponse(object):

    def __init__(self, template):
        self.template = template

    def __call__(self, state, context):
        return self.template.render_to_response(state, context, {'form': state.form})


class FormFactory(object):

    def __init__(self, form_class, form_args_factory):
        self.form_class = form_class
        self.form_args_factory = form_args_factory

    def __call__(self, state, context):
        args, kwargs = self.form_args_factory(state, context)
        form = self.form_class(*args, **kwargs)
        return form


