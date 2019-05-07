from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from test_app.models import ChangeInModel


@receiver([post_save, post_delete])
def save_or_update_signal(sender, **kwargs):
    models = ContentType.objects.filter(app_label__in=settings.LOCAL_APPS).exclude(model='changeinmodel')
    for model in models:
        print('awdad', model.model)
        if sender == model.model_class():
            obj = ChangeInModel()
            obj.app_label = model.app_label
            obj.model_name = sender.__name__
            if kwargs['created']:
                obj.action = 'created'
                print(f'{sender.__name__} created')
            elif not kwargs['created']:
                obj.action = 'updated'
                print(f'{sender.__name__} updated')
            else:
                obj.action = 'deleted'
                print(f'{sender.__name__} deleted')
            obj.save()