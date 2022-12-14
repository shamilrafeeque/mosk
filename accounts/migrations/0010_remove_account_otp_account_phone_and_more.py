# Generated by Django 4.0.6 on 2022-07-08 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_account_is_verified_account_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='otp',
        ),
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.TextField(max_length=20, null=b'I01\n'),
            preserve_default=b'I01\n',
        ),
        migrations.AlterField(
            model_name='account',
            name='is_verified',
            field=models.BooleanField(default=False, null=b'I01\n'),
        ),
    ]
