# Generated by Django 3.2 on 2022-02-22 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myRestaurant', '0004_alter_orderplace_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplace',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
