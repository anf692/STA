from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Entry(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entrees'
    )
    categorie = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entrees'
    )
    image_preuve = models.ImageField(
        upload_to='preuves/',
        null=True,
        blank=True
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"
        ordering = ['-date_creation']


