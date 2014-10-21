
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


class FormFactory(object):

    def __init__(self, form_class, form_args_factory):
        self.form_class = form_class
        self.form_args_factory = form_args_factory

    def __call__(self, state, context):
        args, kwargs = self.form_args_factory(state, context)
        form = self.form_class(*args, **kwargs)
        return form


