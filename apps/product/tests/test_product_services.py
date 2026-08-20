import uuid

import pytest
from apps.core.exceptions import InventoryError
from apps.product.enums import InventoryTransactionType
from apps.product.models import InventoryTransaction, Product
from apps.product.services import InventoryTransactionServices, ProductServices


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


@pytest.mark.django_db
class TestInventoryTransactionServices:
    @classmethod
    @pytest.fixture(autouse=True)
    def setup_class(cls):
        cls.product_name = "laptop"
        cls.quantity = 10

        cls.product = Product.objects.create(
            name=cls.product_name, current_inventory=cls.quantity
        )

    def test_increase_inventory(self):
        result = InventoryTransactionServices.add(
            product_id=self.product.id,
            quantity=5,
            type=InventoryTransactionType.INCREASE,
        )
        self.product.refresh_from_db()
        assert result.id == self.product.id
        assert self.product.current_inventory == 15

    def test_increase_inventory_creates_history(self):
        InventoryTransactionServices.add(
            product_id=self.product.id,
            quantity=5,
            type=InventoryTransactionType.INCREASE,
        )
        history = InventoryTransaction.objects.get(product=self.product)
        assert history.quantity == 5
        assert history.previous_inventory == 10
        assert history.current_inventory == 15
        assert history.type == InventoryTransactionType.INCREASE

    def test_decrease_inventory(self):
        result = InventoryTransactionServices.add(
            product_id=self.product.id,
            quantity=3,
            type=InventoryTransactionType.DECREASE,
        )
        self.product.refresh_from_db()
        assert result.id == self.product.id
        assert self.product.current_inventory == 7

    def test_decrease_inventory_creates_history(self):
        InventoryTransactionServices.add(
            product_id=self.product.id,
            quantity=3,
            type=InventoryTransactionType.DECREASE,
        )
        history = InventoryTransaction.objects.get(product=self.product)
        assert history.quantity == 3
        assert history.previous_inventory == 10
        assert history.current_inventory == 7
        assert history.type == InventoryTransactionType.DECREASE

    def test_decrease_inventory_to_zero(self):
        InventoryTransactionServices.add(
            product_id=self.product.id,
            quantity=self.quantity,
            type=InventoryTransactionType.DECREASE,
        )
        self.product.refresh_from_db()
        assert self.product.current_inventory == 0

    def test_cannot_decrease_inventory_below_zero(self):
        with pytest.raises(InventoryError):
            InventoryTransactionServices.add(
                product_id=self.product.id,
                quantity=11,
                type=InventoryTransactionType.DECREASE,
            )
            self.product.refresh_from_db()
            assert self.product.current_inventory == 10

    def test_failed_decrease_does_not_create_history(self):
        with pytest.raises(InventoryError):
            InventoryTransactionServices.add(
                product_id=self.product.id,
                quantity=11,
                type=InventoryTransactionType.DECREASE,
            )
            assert not InventoryTransaction.objects.filter(
                product=self.product
            ).exists()

    def test_inventory_history(self):

        InventoryTransactionServices.add(
            self.product.id,
            5,
            InventoryTransactionType.INCREASE,
        )
        InventoryTransactionServices.add(
            self.product.id,
            3,
            InventoryTransactionType.DECREASE,
        )
        InventoryTransactionServices.add(
            self.product.id,
            7,
            InventoryTransactionType.INCREASE,
        )
        self.product.refresh_from_db()
        assert self.product.current_inventory == 19
        assert InventoryTransaction.objects.filter(product=self.product).count() == 3

    def test_history_contains_correct_snapshots(self):
        InventoryTransactionServices.add(
            self.product.id,
            5,
            InventoryTransactionType.INCREASE,
        )
        InventoryTransactionServices.add(
            self.product.id,
            3,
            InventoryTransactionType.DECREASE,
        )

        history = list(InventoryTransactionServices.get(self.product))
        assert history[0].previous_inventory == 15
        assert history[0].current_inventory == 12
        assert history[1].previous_inventory == 10
        assert history[1].current_inventory == 15

    def test_history_is_ordered_by_created_at_descending(self):
        first = InventoryTransaction.objects.create(
            product=self.product,
            quantity=5,
            previous_inventory=10,
            current_inventory=15,
            type=InventoryTransactionType.INCREASE,
        )
        second = InventoryTransaction.objects.create(
            product=self.product,
            quantity=3,
            previous_inventory=15,
            current_inventory=12,
            type=InventoryTransactionType.DECREASE,
        )
        history = list(InventoryTransactionServices.get(self.product))

        assert history[0].id == second.id
        assert history[1].id == first.id

    def test_history_does_not_return_transactions_from_other_products(self):
        product1 = Product.objects.create(
            name="glasses",
            current_inventory=10,
        )
        product2 = Product.objects.create(
            name="phone",
            current_inventory=20,
        )
        InventoryTransactionServices.add(
            product1.id,
            5,
            InventoryTransactionType.INCREASE,
        )
        InventoryTransactionServices.add(
            product2.id,
            7,
            InventoryTransactionType.INCREASE,
        )
        history = InventoryTransactionServices.get(product1)
        assert history.count() == 1
        assert history.first().product_id == product1.id

    def test_zero_quantity_should_be_rejected(self):
        with pytest.raises(InventoryError):
            InventoryTransactionServices.add(
                self.product.id,
                0,
                InventoryTransactionType.INCREASE,
            )

    def test_negative_quantity_should_be_rejected(self):
        with pytest.raises(InventoryError):
            InventoryTransactionServices.add(
                self.product.id,
                -5,
                InventoryTransactionType.INCREASE,
            )

    def test_inventory_transaction_for_non_existing_product(self):
        product_id = uuid.uuid4()
        with pytest.raises(InventoryError):
            InventoryTransactionServices.add(
                product_id,
                5,
                InventoryTransactionType.INCREASE,
            )

    def test_cannot_change_inventory_of_deleted_product(self):
        self.product.is_deleted = True
        self.product.save()
        with pytest.raises(InventoryError):
            InventoryTransactionServices.add(
                self.product.id,
                5,
                InventoryTransactionType.INCREASE,
            )
            self.product.refresh_from_db()
            assert self.product.current_inventory == 10

    def test_failed_transaction_does_not_change_product_or_history(self):

        history_before = InventoryTransaction.objects.filter(
            product=self.product
        ).count()
        with pytest.raises(InventoryError):
            InventoryTransactionServices.add(
                self.product.id,
                11,
                InventoryTransactionType.DECREASE,
            )
            self.product.refresh_from_db()
            assert self.product.current_inventory == 10
            history_after = InventoryTransaction.objects.filter(
                product=self.product
            ).count()
            assert history_after == history_before

    def test_complete_inventory_lifecycle(self):
        product = ProductServices.add(
            name="glasses",
            quantity=100,
        )
        InventoryTransactionServices.add(
            product.id,
            50,
            InventoryTransactionType.INCREASE,
        )
        InventoryTransactionServices.add(
            product.id,
            30,
            InventoryTransactionType.DECREASE,
        )
        InventoryTransactionServices.add(
            product.id,
            20,
            InventoryTransactionType.INCREASE,
        )
        product.refresh_from_db()
        assert product.current_inventory == 140
        history = InventoryTransactionServices.get(product)
        assert history.count() == 4
