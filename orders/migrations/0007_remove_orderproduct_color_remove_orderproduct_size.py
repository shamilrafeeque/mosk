# Generated by Django 4.0.6 on 2022-07-25 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_orderproduct_variations_orderproduct_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
    ]
