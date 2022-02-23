from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import channels.layers
import json
import random
import string

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        
        if not email:
            raise ValueError('users must have a Email')
        if not password:
            raise ValueError('user must have a Password')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_staffuser(self, email,password,**extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff User must have is_staff=True.')
        
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
    
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    
class Catagory(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    pic = models.ImageField(upload_to='MenuItem')
    full_pic = models.ImageField(upload_to='MenuItem')
    description = models.TextField()
    price = models.DecimalField(max_digits=4,decimal_places=2)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user_cart = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.item)
    


def random_string_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

CHOICES = (
    ("Order Recieved", "Order Recieved"),
    ("Baking", "Baking"),
    ("Baked", "Baked"),
    ("Out for delivery", "Out for delivery"),
    ("Delivered", "Delivered"),    
)
  
class OrderPlace(models.Model):
    
    order_id = models.CharField(max_length=100 , blank=True)
    order_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    order_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.FloatField()
    status = models.CharField(max_length=100 , choices = CHOICES , default="Order Recieved")
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=True)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True)
    is_paid = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):  
        if not len(self.order_id):
            self.order_id = random_string_generator()
        super(OrderPlace, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.order_id
    
    
    @staticmethod
    def give_order_details(user_id):
        instance = OrderPlace.objects.filter(order_user=user_id)
        return list(instance.values('order_id','status','amount'))
                        
    
    def __str__(self):
        return self.order_id

channel_layer = get_channel_layer()

@receiver(post_save, sender=OrderPlace)
def order_status_handler(sender, instance,created , **kwargs):
    if not created:
        my_oders = OrderPlace.objects.filter(order_user = instance.order_user)
    
        async_to_sync(channel_layer.group_send)(
                'user_%s' % instance.order_user.id,{
                'type': 'order_status',
                'value': list(my_oders.values('order_id','status','amount'))
                }
            )