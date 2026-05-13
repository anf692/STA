from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Entry


@receiver(post_save, sender=Entry)
def log_entry_creation(sender, instance, created, **kwargs):
    if created:  # Uniquement à la création
        print("=" * 50)
        print("Nouveau log créé !")
        print(f"Auteur   : {instance.auteur.username}")
        print(f"Titre    : {instance.titre}")
        print(f"Catégorie: {instance.categorie}")
        print(f"Date     : {instance.date_creation}")
        print("=" * 50)

    
