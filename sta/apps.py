from django.apps import AppConfig


class StaConfig(AppConfig):
    name = 'sta'

    def ready(self):
        import sta.signals  # ← Django charge le signal au démarrage