import random

from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.users.models import UserRegistrationApplication, Abiturient, User


class AbiturientAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        write_only=True
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


def random_randint():
    return random.randint(1001, 9999)


class AbiturientRegistrationApplicationSrz(serializers.ModelSerializer):
    verification_code = serializers.HiddenField(default=random_randint)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, allow_null=False)
    email = serializers.EmailField(max_length=254, min_length=8, allow_null=False)

    class Meta:
        model = UserRegistrationApplication
        fields = ('email', 'password', 'verification_code',)

    def validate_email(self, value: str):
        if Abiturient.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с такой электронной почтой уже существует.')
        return value


class AbiturientRegistrationApplicationResponseSrz(serializers.Serializer):
    email = serializers.EmailField(max_length=254, min_length=8)
    has_sent = serializers.BooleanField(help_text='has sent letter to email?')


class AbiturientRegistrationApplicationConfirmationSrz(serializers.Serializer):
    email = serializers.EmailField(max_length=254, min_length=8)
    verification_code = serializers.IntegerField()

    def validate_verification_code(self, value: int):
        if value < 1000 or value > 9999:
            raise serializers.ValidationError('Код подтверждения должен быть положительным 4-значным числом.')
        return value

    def validate_email(self, value: str):
        if Abiturient.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с такой электронной почтой уже существует.')
        return value


class AbiturientTokenResponseSrz(serializers.Serializer):
    token = serializers.CharField(allow_null=False)


class AbiturientProfileSrz(serializers.ModelSerializer):

    phone_number = serializers.CharField(max_length=25, allow_null=False, min_length=8, required=True)
    school_fullname = serializers.CharField(max_length=255, allow_null=False, required=True)
    first_name = serializers.CharField(allow_null=False, required=True)
    last_name = serializers.CharField(allow_null=False, required=True)
    citizenship = serializers.IntegerField(
        min_value=0, required=True, max_value=5,
        help_text='{1: "KG", 2: "RU", 3: "KZ", 4: "BY", 5: "TJ", 0: "others"}')

    class Meta:
        model = Abiturient
        fields = ('phone_number', 'citizenship', 'school_fullname', 'first_name', 'last_name')
