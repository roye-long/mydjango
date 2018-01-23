from django.http import  HttpResponse,HttpResponseRedirect
from django.shortcuts import render ,get_object_or_404
from django.db.models import  *
from django.urls import reverse
from django.views import generic
from models import  Question, Choice
import json
# Create your views here.

'''def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    content={"latest_question_list":latest_question_list}
    #output = ', '.join([q.question_text for q in latest_question_list])
    return render(request, 'questIndex.html', content)
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'result.html', {'question': question})'''
def index(request):
    return render(request, 'questpage.html')

class IndexView(generic.ListView):
    template_name = 'questIndex.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):


        return Question.objects.order_by('id')
class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'result.html'
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        return render(request, 'detail.html', {
        'question': question,
        'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('questionnaire:result', args=(question.id,)))
def resultlook(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    conlist = Choice.objects.values('question__question_text').annotate(svotes=Sum('votes'))
    clist = Choice.objects.values("question__question_text", "choice_text").annotate(svotes=Sum('votes')).filter(question_id=question_id)
    cont = []
    cnt=[]
    for ave in conlist:
        cont.append(ave)
    for at in clist:
        cnt.append(at)
    content={"conlist":json.dumps(cont),"clist":json.dumps(cnt),"question":question}
    return render(request,"resultlook.html",content)