from functools import partial

from django.db.models.signals import pre_save, post_save, post_delete
from modeltranslation.translator import translator
from modeltranslation.utils import get_translation_fields

from .lokalise_client import create_or_update_translations, delete_translations


def register_translation(model_class, trans_opts_class):
    """
    This function registers model_class as a translatable model into
    django-modeltranslation using trans_opts_class as
    modelstranslation.TranslationOptions class.

    Also, it connects pre_save, post_save and post_delete signals to the
    model in order to attend this events and proper update translations on
    lokalise.
    :param model_class: The class to be registered as translatable.
    :param trans_opts_class: modelstranslation.TranslationOptions class
    containing translatable fields.
    """
    translator.register(model_class, trans_opts_class)

    pre_save.connect(
        partial(note_down_translatable_fields,
                trans_opts_class=trans_opts_class),
        sender=model_class,
        weak=False,
    )
    post_save.connect(partial(notify_changes_lokalise,
                              trans_opts_class=trans_opts_class),
                      sender=model_class,
                      weak=False)
    post_delete.connect(partial(remove_lokalise_keys,
                                trans_opts_class=trans_opts_class),
                        sender=model_class,
                        weak=False)


def note_down_translatable_fields(sender, instance, **kwargs):
    """
    Note down the translatable fields that have been modified on the
    updated_trans_fields field of the instance being saved.
    :param sender: the instance's model class.
    :param instance: object being saved.
    :param kwargs: keyword arguments, including trans_opts_class key that
    contains the modeltranslation.TranslationOptions which contains the
    translatable fields of the model.
    """
    instance.updated_trans_fields = []
    translatable_fields = kwargs.get('trans_opts_class').fields
    try:
        db_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        instance.updated_trans_fields = translatable_fields
        return

    for parent_field in translatable_fields:
        trans_fields = get_translation_fields(parent_field)
        for field in trans_fields:
            if getattr(db_instance, field) != getattr(instance, field):
                instance.updated_trans_fields.append(parent_field)
                break


def notify_changes_lokalise(**kwargs):
    """
    Notify modeltranslation_lokalise about changes on translatable models:
    (e.g. create keys for new translatable fields, update values for
    existent keys, etc.)
    """
    instance = kwargs['instance']
    if len(instance.updated_trans_fields) == 0:
        # Instance has no translatable fields modified
        return

    create_or_update_translations(
        list(kwargs.get('trans_opts_class').fields),
        instance,
    )


def remove_lokalise_keys(**kwargs):
    """
    Remove all keys on lokalise for a given instance.
    :param sender: the instance's model class.
    :param instance: object being saved.
    """
    delete_translations(kwargs['instance'])
