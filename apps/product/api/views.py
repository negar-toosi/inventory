from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from drf_spectacular.utils import extend_schema
from apps.product.api.serializers import (
    AddProductRequest,
    ProductSerializer,
    InventoryTransactionRequest,
)
from apps.core.custom_response import CustomResponse
from apps.product.services import ProductServices, InventoryTransactionServices
from uuid import UUID


class ProductAPI(APIView):
    @extend_schema(request=AddProductRequest, responses={201: ProductSerializer})
    def post(self, request: Request) -> CustomResponse:
        serializer = AddProductRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        product = ProductServices.add(**validated_data)

        response = ProductSerializer(product)

        return CustomResponse(
            message="Product Created Successfully",
            data=response.data,
            status_code=status.HTTP_201_CREATED,
        )


class InventoryTransactionAPI(APIView):
    @extend_schema(request=InventoryTransactionRequest, responses=ProductSerializer)
    def post(self, request: Request, id: UUID) -> CustomResponse:
        serializer = InventoryTransactionRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        new_product = InventoryTransactionServices.add(product_id=id, **validated_data)

        response = ProductSerializer(new_product)

        return CustomResponse(
            message="Product Updated Successfully",
            data=response.data,
            status_code=status.HTTP_200_OK,
        )
