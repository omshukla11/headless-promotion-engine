from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# for reseting password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse

from .utils import Util
from django.conf import settings




User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
    
    def save(self, validated_data):
        user = User.objects.create_user( 
                                password=validated_data.get('password'), 
                                email=validated_data.get('email'),
                                username=validated_data.get('username'),
                                )
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=666)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=3)
    tokens = serializers.CharField(max_length=68, min_length=8, read_only=True)

    class Meta:
        model=User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):

        email = attrs.get('email','')
        password = attrs.get('password', '')

        filtered_user_by_email = User.objects.filter(email=email)
        auth_user = auth.authenticate(email=email, password=password)
        print(auth_user)
        if not auth_user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not auth_user.is_active:
            raise AuthenticationFailed("Account Disabled, contact admin")
        if not auth_user.is_verified:
            raise AuthenticationFailed("Email not verified yet!!")

        tokens = RefreshToken.for_user(user=auth_user)
        return {
            'email': auth_user.email,
            'refresh': str(tokens),
            'access': str(tokens.access_token)
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    # redirect_url = serializers.CharField(max_length=500, required=False)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs['email']
        print(email)
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            #hashing the user id 
            token=PasswordResetTokenGenerator().make_token(user) 
            #this token becomes invalid once the user has reset the password
            relative_link = reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
            abs_url = settings.FRONT_END_HOST + relative_link
            email_body = "Hiii! Use link below to reset your password \n"+ abs_url
            data ={'email_body': email_body, 'email_subject': "reset your password",'to_email':user.email}
            Util.send_email(data)
        
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


##############SOCIAL AUTH#######################
from . import google,facebook
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed
from decouple import config

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('The token is invalid or expired. Please login again')
        
        if user_data['aud'] != config('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')
        
        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(provider = provider, user_id = user_id, email = email, name = name)


class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except:
            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )
