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
    ...
    'django.contrib.contenttypes',
    ...
    'modeltranslation_lokalise',
    ...
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

### How to use

Instead of using modeltranslation `translator.register`, you should use `modeltranslation_lokalise.register_translation`:

```python
from modeltranslation.translator import TranslationOptions
from modeltranslation_lokalise.signals import register_translation

from your_app.models import Model1


class Model1TranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


register_translation(Model1, Model1TranslationOptions)
```

And that's all, `modeltranslations-lokalise` will keep track of changes on your translatable models and import them in your
lokalise project each time you update one of your translatable fields.


#### Non-lokalise translatable fields

It's possible that you want certain fields to be translatable in terms of modeltranslations but exclude them from being 
uploaded to Lokalise. In that case you can add an attribute `non_lokalise_fields` to your TranslationOptions object. 
Modeltranslation-lokalise will not track changes on that fields.

```python
class ProductTranslationOptions(TranslationOptions):
    non_lokalise_fields = ('slug', )
    fields = ('title', 'description', ) + non_lokalise_fields
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
