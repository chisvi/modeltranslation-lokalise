# Django modeltranslation-lokalise

Integrate [django-modeltranslation](https://github.com/deschler/django-modeltranslation) with [lokalise.co](https://lokalise.co).
It will let your project upload translatable fields of your model into lokalise.io using it's [API](https://lokalise.co/api2docs/python/) and
also update your local translations when someone updates them on lokalise. 

### Installing

```
pip install modeltranslation-lokalise
```

`modeltranslation_lokalise` depends on Django's [contribtypes](https://docs.djangoproject.com/es/2.2/ref/contrib/contenttypes/) application, 
so make sure you include it in your `INSTALLED_APPS` setting before `modeltranslation_lokalise`:

```python
INSTALLED_APPS = [
    '...',
    'django.contrib.contenttypes',
    '...',
    'modeltranslation_lokalise',
    '...',
]
```

You need to provide your lokalise proyect id and your api key in order to let `modeltranslation_lokalise` properly update
your translations.

```python
LOKALISE_API_KEY = ''
LOKALISE_PROJECT_ID = ''
```

If you want to get your models updated automatically when someone updates them on lokalise, enable it by adding the view to
your `urls.py` conf. Note that currently only `translation.updated` is supported:

```python
from modeltranslation_lokalise import TranslationWebhookView

urlpatterns = [
    ...
    path('api/translations/', TranslationWebhookView.as_view(), name='translation_webhook'),
    ...
]
```

You also need to make migrations in order to create the necessary tables on your database to handle the translations:

```
python manage.py makemigrations
python manage.py migrate
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
