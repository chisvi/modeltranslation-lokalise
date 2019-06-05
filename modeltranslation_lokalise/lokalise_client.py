import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from modeltranslation.utils import get_translation_fields

from .models import LokaliseTranslation

CREATE_KEYS_URL = 'https://api.lokalise.co/api2/projects/{project_id}/keys'
UPDATE_KEYS_URL = 'https://api.lokalise.co/api2/projects/{project_id}/keys'
DELETE_KEYS_URL = 'https://api.lokalise.co/api2/projects/{project_id}/keys'
AUTH_HEADER_NAME = 'x-api-token'


def create_or_update_translations(fields_l, obj_instance):
    """
    This function takes a list of translatable fields and an object instance
    and checks if there are uploaded translations for that fields and then
    it creates or updates them.
    :param fields_l: list of field names to upload translations for.
    :param obj_instance: instance of the objects the translations belong to.
    """
    fields_key_map = {}
    platforms = ['web']

    if len(fields_l) == 0:
        return

    operations = {'create': [], 'update': []}

    for field in fields_l:
        key_name = f'{obj_instance.__class__.__name__}_' \
            f'{obj_instance.pk}_{field}'
        fields_key_map[key_name] = field
        t_fields = get_translation_fields(field)
        translations = [
            {'language_iso': f[-2:],
             'translation': getattr(obj_instance, f) or ''} for f in t_fields
        ]
        trans = {'key_name': key_name,
                 'platforms': platforms,
                 'translations': translations}

        try:
            content_type = ContentType.objects.get_for_model(
                obj_instance.__class__
            )
            trans['key_id'] = LokaliseTranslation.objects.get(
                content_type=content_type,
                object_id=obj_instance.pk,
                field_name=field
            ).key_id
            operations['update'].append(trans)

        except LokaliseTranslation.DoesNotExist:
            operations['create'].append(trans)

    update_translations(operations['update'], 'update')
    new_trans = update_translations(operations['create'], 'create')

    # We must create a LokaliseTranslation row for every created translation
    for k in new_trans['keys']:
        LokaliseTranslation.objects.create(
            key_id=k['key_id'],
            field_name=fields_key_map[k['key_name'][platforms[0]]],
            content_object=obj_instance,
        )


def update_translations(translations, operation):
    """
    Send updates to lokalise api.
    :param translations: list of translation dicts, as passed to lokalise api.
    :param operation: type of operation to perform. Valid values are
    'create' or 'update'
    """
    headers = {AUTH_HEADER_NAME: settings.LOKALISE_API_KEY}
    result = {'keys': [], 'errors': []}

    if not translations:
        return result

    if operation == 'update':
        url = UPDATE_KEYS_URL.format(project_id=settings.LOKALISE_PROJECT_ID)
        method = 'put'
    elif operation == 'create':
        method = 'post'
        url = CREATE_KEYS_URL.format(project_id=settings.LOKALISE_PROJECT_ID)
    else:
        raise ValueError(f'Invalid operation to perform: {operation}')

    try:
        r = requests.request(method, url,
                             json={'keys': translations},
                             headers=headers)
        r.raise_for_status()
        result = r.json()

    except requests.HTTPError:
        # TODO: unsuccessful request, what to do? Slack?
        pass
    except requests.RequestException:
        # TODO: error occurred (timeout, DNS error?) what to do? Slack?
        pass

    return result


def delete_translations(obj_instance):
    """
    Given an instance, delete all it's translations both on lokalise and on
    local database.
    :param obj_instance: instance object.
    """
    headers = {AUTH_HEADER_NAME: settings.LOKALISE_API_KEY}
    url = DELETE_KEYS_URL.format(project_id=settings.LOKALISE_PROJECT_ID)

    content_type = ContentType.objects.get_for_model(
        obj_instance.__class__
    )
    trans = LokaliseTranslation.objects.filter(
        content_type=content_type,
        object_id=obj_instance.pk,
    )
    if not trans:
        return

    payload = {'keys': [t.key_id for t in trans]}
    try:
        r = requests.delete(url, json=payload, headers=headers)
        r.raise_for_status()

    except requests.HTTPError:
        # TODO: unsuccessful request, what to do? Slack?
        pass
    except requests.RequestException:
        # TODO: error occurred (timeout, DNS error?) what to do? Slack?
        pass
