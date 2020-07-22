from modeltranslation.utils import get_translation_fields
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import LokaliseTranslation
from .permissions import WhitelistIPPermission, LokalisePermission
from .serializers import TranslationUpdateSerializer


class TranslationWebhookView(GenericAPIView):
    http_method_names = ['post']
    serializer_class = TranslationUpdateSerializer
    permission_classes = (WhitelistIPPermission, LokalisePermission)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        if request.data == ['ping']:
            return Response(status=HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.update_translation(serializer.data):
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    def update_translation(self, data):
        lang_code = data['language']['iso']
        translation_key = data['key']['id']
        translation = data['translation']['value']

        try:
            t_obj = LokaliseTranslation.objects.get(
                key_id=translation_key,
            )
        except LokaliseTranslation.DoesNotExist():
            return False

        translated_obj = t_obj.content_object
        translated_field = t_obj.field_name
        obj_translatable_fields = get_translation_fields(translated_field)
        field_lang = next((f for f in obj_translatable_fields if
                           f.endswith(lang_code)), None)
        if field_lang is None:
            return False

        setattr(translated_obj, field_lang, translation)
        translated_obj.save()

        return True
