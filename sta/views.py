from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Entry, Category


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # On sauvegarde l'utilisateur
        user = form.save()
        # On le connecte automatiquement après inscription
        login(self.request, user)
        return redirect(self.success_url)
    
    
