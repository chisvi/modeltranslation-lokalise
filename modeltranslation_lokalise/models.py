from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class LokaliseTranslation(models.Model):
    """
    Each register of this model represents a reference between a field of a
    generic model of the application and its key on modeltranslation_lokalise.
    """
    key_id = models.PositiveIntegerField(unique=True)
    field_name = models.CharField(max_length=64, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f"{self.content_object} - {self.field_name}"

    class Meta:
        unique_together = ('content_type', 'object_id', 'field_name',)
