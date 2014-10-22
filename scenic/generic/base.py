
from ..methods import TemplateHandler
from ..templates import Template
from ..views import View


def template_view(
        template_name,
        context,
        ):

    return View(TemplateHandler(Template(template_name, context)))
