from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BlackList, BlackListedUser
from user.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class GetBlackList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response(self.request.user.blacklist.blacklisteduser_set.values_list('user__username', flat=True),
                        status=status.HTTP_200_OK
                        )


class BlackListUser(APIView):
    user_400_exist = {'popup_message': "user with that username doesn't exist"}
    user_400_blacklisted = {'popup_message': '{0} is not blacklisted'}
    user_204 = {'popup_message': (lambda username: '{0} удален из черного списка'.format(username))}
    user_200 = {'popup_message': (lambda username: '{0} добавлен в черный список'.format(username))}
    permission_classes = (IsAuthenticated, )

    def get(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(self.user_400_exist, status=status.HTTP_400_BAD_REQUEST)
        blacklist = request.user.blacklist
        try:
            blacklisted_user = BlackListedUser.objects.get(user=user, blacklist=blacklist)
            blacklisted_user.delete()
            return Response(self.user_204['popup_message'](username), status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            BlackListedUser.objects.create(user=user, blacklist=blacklist)
            return Response(self.user_200['popup_message'](username), status=status.HTTP_200_OK)

    def delete(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(self.user_400_exist, status=status.HTTP_400_BAD_REQUEST)
        blacklist = request.user.blacklist
        try:
            blacklisted_user = BlackListedUser.objects.get(user=user, blacklist=blacklist)
            blacklisted_user.delete()
            return Response(self.user_204['popup_message'](username), status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(self.user_400_blacklisted, status=status.HTTP_400_BAD_REQUEST)
