from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from apps.product.api.serializers import (
    AddProductRequest,
    ProductSerializer,
    InventoryTransactionRequest,
    TransactionSerializer,
)
from apps.core.custom_response import CustomResponse
from apps.product.services import ProductServices, InventoryTransactionServices
from apps.product.schema import (
    AddProductSchema,
    ChangeProductInventorySchema,
    GetProductTransactionHistory,
)
from apps.core.pagination import get_paginated_response
from uuid import UUID


class ProductAPI(APIView):
    @extend_schema(
        description="Add new product.",
        request=AddProductSchema,
        responses={201: ProductSerializer},
    )
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
    @extend_schema(
        description="change product inventory.",
        request=ChangeProductInventorySchema,
        responses=ProductSerializer,
    )
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

    @extend_schema(
        description="Get product transactions history.",
        parameters=GetProductTransactionHistory,
        responses={200: TransactionSerializer},
    )
    def get(self, request: Request, id: UUID) -> Response:
        product = ProductServices.get(id=id)
        transactions = InventoryTransactionServices.get(product=product)

        return get_paginated_response(
            message="Inventory transactions retrieved successfully.",
            serializer_class=TransactionSerializer,
            queryset=transactions,
            request=request,
            view=self,
        )
