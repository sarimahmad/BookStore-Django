from .views import *
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('signup/', SignUpAPIView.as_view(), name='signup_Api'),
    path('login/', LoginAPIView.as_view(), name='login_Api'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
