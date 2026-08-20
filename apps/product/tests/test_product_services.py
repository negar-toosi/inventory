import uuid

import pytest
from apps.core.exceptions import InventoryError
from apps.product.enums import InventoryTransactionType
from apps.product.models import InventoryTransaction, Product
from apps.product.services import ProductServices


@pytest.mark.django_db
class TestProductServices:
    @classmethod
    def setup_class(cls):
        cls.product_name = "laptop"
        cls.quantity = 10

    # ProductServices.add
    def test_add_product_with_initial_inventory(self):
        product = ProductServices.add(name=self.product_name, quantity=self.quantity)
        assert product.name == self.product_name
        assert product.current_inventory == self.quantity

        history = InventoryTransaction.objects.get(product=product)

        assert history.quantity == self.quantity
        assert history.previous_inventory == 0
        assert history.current_inventory == 0 + self.quantity
        assert history.type == InventoryTransactionType.INCREASE

    def test_add_product_with_zero_inventory(self):
        product = ProductServices.add(name=self.product_name, quantity=0)
        assert product.current_inventory == 0
        assert not InventoryTransaction.objects.filter(product=product).exists()

    def test_add_product_with_duplicate_name(self):
        Product.objects.create(name=self.product_name, current_inventory=self.quantity)
        with pytest.raises(InventoryError):
            ProductServices.add(name=self.product_name, quantity=5)
            assert (
                Product.objects.filter(name=self.product_name, is_deleted=False).count()
                == 1
            )

    def test_add_product_with_same_name_after_soft_delete(self):
        product = Product.objects.create(
            name=self.product_name, current_inventory=self.quantity, is_deleted=True
        )

        new_product = ProductServices.add(name=self.product_name, quantity=5)
        assert new_product.name == self.product_name
        assert new_product.current_inventory == 5
        assert new_product.id != product.id

    # ProductServices.get
    def test_get_existing_product(self):
        product = Product.objects.create(
            name=self.product_name, current_inventory=self.quantity
        )
        result = ProductServices.get(product.id)

        assert result.id == product.id
        assert result.name == product.name
        assert result.current_inventory == product.current_inventory

    def test_get_non_existing_product(self):
        product_id = uuid.uuid4()
        with pytest.raises(InventoryError):
            ProductServices.get(product_id)

    def test_get_soft_deleted_product(self):
        product = Product.objects.create(
            name=self.product_name, current_inventory=self.quantity, is_deleted=True
        )
        with pytest.raises(InventoryError):
            ProductServices.get(product.id)
