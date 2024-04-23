from django.core.exceptions import FieldDoesNotExist
from rest_framework import serializers

# from gateway.models import Subject


class DynamicModelSerializer(serializers.ModelSerializer):
    # Usage: DynamicModelSerializer(model=ModelNameHere)
    def __init__(self, *args, **kwargs):
        self.Meta.model = kwargs.pop("model", None)
        if not self.Meta.model:
            raise ValueError(
                "Invalid usage of DynamicModelSerializer, must have kwarg 'model'"
            )
        super(DynamicModelSerializer, self).__init__(*args, **kwargs)

    class Meta:
        fields = "__all__"

    # @classmethod
    # def get_classes(self, model):
    #     if model == Subject:
    #         choices = self.objects.all().select_related("classsubject_set")
    #         return choices
    #     raise FieldDoesNotExist("Only the Subject model is allowed to use this method.")
