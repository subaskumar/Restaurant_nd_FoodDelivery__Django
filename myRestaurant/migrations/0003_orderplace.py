# Generated by Django 3.2 on 2022-02-22 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myRestaurant', '0002_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=100)),
                ('amount', models.IntegerField(default=100)),
                ('status', models.CharField(choices=[('Order Recieved', 'Order Recieved'), ('Baking', 'Baking'), ('Baked', 'Baked'), ('Out for delivery', 'Out for delivery'), ('Order recieved', 'Order recieved')], default='Order Recieved', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=250)),
                ('is_paid', models.BooleanField(default=False)),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myRestaurant.menuitem')),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]