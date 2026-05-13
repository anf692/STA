from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    nom = models.CharField(max_length=100)
    couleur = models.CharField(max_length=7, default='#6366F1')  # couleur badge

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Categories"


class Entry(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    Categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ImageField(upload_to='entries/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.auteur.username}"

    class Meta:
        ordering = ['-created_at']  # Plus récent en premier
        verbose_name_plural = "Entries"


