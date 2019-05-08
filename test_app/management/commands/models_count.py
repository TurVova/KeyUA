from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Displays model name and number of entries'

    def handle(self, *args, **kwargs):
        models = ContentType.objects.filter(app_label__in=settings.LOCAL_APPS)
        for model in models:
            model_count = model.get_all_objects_for_this_type().count()
            model_name = model.model_class().__name__
            print(f'There are {model_count} entries in the {model_name} model')

