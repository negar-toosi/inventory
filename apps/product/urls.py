from django.urls import path

from apps.product.api.views import ProductAPI, InventoryTransactionAPI

urlpatterns = [
    path("add/", ProductAPI.as_view(), name="add-new-product"),
    path(
        "<uuid:id>/inventory/transactions/",
        InventoryTransactionAPI.as_view(),
        name="inventory-transaction",
    ),
]
