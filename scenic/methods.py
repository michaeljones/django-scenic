
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


