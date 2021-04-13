from django.apps import AppConfig


class LogParserConfig(AppConfig):
    # BigAutoField = вручную без миграции
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LogParser'
