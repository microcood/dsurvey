from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from .utils import get_questions_from_file
from .models import Test


@receiver(post_init, sender=Test)
def test_post_init(sender, instance, **kwargs):
    # Signals in replacement for django-dirtyfields += 1
    instance._doc_file = instance.file


@receiver(post_save, sender=Test)
def test_pre_save(sender, instance, **kwargs):
    if instance.file and instance.file != instance._doc_file:
        get_questions_from_file(instance)
