# Create your views here.
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .permissions import AllowAny
from .serializers import RestaurantSerializer,BranchSerializer

from apps.restaurant.models import Restaurant,Branch
from ..users.models import Person

############    Restaurant      ##############
# ListAPIView already generates the response. No need to define a get method.
class Restaurants(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

# C Create
class RestaurantCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


# RUD Retrieve - Update - Destroy
class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


#############    Branches     ################
class BranchCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


# RUD Retrieve - Update - Destroy
class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class Branches(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializer

    ''' Override get_queryset method in ListAPIView. Allows using custom dynamic query,
    filtering by 'restaurant_id' field from URL path.
    Cuando tienes una relación de clave foránea (ForeignKey), puedes filtrar los objetos utilizando
    tanto el nombre del campo de la relación (restaurant) como el sufijo _id para referenciar directamente 
    el valor de la clave foránea (el ID).'''
    def get_queryset(self):
        # Obtener el ID del restaurante desde los parámetros de la URL
        restaurant_id = self.kwargs['restaurant_id']
        # Filtrar las branches que pertenecen a ese restaurante
        return Branch.objects.filter(restaurant_id=restaurant_id)



# class MyInformation(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserSerializer
#
#     def get(self, request):
#         user = request.user
#         person = Person.objects.get(user=user)
#         return Response({"first_name": person.first_name, "email": user.email})
#
