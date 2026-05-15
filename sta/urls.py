from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentification
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('', views.HomeView.as_view(), name='accueil'),
    # CRUD
    path('entry/', views.EntryListView.as_view(), name='dashboard'),
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='entry-detail'),
    path('entry/create/', views.EntryCreateView.as_view(), name='entry-create'),
    path('entry/<int:pk>/update/', views.EntryUpdateView.as_view(), name='entry-update'),
    path('entry/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry-delete'),

    # API pour l'IA
    path('chatbot/', views.ChatbotView.as_view(), name='chatbot'),
]

