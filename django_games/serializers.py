from typing import Any, Dict, Tuple, Type

from rest_framework import serializers

from . import fields, serializer_fields


class GameFieldMixin:
    """
    Automatically maps Django model GameField to DRF serializer GameField.

    Example:
        from django_games.fields import GameField

        class Character(models.Model):
            game = GameField()

        class CharacterSerializer(GameFieldMixin, serializers.ModelSerializer):
            class Meta:
                model = Character
                fields = ["id", "name", "game"]
    """

    def build_standard_field(
        self, field_name: str, model_field: Any
    ) -> Tuple[Type[serializers.Field], Dict[str, Any]]:
        # Get the default DRF field class and kwargs
        field_class, field_kwargs = super().build_standard_field(field_name, model_field)  # type: ignore

        # Only act on our custom GameField, and if DRF still sees it as a ChoiceField
        if not isinstance(model_field, fields.GameField) or field_class is not serializers.ChoiceField:
            return field_class, field_kwargs

        # Replace DRF's choices with our game registry
        field_kwargs["games"] = model_field.games
        field_kwargs.pop("choices", None)

        # Single-selection GameField → use custom serializer
        if not getattr(model_field, "multiple", False):
            field_class = serializer_fields.GameField
        else:
            # Multi-selection → ListField of GameFields
            child_field = serializer_fields.GameField(**field_kwargs)
            field_class = serializers.ListField
            field_kwargs = {"child": child_field}

            # Optional safeguard for DRF versions supporting max_length in ListField
            if hasattr(serializers.ListField, "default_error_messages"):
                field_kwargs["max_length"] = len(child_field.games)

        return field_class, field_kwargs
