from django.urls import include, path

urlpatterns = [
    path("product/", include(("apps.product.urls", "product"))),
    path("api/", include(("apps.api.urls", "api"))),
]