from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from .utils import Util
from .models import CustomUser
from .serializers import *
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect
import datetime   
import os
FRONTEND_URL='https://robotix.nitrr.ac.in'

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'patch', 'head']
    lookup_field = 'user_id'

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = CustomUser.objects.get(email=serializer.data['email'])
            user_access_token = AccessToken.for_user(user)
            current_site = FRONTEND_URL
            relativeEmailLink = reverse('users:email-verify')
            # relativeMobileLink = reverse('users:mobile-verify')
            abs_emailurl = current_site + relativeEmailLink + "?token=" + str(user_access_token)
            # abs_mobileurl = current_site + relativeMobileLink + "?token=" + str(user_access_token)
            
            email_body = 'Hi ' + user.username + \
                        ' Use the link below to verify your email \n' + abs_emailurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email', 'email_link': abs_emailurl}

            # mobile_msg = 'Hi ' + user.username + \
                        # ' Use the link below to verify your mobile \n' + abs_mobileurl

            Util.send_email(data)
            # Util.send_msg(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.email_verified:
                user.email_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer

    def post(self, request):
        if 'phone_number' in request.data.keys():
            serializer = PhoneLoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                response = Response(
                    serializer.data
                , status=status.HTTP_200_OK)

                response.set_cookie(
                    key='ACCESS_TOKEN',
                    value=serializer.data['tokens']['access'],
                    httponly=False,
                )
                response.set_cookie(
                    key='REFRESH_TOKEN',
                    value=serializer.data['tokens']['refresh'],
                    httponly=False,
                )

                return response
        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                response = Response(serializer.data, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='ACCESS_TOKEN',
                    value=serializer.data['tokens']['access'],
                    samesite='Lax',secure=False, httponly=True
                )
                response.set_cookie(
                    key='REFRESH_TOKEN',
                    value=serializer.data['tokens']['refresh'],
                    samesite='Lax',secure=False, httponly=True
                )

                return response

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email', '')

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.user_id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = FRONTEND_URL
            relativeLink = reverse(
                'users:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = FRONTEND_URL

            absurl = current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                         absurl + "?redirect_url=" + redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'failure' : 'Email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request, uidb64, token):

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(user_id=user_id)

            if PasswordResetTokenGenerator().check_token(user, token):
                serializer = self.serializer_class(user, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(user_id=user_id)
                return Response({'message': 'Password reset success'}, status=status.HTTP_200_OK)
            else: 
                # if len(redirect_url) > 3:
                #     return CustomRedirect(redirect_url + '?token_valid=False')
                # else:
                #     return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')
                return Response({'message': 'Password reset failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # if redirect_url and len(redirect_url) > 3:
            #     return CustomRedirect(
            #         redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            # else:
            #     return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')
        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    # return CustomRedirect(redirect_url + '?token_valid=False')
                    print('failure user')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)
