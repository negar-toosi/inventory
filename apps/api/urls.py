from django.urls import include, path

urlpatterns = [
    path("product/", include(("apps.product.urls", "product"))),
]
