import django
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookStore.settings')
django.setup()

websocket_urlpatterns = []

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns)
})
