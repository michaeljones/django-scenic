
from ....responses import RedirectResponse, TemplateResponse
from ....templates import Template
from ....values import AbsoluteUrl, StateValue
from ....views import View

from ...responses import SaveForm
from ...forms import FormFactory
from ...methods import GetFormHandler, PostFormHandler
from ...templates import StateFormContext


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
