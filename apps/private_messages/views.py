from django.shortcuts import render
from .models import PrivateMessage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class PMList(ListView):

    def get_queryset(self):
        return PrivateMessage.objects.filter(contact=self.request.user)
