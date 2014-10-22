
from ..responses import RedirectResponse, TemplateResponse, SaveForm
from ..methods import GetFormHandler, PostFormHandler
from ..templates import Template, StateFormContext
from ..values import AbsoluteUrl, StateValue
from ..forms import FormFactory
from ..views import View


def form_view(
        template_name,
        context,
        form,
        form_args,
        action=None
        ):

    if action is None:
        action = SaveForm()

    form_factory = FormFactory(form, form_args)

    template = Template(template_name, context)

    return View(
        GetFormHandler(form_factory, template),
        PostFormHandler(
            form_factory,
            RedirectResponse(
                AbsoluteUrl(StateValue('object')),
                action
                ),
            TemplateResponse(template, StateFormContext())
            )
        )
