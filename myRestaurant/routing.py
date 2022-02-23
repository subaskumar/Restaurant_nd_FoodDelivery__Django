from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/order/(?P<user_id>\w+)/$', consumers.OrderProgress.as_asgi()),
]
