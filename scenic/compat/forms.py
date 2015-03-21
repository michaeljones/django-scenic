
class UserArg(object):

    def __call__(self, state, context, args, kwargs):
        args.append(context.request.user)


class ValueArg(object):

    def __init__(self, value):
        self.value = value

    def __call__(self, state, context, args, kwargs):
        args.append(self.value(state, context))


class InstanceKwarg(object):

    def __init__(self, single_object):
        self.single_object = single_object

    def __call__(self, state, context, args, kwargs):
        kwargs['instance'] = self.single_object(state, context)


class InitialKwarg(object):

    def __init__(self, initial_data):
        self.initial_data = initial_data

    def __call__(self, state, context, args, kwargs):

        initial = {}
        for key, value in self.initial_data:
            initial[key] = value(state, context)

        kwargs['initial'] = initial


class AbsoluteUrlArg(object):

    def __init__(self, object):
        self.object = object

    def __call__(self, state, context, args, kwargs):
        object = self.object(state, context)
        args.append(object.get_absolute_url())


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

    def __init__(self, form_class, form_args):
        self.form_class = form_class
        self.form_args = form_args

    def get(self, state, context):
        args, kwargs = FormArgsFactory(*self.form_args)(state, context)
        form = self.form_class(*args, **kwargs)
        return form

    def post(self, state, context):
        post_form_args = self.form_args + [PostDataArgs()]
        args, kwargs = FormArgsFactory(*post_form_args)(state, context)
        form = self.form_class(*args, **kwargs)
        return form


class NamedForm(object):

    def __init__(self, name, aliases, form_factory):
        self.name = name
        self.aliases = aliases
        self.form_factory = form_factory
