import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import myRestaurant.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restaurant_nd_FoodDelivery.settings')

application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    
    
    "websocket": AuthMiddlewareStack(
        URLRouter(
            myRestaurant.routing.websocket_urlpatterns
        )
    ),
})