from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import send_activation_code

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password',
            'password_confirm' 
        ] 

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists')
        return email

    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError(
                'Passwords does not match'
            )
        return attrs

    def create(self, validated_data):
        print('CREATING USER WITH DATA:', validated_data)
        return User.objects.create_user(**validated_data)


    def save(self):
        data = self.validated_data
        user = User.objects.create_user(**data)
        user.send_activation_code()



# class LoginSerializer(TokenObtainPairSerializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True, min_length=8)

#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('Email does not exist')
#         return email

#     def validate (self, attrs):
#         email = attrs.get('email')
#         password = attrs.pop('password')
#         user = User.objects.get(email=email)
#         if not user.check_password(password):
#             raise serializers.ValidationError('Invalid password')
#         if user and user.is_active:
#             refresh = self.get_token(user)
#             attrs['refresh']=str(refresh)
#             attrs['access']=str(refresh.access_token)
#         return attrs

# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

#     default_error_message = {
#         'bad_token': ('Token is expired or invalid')
#     }

#     def validate(self, attrs):
#         self.token = attrs['refresh']
#         return attrs

#     def save(self, **kwargs):
#         try:
#             RefreshToken(self.token).blacklist()
#         except TokenError:
#             self.fail('bad_token')



class ProfileSerializer(serializers.ModelSerializer):
    
    contact_us = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            'name',
            'last_name',
            "username",
            'contact_us',
        )