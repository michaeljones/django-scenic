
from django.contrib.auth.views import redirect_to_login
from django import http

from .views import BaseView


class LoginRequired(BaseView):

    def __init__(self, child):
        self.child = child

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(
                    request.get_full_path()
                    )

        return self.child(request, *args, **kwargs)


class Guard(BaseView):

    def __init__(self, condition, child):
        self.condition = condition
        self.child = child

    def dispatch(self, state, context):

        if self.condition(state, context):
            raise http.Http404

        return self.child.dispatch(state, context)


