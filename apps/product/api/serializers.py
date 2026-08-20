from rest_framework import serializers

class AddProductRequest(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.IntegerField(min_value=0)

class AddProductResponse(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    current_inventory = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    