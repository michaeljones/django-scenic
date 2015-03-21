
from ...methods import GetHandler
from ...templates import Template
from ...views import View


def template_view(
        template_name,
        context,
        ):

    return View(GetHandler(Template(template_name, context)))
