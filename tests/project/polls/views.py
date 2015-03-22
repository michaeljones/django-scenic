
from scenic.build.generic.base import template_view
from scenic.decorators import scenic
from scenic import all as sc

from .models import Choice, Poll


@scenic
def main_index():
    return template_view('polls/main-index.html', sc.NullContext())


@scenic
def index():
    context = sc.DictContext({
        'latest_poll_list': sc.LiteralValue(Poll.objects.all().order_by('-pub_date')[:5])
    })
    return sc.View(
        sc.GetHandler(
            sc.TemplateResponse(
                sc.Template('polls/index.html', context),
                {}
            )
        )
    )


@scenic
def detail():
    context = sc.DictContext({
        'poll': sc.SingleObject('poll_id', 'poll', Poll.objects)
    })
    return sc.View(
        sc.GetHandler(
            sc.TemplateResponse(
                sc.Template('polls/detail.html', context),
                {}
            )
        )
    )


class VotePostHandler(object):

    def __init__(self, poll, valid_response, invalid_response):
        self.poll = poll
        self.valid_response = valid_response
        self.invalid_response = invalid_response

    def process(self, state, context):

        poll = self.poll(state, context)

        try:
            selected_choice = poll.choice_set.get(pk=context.request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the poll voting form.
            return self.invalid_response(state, context)
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return self.valid_response(state, context)


@scenic
def vote():

    poll = sc.SingleObject('poll_id', 'poll', Poll.objects)
    context = sc.DictContext({
        'poll': poll,
        'error_message': sc.LiteralValue("You didn't select a choice.")
    })

    return sc.View(
        get=None,
        post=VotePostHandler(
            poll,
            sc.RedirectResponse(
                sc.ReverseUrl('polls:results', args=(poll.id,)),
                sc.NullAction()
            ),
            sc.TemplateResponse(
                sc.Template('polls/detail.html', context),
                {}
            ),
        )
    )


@scenic
def results():
    context = sc.DictContext({
        'poll': sc.SingleObject('poll_id', 'poll', Poll.objects)
    })
    return sc.View(
        sc.GetHandler(
            sc.TemplateResponse(
                sc.Template('polls/results.html', context),
                {}
            )
        )
    )
