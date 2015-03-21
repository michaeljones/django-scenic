
from django import http


class RequestContext(object):

    def __init__(self, request, args, kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs


class State(object):
    pass


class BaseView(object):

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __call__(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        state = State()
        context = RequestContext(request, args, kwargs)
        return self.dispatch(state, context)

    def dispatch(self, state, context):
        if context.request.method.lower() in self.http_method_names:
            handler = getattr(self, context.request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(state, context)

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

    def __init__(self, get=None, post=None):
        self.get_handler = get
        self.post_handler = post

    def get(self, state, context):
        return self.get_handler.process(state, context)

    def post(self, state, context):
        return self.post_handler.process(state, context)
