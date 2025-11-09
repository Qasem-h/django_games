from . import fields, serializer_fields
from rest_framework import serializers


class GameFieldMixin:
    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = super().build_standard_field(
            field_name, model_field
        )
        if (
            # Only deal with GameFields.
            not isinstance(model_field, fields.GameField)
            # Some other mixin has changed the field class already!
            or field_class is not serializers.ChoiceField
        ):
            return field_class, field_kwargs
        field_kwargs["games"] = model_field.games
        del field_kwargs["choices"]
        if not model_field.multiple:
            field_class = serializer_fields.GameField
        else:
            field_class = serializers.ListField
            child_field = serializer_fields.GameField(**field_kwargs)
            field_kwargs = {"child": child_field}
            if "max_length" in serializers.ListField.default_error_messages:
                # Added in DRF 3.5.4
                field_kwargs["max_length"] = len(child_field.games)
        return field_class, field_kwargs
