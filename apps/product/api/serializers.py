from rest_framework import serializers
from apps.product.enums import InventoryTransactionType


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    current_inventory = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class TransactionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    previous_inventory = serializers.IntegerField()
    current_inventory = serializers.IntegerField()
    type = serializers.CharField()
    created_at = serializers.DateTimeField()


class AddProductRequest(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    quantity = serializers.IntegerField(min_value=0)

    def validate_name(self, value):
        if not isinstance(self.initial_data.get("name"), str):
            raise serializers.ValidationError("name must be a string.")
        return value


class InventoryTransactionRequest(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    type = serializers.ChoiceField(choices=InventoryTransactionType.choices)
