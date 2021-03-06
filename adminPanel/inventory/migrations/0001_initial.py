# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-05 13:14
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseInventory',
            fields=[
                ('inventory_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100)),
                ('quantity', models.FloatField(null=True)),
                ('units', models.CharField(max_length=100, null=True)),
                ('rate_per_unit', models.FloatField(null=True)),
                ('amount', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created_at'],
                'db_table': 'base_inventory',
            },
        ),
        migrations.CreateModel(
            name='HotelPredefinedProducts',
            fields=[
                ('predefined_id', models.AutoField(primary_key=True, serialize=False)),
                ('hotel_name', models.CharField(db_column='hotel_name', max_length=500)),
                ('product_name', models.CharField(max_length=100)),
                ('quantity', models.FloatField(null=True)),
                ('units', models.CharField(max_length=100, null=True)),
                ('rate_per_unit', models.FloatField(null=True)),
                ('amount', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hotel_id', models.ForeignKey(db_column='hotel_id', on_delete=django.db.models.deletion.CASCADE, to='account.HotelUser')),
                ('product_id', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.CASCADE, to='inventory.BaseInventory')),
            ],
            options={
                'ordering': ['updated_at'],
                'db_table': 'hotel_predefined_products',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_name', models.CharField(db_column='invoice_name', max_length=500)),
                ('invoice_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('pay_date', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['updated_at'],
                'db_table': 'invoice',
            },
        ),
    ]
