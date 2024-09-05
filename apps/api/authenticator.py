from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from apps.api.serializers import CustomTokenObtainPairSerializer
from apps.users.models import Person


class PersonTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user

        try:
            Person.objects.get(user=user)
        except Person.DoesNotExist:
            del response.data["access"]
            del response.data["refresh"]
            response.status_code = status.HTTP_401_UNAUTHORIZED
            response.data["detail"] = "No tiene un perfil asociado en Person."
            return response

        return response