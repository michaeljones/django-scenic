
from ...methods import GetHandler
from ...templates import Template, NullContext
from ...responses import TemplateResponse, JsonResponse
from ...views import View


def template_view(
        template_name,
        context,
        ):

    return View(GetHandler(TemplateResponse(Template(template_name, context), NullContext())))


def json_view(json_generator):

    return View(GetHandler(JsonResponse(json_generator)))
