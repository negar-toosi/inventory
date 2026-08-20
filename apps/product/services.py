from uuid import UUID

from apps.product.models import Product, InventoryTransaction
from apps.product.enums import InventoryTransactionType
from apps.core.exceptions import InventoryError

from django.db import IntegrityError, transaction
import logging

logger = logging.getLogger(__name__)


class ProductServices:
    @staticmethod
    def add(name: str, quantity: int) -> Product:
        try:
            with transaction.atomic():
                product = Product.objects.create(
                    name=name,
                    current_inventory=quantity,
                )
                if quantity != 0:
                    InventoryTransaction.objects.create(
                        product=product,
                        quantity=quantity,
                        previous_inventory=0,
                        current_inventory=quantity,
                        type=InventoryTransactionType.INCREASE,
                    )
            return product
        except IntegrityError:
            logger.exception("A product with this name already exists.")
            raise InventoryError.bad_request("A product with this name already exists.")

    @staticmethod
    def get(id: UUID):
        try:
            return Product.objects.get(id=id, is_deleted=False)
        except Product.DoesNotExist:
            logger.exception("The product does not exist.")
            raise InventoryError.bad_request(
                message="The product does not exist.",
                extra={"id": str(id)},
            )


class InventoryTransactionServices:
    @classmethod
    @transaction.atomic
    def add(
        cls, product_id: UUID, quantity: int, type: InventoryTransactionType
    ) -> Product:
        if quantity <= 0:
            raise InventoryError.bad_request(
                message="Quantity must be greater than zero."
            )
        product = cls.get_product(product_id)

        current_inventory = product.current_inventory

        if type == InventoryTransactionType.DECREASE:
            if current_inventory < quantity:
                raise InventoryError.bad_request(
                    f"Insufficient inventory. Only {current_inventory} units are available."
                )

            new_inventory = current_inventory - quantity

        else:
            new_inventory = current_inventory + quantity

        InventoryTransaction.objects.create(
            product=product,
            quantity=quantity,
            previous_inventory=current_inventory,
            current_inventory=new_inventory,
            type=type,
        )

        product.current_inventory = new_inventory
        product.save(update_fields=["current_inventory"])

        return product

    def get_product(product_id: UUID) -> Product:
        try:
            product = Product.objects.select_for_update().get(
                pk=product_id,
                is_deleted=False,
            )
            return product
        except Product.DoesNotExist:
            raise InventoryError.bad_request(
                message="The product does not exist.",
                extra={"id": str(product_id)},
            )

    def get(product: Product):
        return InventoryTransaction.objects.filter(product=product).order_by(
            "-created_at"
        )
