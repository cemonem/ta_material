from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/simulation/', consumers.SimulationConsumer.as_asgi()),
]
