from django.contrib import admin
from .models import MenuItem,Catagory,Cart,UserAccount,OrderPlace

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id','email','is_active','is_staff']
    
class MenuItemAdmin(admin.ModelAdmin):
    
    list_display = ['name','price','catagory','description',]
    search_fields = ['name','catagory','price']
    list_filter = ['name','catagory','price']
    
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_cart','item','quantity']
    
class OrderPlaceAdmin(admin.ModelAdmin):
    list_display = ['order_id','order_item','order_user','amount','is_paid','status']
    

admin.site.register(OrderPlace,OrderPlaceAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(UserAccount,UserAccountAdmin)
admin.site.register(MenuItem,MenuItemAdmin)
admin.site.register(Catagory,CatagoryAdmin)
