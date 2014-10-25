
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from scenic import all as sc

from .models import Choice, Poll


def create_main_index():

    return sc.View(
            sc.TemplateHandler(
                sc.Template('polls/main-index.html', sc.DictContext({})),
                )
            )

main_index = create_main_index()


def create_index():
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]

    return sc.View(
            sc.TemplateHandler(
                sc.Template('polls/index.html', sc.DictContext({})),
                )
            )

index = create_index()


def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})
