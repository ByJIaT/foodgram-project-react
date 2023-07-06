from django.db import transaction
from rest_framework import serializers


class CreateUpdateNestedMixin(serializers.ModelSerializer):

    def update_or_create(self, instance, validated_data):
        reverse_relations = {}

        for field_name, field in self.fields.items():
            if isinstance(
                    field, serializers.ListSerializer
            ):
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

                except:
                    for data_dict in related_data:
                        id = data_dict.pop('id')
                        model_obj = model.objects.get(id=id)
                        m2m_manager.set(
                            [model_obj],
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
