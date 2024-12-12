from django.shortcuts import render, get_object_or_404
from apps.restaurant.models import Restaurant, Branch

def reservation_page(request, restaurant_name, branch_name):
    restaurant = get_object_or_404(Restaurant, name=restaurant_name)
    branch = get_object_or_404(Branch, restaurant=restaurant, name=branch_name)
    
    context = {
        'restaurant': restaurant,
        'branch': branch,
    }
    
    return render(request, 'reservations/reservation_page.html', context)
