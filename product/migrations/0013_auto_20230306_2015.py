# Generated by Django 4.1.6 on 2023-03-06 18:15

from django.db import migrations


def calculate_rate(product):
    # Do some calculation based on the product object
    return 0


def set_rate(apps, schema_editor):
    Product = apps.get_model('product', 'Product')
    for product in Product.objects.all():
        # Set the rate value based on some logic
        product.rate = calculate_rate(product)
        product.save()

class Migration(migrations.Migration):

    dependencies = [
        ("product", "0012_alter_product_product_cat"),
    ]

    operations = [
        migrations.RunPython(set_rate),
    ]
