from django.db import models


class ProductTransactionStatus(models.TextChoices):
    INCREASE = "increase", "Increase"
    DECREASE = "decrease", "Decrease"
