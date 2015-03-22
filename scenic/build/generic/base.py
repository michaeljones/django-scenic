
from ...methods import GetHandler
from ...templates import Template, NullContext
from ...responses import TemplateResponse
from ...views import View


def template_view(
        template_name,
        context,
        ):

    return View(GetHandler(TemplateResponse(Template(template_name, context), NullContext())))
