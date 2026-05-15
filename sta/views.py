import json

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .services import ollama
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


class HomeView(ListView):
    model = Entry
    template_name = 'accueil.html'
    context_object_name = 'home' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home'] = Entry.objects.all().order_by('-date_creation')[:3]
        return context
    


# ─── LIST ─────────────────────────────────────────────────
class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'entry_list.html'
    context_object_name = 'entries'
    paginate_by = 6 


    def get_queryset(self):
        # Chaque user voit tous les logs
        queryset = Entry.objects.all().order_by('-date_creation')

        # Filtre catégorie si présent dans l'URL
        categorie = self.request.GET.get('categorie')
        if categorie:
            queryset = queryset.filter(categorie__nom=categorie)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # On envoie les catégories pour afficher les boutons
        context['categories'] = Category.objects.all()
        # On garde la catégorie active pour highlight le bouton
        context['categorie_active'] = self.request.GET.get('categorie', '')
        return context


# ─── DETAIL ───────────────────────────────────────────────
class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'entry_detail.html'
    context_object_name = 'entry'


# ─── CREATE ───────────────────────────────────────────────
class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'entry_form.html'
    fields = ['titre', 'contenu', 'categorie', 'image_preuve']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # L'auteur = utilisateur connecté (automatique)
        form.instance.auteur = self.request.user
        return super().form_valid(form)


# ─── UPDATE ───────────────────────────────────────────────
class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    template_name = 'entry_form.html'
    fields = ['titre', 'contenu', 'categorie', 'image_preuve']
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        # Seul l'auteur peut modifier
        entry = self.get_object()
        return self.request.user == entry.auteur


# ─── DELETE ───────────────────────────────────────────────
class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = 'entry_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        # Seul l'auteur peut supprimer
        entry = self.get_object()
        return self.request.user == entry.auteur



# ─── CHATBOT ─────────────────────────────────────────────
def construire_contexte_logs(user):
    """Transforme les logs en texte pour l'IA"""
    logs = Entry.objects.filter(
        auteur=user
    ).select_related('categorie').order_by('-date_creation')[:20]

    if not logs:
        return "Aucun log disponible pour cet utilisateur."

    texte = f"L'utilisateur {user.username} a {logs.count()} logs :\n\n"

    for log in logs:
        texte += (
            f"[{log.date_creation.strftime('%d/%m/%Y %H:%M')}] "
            f"{log.categorie.nom if log.categorie else 'Non classé'} — "
            f"{log.titre} : {log.contenu}\n"
        )
    return texte


class ChatbotView(LoginRequiredMixin, View):

    def get(self, request):
        if 'historique' not in request.session:
            request.session['historique'] = []
        return render(request, 'chat.html', {
            'historique': request.session['historique']
        })

    def post(self, request):
        message = request.POST.get('message', '').strip()

        if not message:
            return redirect('chatbot')

        # Récupérer l'historique depuis la session
        historique = request.session.get('historique', [])

        # Contexte logs
        contexte = construire_contexte_logs(request.user)

        # Appel Ollama
        reponse = ollama.envoyer_message(
            message_utilisateur=message,
            contexte_logs=contexte,
            historique_messages=historique
        )

        # Ajouter à l'historique
        historique.append({'role': 'user',      'content': message})
        historique.append({'role': 'assistant', 'content': reponse})

        # Sauvegarder en session
        request.session['historique'] = historique
        request.session.modified = True

        return redirect('chatbot')
    
    
    