
from ...responses import RedirectResponse, TemplateResponse
from ...values import AbsoluteUrl, StateValue

from ..methods import NamedPostFormHandler
from ..templates import StateFormContext
from ..responses import SaveForm


def named_form_handler(named_form, template, action=None):

    if action is None:
        action = SaveForm('object')

    return NamedPostFormHandler(
        named_form,
        RedirectResponse(
            AbsoluteUrl(StateValue('object')),
            action,
            ),
        TemplateResponse(template, StateFormContext(named_form.name))
        )

