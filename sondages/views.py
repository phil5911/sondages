from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from sondages.models import Question, Choix
from django.template import loader
from django.urls import reverse


# Create your views here.

def index(request):
    questions = Question.objects.order_by("pub_date")[:5]
    #template = loader.get_template("sondage/index.html")
    context = {"questions": questions}
    #output = ", ".join([q.question_text for q in questions])
    #return HttpResponse(output)
    #return HttpResponse(template.render(context, request))
    return render(request, "sondage/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "sondage/detail.html", {"question": question})

def results(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, "sondage/results.html", {"question": question})
        #return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choix = question.choix_set.get(pk=request.POST["choix"])
    except (KeyError, Choix.DoesNotExist):
        return render(request, "sondage/detail.html", {"question":question, "error_message": "Vous n'avez pas sélectionné un choix"})
    else:
        choix.votes += 1
        choix.save()
        return HttpResponseRedirect(reverse("sondage:results", args=(question.id,)))






