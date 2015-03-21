
class GetFormHandler(object):

    def __init__(self, form_factory, template):
        self.form_factory = form_factory
        self.template = template

    def process(self, state, context):
        form = self.form_factory.get(state, context)
        return self.template.render_to_response(state, context, {'form': form})


class PostFormHandler(object):

    def __init__(self, form_factory, valid_response, invalid_response):
        self.form_factory = form_factory
        self.valid_response = valid_response
        self.invalid_response = invalid_response

    def process(self, state, context):
        state.form = self.form_factory.post(state, context)
        if state.form.is_valid():
            return self.valid_response(state, context)
        else:
            return self.invalid_response(state, context)


class FormNotFound(Exception):
    """Exception for when incoming POST data doesn't seem to have come from any of the forms
    supported by this view.
    """


class NamedPostFormHandler(PostFormHandler):

    def __init__(self, named_form, valid_response, invalid_response):
        super(NamedPostFormHandler, self).__init__(
            named_form.form_factory, valid_response, invalid_response
        )
        self.name = named_form.name
        self.aliases = named_form.aliases


class PostMultiFormHandler(object):

    def __init__(self, named_handlers):
        self.named_handlers = named_handlers

    def _from_form(self, name, aliases, state, context):

        if name in context.request.POST:
            return True

        for entry in aliases:
            if entry in context.request.POST:
                return True

        return False

    def process(self, state, context):
        for handler in self.named_handlers:
            if self._from_form(handler.name, handler.aliases, state, context):
                return handler.process(state, context)

        raise FormNotFound('POST: %s' % context.request.POST)
