# Generated by Django 5.1.6 on 2025-03-13 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_transaction_price_transaction_total_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='date',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='price',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='price_currency',
        ),
        migrations.AddField(
            model_name='stock',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
