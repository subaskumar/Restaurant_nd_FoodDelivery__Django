# Generated by Django 3.2 on 2022-02-23 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myRestaurant', '0005_orderplace_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplace',
            name='amount',
            field=models.FloatField(),
        ),
    ]
