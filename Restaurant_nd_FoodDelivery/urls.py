from django.contrib import admin
from django.urls import path
from myRestaurant import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.MainPage, ),
    path('register/',views.Register, name="Register"),
    path('login/',views.login_view, name = 'Login'),
    path('logout/',views.logout_view, name = 'Logout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView, name='activate'),
    path('add_to_cart/',views.add_to_cart, name = 'add_item'),
    path('get_cart_item/',views.get_cart_item, name='get_cart'),
    path('remove_to_cart/<int:id>',views.remove_to_cart, name = 'remove_item'),
    path('Plus_minus_quantity/', views.update_quantity , name="update_quantity"),
    path('order_item/',views.Order_place, name = 'order_item'),
    path('Track_order/',views.OrderView, name = 'TrackOrder'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)