from django.urls import path
from .views import WhatsappReceiver, LatestOrderWppUrl, Whatsapp

urlpatterns = [
    path('webhook', WhatsappReceiver.as_view(), name='wpp-receiver'),
    
    # Beepers
    path("latestOrderWppUrl/<int:branch>", LatestOrderWppUrl.as_view(), name="orderurl"),
]