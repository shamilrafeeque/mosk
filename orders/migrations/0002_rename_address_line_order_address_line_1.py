# Generated by Django 4.0.6 on 2022-07-22 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address_line',
            new_name='address_line_1',
        ),
    ]
