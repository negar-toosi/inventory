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
