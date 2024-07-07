# views.py
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, OrganisationSerializer
from .models import User, Organisation, UserOrganisation

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            user = result['user']
            access_token = result['access_token']
            response_data = {
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": access_token,
                    "user": {
                        "userId": user.user_id,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    "status": "Bad request",
                    "message": "Registration unsuccessful",
                    "statusCode": 400
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class UserLoginView(APIView):
    def post(self, request):
        print(f"Data = {request.data}")
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                # print(f"user password - {user.password}")
            except User.DoesNotExist:
                return Response(
                    {
                        "status": "Bad request",
                        "message": "Authentication failed",
                        "statusCode": 401
                    }, status=status.HTTP_401_UNAUTHORIZED)

            if user.check_password(password):
                
                print("Password check successful")
                refresh = RefreshToken.for_user(user)
                
                return Response(
                    {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                        "accessToken": str(refresh.access_token),
                        "user": {
                            "userId": "string",
                            "firstName": "string",
                                    "lastName": "string",
                                    "email": "string",
                                    "phone": "string",
                        }
                        }
                    }
                )

            return Response(
                    {
                        "status": "Bad request",
                        "message": "Authentication failed",
                        "statusCode": 401
                    }, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
                    {
                        "status": "Bad request",
                        "message": "Authentication failed",
                        "statusCode": 401
                    }, status=status.HTTP_401_UNAUTHORIZED)

class CreatedOrganisationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        created_organisations = Organisation.objects.filter(userorganisation__user=user)
        serializer = OrganisationSerializer(created_organisations, many=True)
        return Response(serializer.data)
