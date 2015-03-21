
class GetHandler(object):

    def __init__(self, response):
        self.response = response

    def process(self, state, context):
        return self.response(state, context)
