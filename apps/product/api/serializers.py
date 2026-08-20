from rest_framework import serializers
from apps.product.enums import InventoryTransactionType

class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    current_inventory = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class AddProductRequest(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.IntegerField(min_value=0)


class InventoryTransactionRequest(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    type = serializers.ChoiceField(
        choices=InventoryTransactionType.choices
    )

