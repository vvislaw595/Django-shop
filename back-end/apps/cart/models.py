from django.db import models


class Cart(models.Model):
    sku_id = models.CharField(null=False, max_length=255, unique=True)
    email = models.CharField(max_length=255)
    nums = models.IntegerField()
    is_delete = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'shopping_cart'

