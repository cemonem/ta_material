"""
ASGI config for django_sim_example project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import app.routing
from channels.auth import AuthMiddlewareStack
import time
import threading
from channels.layers import get_channel_layer
import app.misc
import math
from asgiref.sync import async_to_sync

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_sim_example.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app.routing.websocket_urlpatterns
        )
    ),
})

#probably a terrible idea but works enough
def simulation_thread():
    channel_layer = get_channel_layer()
    angle = 0
    radius = 10
    pi = math.pi
    while True:
        time.sleep(1)
        with app.misc.lock:
            app.misc.rect_pos["x"] += radius*(math.cos((angle+20.0)/180.0*pi)-math.cos(angle/180.0*pi))
            app.misc.rect_pos["y"] += radius*(math.sin((angle+20.0)/180.0*pi)-math.sin(angle/180.0*pi))
            x = app.misc.rect_pos["x"]
            y = app.misc.rect_pos["y"]
        async_to_sync(channel_layer.group_send)("users", {'type': 'broadcast_msg', 'message': {"x":x, "y":y}})
        angle = (angle+20.0) % 360.0

threading.Thread(target=simulation_thread).start()
