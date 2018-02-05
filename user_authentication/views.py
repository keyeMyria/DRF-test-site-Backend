from django.contrib.sites.shortcuts import get_current_site
from django.middleware.csrf import get_token
from django.core import signing
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, Http404
from django.conf import settings
from django.template import loader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user_authentication.serializers import RegistrationSerializer, SignInSerializer
from django.contrib.auth import logout


class SigningMixIn(object):
    salt = 'registration'

    def check_signing(self, token):
        token_lifetime = 3600 * 72
        try:
            signing.loads(token, salt=self.salt, max_age=token_lifetime)
        except signing.SignatureExpired:
            return False
        except signing.BadSignature:
            raise Http404

    def activate_user(self, token):
        try:
            user = get_object_or_404(settings.AUTH_USER_MODEL, pk=signing.loads(token, salt=self.salt))
            user.is_active = True
            user.save()
        except signing.BadSignature:
            raise Http404


class SendEmailMixIn(object):
    def send_token(self):
        context = {
            'site': get_current_site(self.request),
            'username': self.user.username,
            'token': signing.dumps(self.user.pk, salt=self.salt),
        }
        subject = 'Hello'
        body = loader.render_to_string('registration/registration_text.txt', context).strip()
        send_mail(subject, body, 'test-site', [self.user.email], fail_silently=False)


class Registration(APIView):
    def post(self, request, filter=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class SignIn(APIView):
    def post(self, request, filter=None):
        serializer = SignInSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({'message': 'success'})
        return Response({'errors': serializer.errors})


class CheckAuth(APIView):
    def get(self, request, filter=None):
        if request.user.is_authenticated:
            return Response({'username': request.user.username, 'auth': True})
        return Response({'auth': False})


class GenerateCSRFToken(APIView):
    def get(self, request):
        print(get_token(request))
        return Response({'token': get_token(request)})


class Logout(APIView):
    def get(self, request, filter=None):
        logout(request)
        return Response({'logout': 'success'})
