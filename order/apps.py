from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'

    def ready(self) -> None:
        from jobs.sched import start
        start()
        return super().ready()
