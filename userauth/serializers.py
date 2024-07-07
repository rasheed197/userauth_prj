# serializers.py
from rest_framework import serializers
from .models import User, Organisation, UserOrganisation
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'password', 'phone']

    def validate(self, data):
        errors = []
        if not data.get('first_name'):
            errors.append({'field': 'first_name', 'message': 'First name must not be null.'})
        if not data.get('last_name'):
            errors.append({'field': 'last_name', 'message': 'Last name must not be null.'})
        if not data.get('email'):
            errors.append({'field': 'email', 'message': 'Email must not be null.'})
        if not data.get('password'):
            errors.append({'field': 'password', 'message': 'Password must not be null.'})

        if errors:
            raise serializers.ValidationError({"errors": errors})

        return data

    def create(self, validated_data):
        user = User(
            user_id=str(uuid.uuid4()),  # Generate a unique user_id
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
            password=validated_data.get('password'),
        )
        user.password = user.hash_password(validated_data['password'])
        user.save()
        
        organisation_name = f"{user.first_name}'s Organisation" 
        organisation = Organisation.objects.create(name=organisation_name)
        UserOrganisation.objects.create(user=user, organisation=organisation)
        
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': user,
            'access_token': str(refresh.access_token)
        }
        


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['org_id', 'name', 'description']
