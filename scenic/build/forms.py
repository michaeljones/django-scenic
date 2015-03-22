
from ..responses import RedirectResponse, TemplateResponse
from ..values import AbsoluteUrl, StateValue
from ..forms.templates import StateFormContext
from ..forms.responses import SaveForm
from ..forms.methods import NamedPostFormHandler


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
