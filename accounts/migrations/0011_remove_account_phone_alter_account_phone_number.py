# Generated by Django 4.0.6 on 2022-07-08 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_account_otp_account_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='phone',
        ),
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.TextField(max_length=20, null=b'I01\n'),
        ),
    ]
