from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    def ready(self):
            from . import classUpdater_update
            classUpdater_update.start()
