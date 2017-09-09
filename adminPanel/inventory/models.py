from __future__ import unicode_literals

from django.db import models
from account.models import HotelUser
from django.contrib.postgres.fields import JSONField


class BaseInventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    quantity = models.FloatField(null=True)
    units = models.CharField(max_length=100, null=True)
    rate_per_unit = models.FloatField(null=True)
    amount = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'base_inventory'

    def __unicode__(self):
        return str(self.inventory_id)


class HotelPredefinedProducts(models.Model):
    predefined_id = models.AutoField(primary_key=True)
    hotel_id = models.ForeignKey(HotelUser, to_field='hotel_id', db_column='hotel_id', on_delete=models.CASCADE)
    # hotel_name = models.ForeignKey(HotelUser, to_field='hotel_name', db_column='hotel_name', related_name="hotel",
    #                                on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=500, db_column='hotel_name')
    product_id = models.ForeignKey(BaseInventory, to_field='inventory_id', db_column='product_id', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.FloatField(null=True)
    units = models.CharField(max_length=100, null=True)
    rate_per_unit = models.FloatField(null=True)
    amount = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.hotel_id)

    class Meta:
        db_table = 'hotel_predefined_products'
        ordering = ['updated_at']


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_name = models.CharField(max_length=500, db_column='invoice_name')
    invoice_data = JSONField()
    pay_date = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.invoice_name)

    class Meta:
        db_table = 'invoice'
        ordering = ['updated_at']




