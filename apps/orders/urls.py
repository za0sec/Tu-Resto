from django.urls import path
from views import TakeAwayOrderDetailView

urlpatterns = [
    path("restaurants", TakeAwayOrderDetailView.as_view(), name="takeawayorder-detail"),
]