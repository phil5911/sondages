from django.contrib import admin
from django.urls import path

from sondages import views

app_name = "sondage"
urlpatterns = [
    path('index/', views.index, name="index"),
    path('<int:question_id>', views.detail, name="detail"),
    path('<int:question_id>/results/', views.results, name="results"),
    path('<int:question_id>/vote/', views.vote, name="vote")
]
