# Generated by Django 4.0.6 on 2022-07-08 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_account_phone_alter_account_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_verified',
        ),
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
