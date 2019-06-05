from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import LokaliseTranslation


class TranslationProjectSerializer(serializers.Serializer):
    id = serializers.ChoiceField(required=True,
                                 choices=[settings.LOKALISE_PROJECT_ID])
    name = serializers.CharField()


class TranslationKeySerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    key = serializers.CharField(required=True)

    def validate_id(self, value):
        try:
            LokaliseTranslation.objects.get(key_id=value)
        except:
            raise serializers.ValidationError(
                _("Translation with key_id = {trans_key_id} does not "
                  "exist").format(trans_key_id=value)
            )
        return value


class TranslationLangSerializer(serializers.Serializer):
    name = serializers.CharField()
    iso = serializers.ChoiceField(choices=[l[0] for l in settings.LANGUAGES],
                                  required=True)


class TranslationDataSerializer(serializers.Serializer):
    translation = serializers.CharField(required=True)
    lang = TranslationLangSerializer(required=True)
    key = TranslationKeySerializer(required=True)
    project = TranslationProjectSerializer(required=True)


class TranslationUpdateSerializer(serializers.Serializer):
    event = serializers.ChoiceField(choices=['translation.updated'],
                                    required=True)
    data = TranslationDataSerializer(required=True)
