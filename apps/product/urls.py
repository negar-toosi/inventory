from django.urls import path

from apps.product.api.views import AddProductAPI

urlpatterns = [
    path("add/", AddProductAPI.as_view(), name="add-new-product"),
]
