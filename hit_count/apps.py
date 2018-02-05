from django.apps import AppConfig


class HitConfig(AppConfig):
    name = 'hit_count'

    def ready(self):
        import hit_count.signals
