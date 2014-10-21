
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


class FormNotFound(Exception):
    """Exception for when incoming POST data doesn't seem to have come from any of the forms
    supported by this view.
    """


class PostMultiHandler(object):

    def __init__(self, form_handlers):
        self.form_handlers = form_handlers

    def _from_form(self, name, state, context):

        if name in context.request.POST:
            return True

        names = self.form_handlers[name].get_names()
        for entry in names:
            if entry in context.request.POST:
                return True

        return False

    def process(self, state, context):
        for name in self.form_handlers.iterkeys():
            if self._from_form(name, state, context):
                return self.form_handlers[name].process(state, context)

        raise FormNotFound('POST: %s' % context.request.POST)


class TemplateHandler(object):

    def __init__(self, template):
        self.template = template

    def process(self, state, context):
        return self.template.render_to_response(state, context, {})


class NamedHandler(object):

    def __init__(self, handler, names):
        self.handler = handler
        self.names = names

    def get_names(self):
        return self.names

    def process(self, state, context):
        return self.handler.process(state, context)
