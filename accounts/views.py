from multiprocessing import AuthenticationError
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import (mixins, generics, status, permissions)
from rest_framework_simplejwt.tokens import RefreshToken
from django.http.response import HttpResponse, JsonResponse
import jwt
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (mixins, generics, status, permissions)
from rest_framework.response import Response

#reseting password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from decouple import config
from django.shortcuts import render
# Create your views here.

from .utils import Util
from accounts.serializers import GoogleSocialAuthSerializer,FacebookSocialAuthSerializer,UserSerializer, EmailVerificationSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer, LogoutSerializer, AdminSerializer
from .models import AdminProfile

User = get_user_model()

class SignUp(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer1 = UserSerializer(data=request.data)
        if serializer1.is_valid():
            user_data = serializer1.save(serializer1.data)
            token = RefreshToken.for_user(user_data).access_token
            relative_link = reverse('EmailVerification')
            abs_url = settings.FRONT_END_HOST + relative_link + "user-id=" + str(token)
            email_body = "Hiii" + "! Use link below to verify your email \n"+ abs_url
            data ={'email_body': email_body, 'email_subject': "Verify your Email",'to_email':user_data.email}
            Util.send_email(data)
            return JsonResponse({'status': 'created', 'token': str(token)}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Enter token here")

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return JsonResponse({'status': 'Email Successfully Verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return JsonResponse({'error':"Activation Link has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return JsonResponse({'error':"Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class Login(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        data = {'request': request, 'email': request.data['email']}
        serializer = self.serializer_class(data=data)
        try: 
            validated = serializer.is_valid(raise_exception=True)
            return Response({'success': 'We have sent you a link to your email to reset your password'}, status=status.HTTP_200_OK)
        except:
            raise HttpResponse({'Invalid Request': status.HTTP_401_UNAUTHORIZED})



class PasswordTokenCheckAPI(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailRequestSerializer

    def get(self,request,uidb64,token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return JsonResponse({'error':'Token is not valid, please request a new one'}, status = status.HTTP_401_UNAUTHORIZED)
            return JsonResponse({'success':True,'message':'Credentials Valid','uidb64':uidb64,'token':token}, status = status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return JsonResponse({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message':'Logged out successfully'},status=status.HTTP_204_NO_CONTENT)


class AdminAPI(mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = AdminProfile.objects.all()
    serializer_class = AdminSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email = request.user)
            print(request.user)
            
            try:
                companyname = request.data['companyname']
                location = request.data['location']
                description = request.data['description']
                coupon_count = int(request.data['coupon_count'])
                img = request.FILES['img']
                admin = AdminProfile.objects.create(user=user, companyname=companyname, location=location, description=description, coupon_count=coupon_count, img=img)
                adminserializer = AdminSerializer(admin).data
                return JsonResponse(adminserializer, status=status.HTTP_201_CREATED)
            except:
                return JsonResponse({'error': 'Admin Profile creation failed'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'error': 'Anonymous user'}, status=status.HTTP_401_UNAUTHORIZED)


##############SOCIAL AUTH#######################

class GoogleAuth(generics.GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class FacebookAuth(generics.GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        serializer = FacebookSocialAuthSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


def index(request):
    GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')
    content = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID}
    return render(request, 'index.html', content)

def facebookindex(request):
    FACEBOOK_APP_ID = config('FACEBOOK_APP_ID')
    content = {'FACEBOOK_APP_ID': FACEBOOK_APP_ID}
    return render(request, 'facebook.html', content)

