from django.db import models


class InventoryTransactionType(models.TextChoices):
    INCREASE = "increase", "Increase"
    DECREASE = "decrease", "Decrease"
