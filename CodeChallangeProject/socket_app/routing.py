from django.urls import path

from .consumer import *

websocket_urlpatterns = [
    path("behave/", DriverBehaviourReceiver.as_asgi()),
]