from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.response import Response


class CreateUpdateNestedMixin(serializers.ModelSerializer):
    """Принимает данные вида [1,] или [{'id': 1},]."""

    def update_or_create(self, instance, validated_data):
        reverse_relations = {}

        for field_name, field in self.fields.items():
            if isinstance(field, serializers.ListSerializer):
                if field.source in validated_data:
                    validated_data.pop(field.source)

                reverse_relations[field_name] = field

        for field_name, field in reverse_relations.items():
            model = field.child.Meta.model
            related_data = self.initial_data[field_name]

            if self.Meta.model._meta.get_field(field.source).many_to_many:
                m2m_manager = getattr(instance, field.source)
                try:
                    m2m_manager.set(model.objects.filter(
                        id__in=related_data))

                except TypeError:
                    m2m_manager.clear()
                    for data_dict in related_data:
                        if isinstance(data_dict, dict):
                            id = data_dict.pop('id')
                            model_obj = model.objects.get(id=id)
                            m2m_manager.add(
                                model_obj,
                                through_defaults=data_dict,
                            )

        return instance

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        return self.update_or_create(instance, validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return self.update_or_create(instance, validated_data)


class CreateMixin:
    def created(self, model=None, serializer=None, instance=None,
                error_message='error', **kwargs):
        if model.objects.filter(**kwargs).exists():
            return Response(
                {'errors': _(error_message)},
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.create(**kwargs)
        serializer = serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteMixin:
    def deleted(self, model=None, error_message='error', **fields):
        if not model.objects.filter(**fields).exists():
            return Response(
                {'errors': _(error_message)},
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.delete(**fields)
        return Response(status=status.HTTP_204_NO_CONTENT)
