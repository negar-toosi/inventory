import uuid

from drf_spectacular.utils import OpenApiRequest, OpenApiParameter

AddProductSchema = OpenApiRequest(
    request={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "example": "iPhone 15",
            },
            "quantity": {
                "type": "integer",
                "minimum": 0,
                "example": 10,
            },
        },
        "required": ["name", "quantity"],
    },
)

ChangeProductInventorySchema = OpenApiRequest(
    request={
        "type": "object",
        "properties": {
            "quantity": {
                "type": "integer",
                "minimum": 0,
                "example": 10,
            },
            "type": {
                "type": "string",
                "example": "increase",
                "description": "The transaction type must be either increase or decrease.",
            },
        },
        "required": ["quantity", "type"],
    },
)

GetProductTransactionHistory = [
    OpenApiParameter(
        "page",
        int,
        OpenApiParameter.QUERY,
        description="Page number.",
    )
]
