
class TemplateHandler(object):

    def __init__(self, template):
        self.template = template

    def process(self, state, context):
        return self.template.render_to_response(state, context, {})


