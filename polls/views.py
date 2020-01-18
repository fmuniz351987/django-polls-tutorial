from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		return Question.objects.filter(
			pub_date__lte=timezone.now()
		)


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		template = loader.get_template('polls/detail.html')
		context = {
			'question': question,
			'error_message': "You did't select a choice.",
		}
		return HttpResponse(template.render(context, request), status_code=400)
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return redirects when successfully dealing with POST data, to prevent 
		# it from being posted twice.
		return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
