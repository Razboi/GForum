from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Forum


class ForumList(ListView):

    def get_queryset(self, **kwargs):
        return Forum.objects.all()
