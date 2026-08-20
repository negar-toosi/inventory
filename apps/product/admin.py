from django.contrib import admin
from apps.product.models import Product, InventoryTransaction


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "current_inventory",
        "is_deleted",
    )


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "quantity",
        "current_inventory",
        "type",
    )
