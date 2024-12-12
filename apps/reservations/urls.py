from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('<str:restaurant_name>/<str:branch_name>/reservation/', 
         views.reservation_page, 
         name='reservation_page'),
] 