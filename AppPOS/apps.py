from django.apps import AppConfig


class AppposConfig(AppConfig):
    name = 'AppPOS'

    def ready(self):
        import AppPOS.signals
