""" API App Apps. """
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Class representing the API application and it's configration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    verbose_name = "API"
