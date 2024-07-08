from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer, CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        orgName = f"{user.firstName}'s Organisation"
        # Create organisation and add user to it
        organisation = Organisation.objects.create(name=orgName, description='')
        organisation.users.add(user)  # Use .add() to add the user to the organisation

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = response.data
        token = RefreshToken.for_user(User.objects.get(email=user['email']))
        data = {
            "status": "success",
            "message": "Registration successful",
            "data": {
                "accessToken": str(token.access_token),
                "user": user
            }
        }
        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token = RefreshToken.for_user(user)
        
        data = {
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": str(token.access_token),
                "user": UserSerializer(user).data,
               
            }
        }
        return Response(data, status=status.HTTP_200_OK)
  
class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class OrganisationView(generics.ListCreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.organisations.all()

class SingleOrganisationView(generics.RetrieveAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

class AddUserToOrganisationView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        orgId = kwargs.get('orgId')
        userId = request.data.get('userId')
        organisation = get_object_or_404(Organisation, id=orgId)
        user = get_object_or_404(User, id=userId)
        organisation.users.add(user)
        return Response({
            "status": "success",
            "message": "User added to organisation successfully",
        }, status=status.HTTP_200_OK)

