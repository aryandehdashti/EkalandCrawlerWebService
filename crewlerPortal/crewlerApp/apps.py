from django.apps import AppConfig


class CrewlerappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crewlerApp'

    def ready(self):
        import getProducts
        getProducts.start()
