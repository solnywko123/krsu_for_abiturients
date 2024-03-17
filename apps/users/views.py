import random

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api_exceptions import VerificationCodeIncorrectExc
from apps.users.models import UserRegistrationApplication, Abiturient
from apps.users.serializers import AbiturientAuthTokenSerializer, \
    AbiturientRegistrationApplicationSrz, AbiturientRegistrationApplicationResponseSrz, \
    AbiturientRegistrationApplicationConfirmationSrz, AbiturientTokenResponseSrz, \
    AbiturientProfileSrz


class AbiturientObtainAuthToken(ObtainAuthToken):

    serializer_class = AbiturientAuthTokenSerializer

    @swagger_auto_schema(operation_summary='Obtain auth abiturient token',
                         request_body=AbiturientAuthTokenSerializer,
                         responses={status.HTTP_200_OK: AbiturientTokenResponseSrz()})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class AbiturientRegistrationApplicationCreateAPIView(CreateAPIView):
    serializer_class = AbiturientRegistrationApplicationSrz
    verification_code = None

    def perform_create(self, serializer):
        self.verification_code = random.randint(1001, 9999)
        serializer.save(verification_code=self.verification_code)

    @swagger_auto_schema(operation_summary='Create registration abiturient application',
                         request_body=AbiturientRegistrationApplicationSrz,
                         responses={status.HTTP_200_OK: AbiturientRegistrationApplicationResponseSrz()})
    def post(self, request, *args, **kwargs):
        response = super(AbiturientRegistrationApplicationCreateAPIView, self).post(request, *args, **kwargs)

        result = send_mail(
            'Абитуриент КРСУ ЕТФ: Подтверждение вашей электронной почты для регистрации',
            f'{self.verification_code}',
            settings.EMAIL_HOST_USER,
            [response.data['email']],
            fail_silently=True,
            html_message=f'<h1>Ваш код подтверждения: {self.verification_code}</h1>',
        )
        response_srz = AbiturientRegistrationApplicationResponseSrz(data={'email': response.data['email'],
                                                                          'has_sent': True if result else False})
        response_srz.is_valid()
        return Response(response_srz.data, status=status.HTTP_201_CREATED)


class AbiturientRegistrationApplicationConfirmAPIView(APIView):

    @swagger_auto_schema(
        operation_summary='Confirm abiturient application email',
        request_body=AbiturientRegistrationApplicationConfirmationSrz,
        responses={status.HTTP_200_OK: AbiturientTokenResponseSrz(),
                   status.HTTP_400_BAD_REQUEST: '{"detail": "%s"' % VerificationCodeIncorrectExc.default_detail}
    )
    def post(self, request):
        srz = AbiturientRegistrationApplicationConfirmationSrz(data=request.data)
        srz.is_valid(raise_exception=True)
        try:
            application = UserRegistrationApplication.objects.get(verification_code=srz.data['verification_code'], email=srz.data['email'])
        except UserRegistrationApplication.DoesNotExist:
            raise VerificationCodeIncorrectExc()

        with transaction.atomic():
            abiturient = Abiturient.objects.create_abiturient(application.email, application.password)
            application.delete()
        token, created = Token.objects.get_or_create(user=abiturient)
        resp_srz = AbiturientTokenResponseSrz(data={'token': token.key})
        resp_srz.is_valid()
        return Response(resp_srz.data, status=status.HTTP_200_OK)


class AbiturientProfileUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_summary='Get abiturient profile',responses={
        status.HTTP_200_OK: AbiturientProfileSrz(),
        status.HTTP_401_UNAUTHORIZED: '{"detail": "Учетные данные не были предоставлены."}',
    })
    def get(self, request):
        srz = AbiturientProfileSrz(instance=request.user)
        return Response(srz.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary='Update abiturient profile',
                         request_body=AbiturientProfileSrz, responses=
                         {status.HTTP_200_OK: AbiturientProfileSrz(),
                          status.HTTP_401_UNAUTHORIZED: '{"detail": "Учетные данные не были предоставлены."}'})
    def put(self, request):
        srz = AbiturientProfileSrz(instance=request.user, data=request.data)
        srz.is_valid(raise_exception=True)
        srz.save()
        return Response(srz.data, status=status.HTTP_200_OK)
