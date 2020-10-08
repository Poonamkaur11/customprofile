from django.apps import AppConfig
from users import signals


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
