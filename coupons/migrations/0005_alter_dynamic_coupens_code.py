# Generated by Django 4.1.7 on 2023-03-11 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0004_dynamic_coupens_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamic_coupens',
            name='code',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]
