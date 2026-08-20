import uuid

from django.db import models
from apps.product.enums import InventoryTransactionType


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True)
    current_inventory = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InventoryTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="inventory_transaction"
    )
    quantity = models.PositiveIntegerField()
    previous_inventory = models.PositiveIntegerField()
    current_inventory = models.PositiveIntegerField()
    type = models.CharField(max_length=20, choices=InventoryTransactionType.choices)
