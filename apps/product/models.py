import uuid

from django.db import models
from apps.product.enums import InventoryTransactionType


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    current_inventory = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=models.Q(is_deleted=False),
                name="unique_active_product_name",
            ),
        ]
    def __str__(self):
        return f"{self.name},{self.is_deleted}"

class InventoryTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="inventory_transaction"
    )
    quantity = models.PositiveIntegerField()
    previous_inventory = models.PositiveIntegerField()
    current_inventory = models.PositiveIntegerField()
    type = models.CharField(max_length=20, choices=InventoryTransactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
