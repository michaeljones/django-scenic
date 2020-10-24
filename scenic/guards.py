
from django.contrib.auth.views import redirect_to_login

from .views import BaseView


class LoginRequired(BaseView):

    def __init__(self, child):
        self.child = child

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path()
            )

        return self.child(request, *args, **kwargs)


class Guard(BaseView):

    def __init__(self, condition, response, view):
        self.condition = condition
        self.response = response
        self.view = view

    def dispatch(self, state, context):

        if self.condition(state, context):
            return self.response(state, context)

        return self.view.dispatch(state, context)

    def process(self, state, context):

        if self.condition(state, context):
            return self.response(state, context)

        return self.view.process(state, context)
