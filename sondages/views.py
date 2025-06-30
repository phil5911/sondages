from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from sondages.models import Question, Choix
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sondages.models import Vote
from .forms import CommentForm
from .models import Comment



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
    comments = Comment.objects.filter(question=question).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.user = request.user
            commentaire.question = question
            commentaire.save()
            return HttpResponseRedirect(reverse("sondage:detail", args=(question.id,)))
    else:
        form = CommentForm()
    return render(request, "sondage/detail.html", {
                  "question": question,
                  "form": form,
                  "comments": comments
    })

def results(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        # Préparation des données pour Chart.js
        choix_labels = list(question.choix_set.values_list('choix_text', flat=True))
        choix_votes = list(question.choix_set.values_list('votes', flat=True))

        context = {
            'question': question,
            'choix_labels': choix_labels,
            'choix_votes': choix_votes,
        }
        return render(request, "sondage/results.html", context)


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


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Vérifie si l'utilisateur a déjà voté
    if Vote.objects.filter(user=request.user, question=question).exists():
        messages.warning(request, "Tu as déjà voté pour cette question.")
        return HttpResponseRedirect(reverse("sondage:results", args=(question.id,)))

    try:
        choix = question.choix_set.get(pk=request.POST["choix"])
    except (KeyError, Choix.DoesNotExist):
        return render(request, "sondage/detail.html", {
            "question": question,
            "error_message": "Vous n'avez pas sélectionné un choix",
        })

    # Enregistre le vote
    Vote.objects.create(user=request.user, question=question, choix=choix)
    choix.votes += 1
    choix.save()
    return HttpResponseRedirect(reverse("sondage:results", args=(question.id,)))






