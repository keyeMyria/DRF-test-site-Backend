from rest_framework import serializers
from user.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(default='lel')
    email = serializers.EmailField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super(RegistrationSerializer, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages['blank'] = 'введите имя пользователя'
        self.fields['email'].error_messages.update({'blank': 'введите адрес электронной почты',
                                                    'invalid': 'неверный адрес электронной почты'}
                                                   )
        self.fields['password'].error_messages['blank'] = 'введите пароль'

    def validate_username(self, value):
        try:
            CustomUser.objects.get(username=value)
            raise serializers.ValidationError('пользователь с таким именем уже существует')
        except ObjectDoesNotExist:
            pass
        return value

    def validate_email(self, value):
        try:
            CustomUser.objects.get(email=value)
            raise serializers.ValidationError('электронная почта уже используется')
        except ObjectDoesNotExist:
            pass
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('пароль должен состоять минимум из 6 символов')
        return value

    def create(self, validated_data):
        new_user = CustomUser.objects.create(username=validated_data['username'], email=validated_data['email'])
        new_user.set_password(validated_data['password'])


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if user is not None:
            login(self.context.get('request'), user)
        else:
            raise serializers.ValidationError('wrong username or password')
        return data
