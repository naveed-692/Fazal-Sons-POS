from django.db import models


# Create your models here.


class Stock(models.Model):
    product_name = models.CharField(max_length=200, null=True)
    sku = models.CharField(max_length=200, null=True, unique=True)
    color = models.CharField(max_length=100, null=True,blank=True)
    # size = models.CharField(max_length=100, null=True, blank=True)
    avail_quantity = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_stock'

    def __str__(self):
        return self.sku

