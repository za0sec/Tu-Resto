# Create your views here.
from rest_framework import status, generics
from rest_framework.response import Response

from .permissions import AllowAny
from .serializers import RestaurantSerializer

from apps.restaurant.models import Restaurant


class RestaurantCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RestaurantSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        restaurant = Restaurant.objects.create(**serializer.validated_data)

        return Response(RestaurantSerializer(restaurant).data, status=status.HTTP_201_CREATED)

