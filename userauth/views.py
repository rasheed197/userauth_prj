# views.py
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, OrganisationSerializer, UserSerializer
from .models import User, Organisation, UserOrganisation
from django.shortcuts import get_object_or_404

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
                }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {
                        "status": "Bad request",
                        "message": "Authentication failed",
                        "statusCode": 401,
                    }, status=status.HTTP_401_UNAUTHORIZED)

            if user.check_password(password):
                
                refresh = RefreshToken.for_user(user)
                
                return Response(
                    {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                        "accessToken": str(refresh.access_token),
                        "user": {
                            "userId": user.user_id,
                            "firstName": user.first_name,
                            "lastName": user.last_name,
                            "email": user.email,
                            "phone": user.phone,
                        }
                        }
                    }, status=status.HTTP_200_OK)

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

class OrganisationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        organisations = user.organisations.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data)

class CreatedOrganisationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        created_organisations = Organisation.objects.filter(userorganisation__user=user)
        serializer = OrganisationSerializer(created_organisations, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        logged_in_user = request.user

        # Check if the logged-in user is requesting their own record
        if logged_in_user == user:
            serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "message": "User record retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        # Check if the logged-in user belongs to any organization the user belongs to
        orgs_logged_in_user_belongs_to = Organisation.objects.filter(users=logged_in_user)
        if UserOrganisation.objects.filter(user=user, organisation__in=orgs_logged_in_user_belongs_to).exists():
            serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "message": "User record retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        # If the user does not have permission to view the record
        return Response({
            "status": "failure",
            "message": "You do not have permission to view this user record."
        }, status=status.HTTP_403_FORBIDDEN)
        
class UserOrganisationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Get organizations the user belongs to
        user_organisations = Organisation.objects.filter(userorganisation__user=user)

        # Serialize the data
        serializer = OrganisationSerializer(user_organisations, many=True)
        
        return Response({
            "status": "success",
            "message": "Organisations fetched successfully",
            "data": {
                "organisations": serializer.data
            }
        }, status=status.HTTP_200_OK)
        