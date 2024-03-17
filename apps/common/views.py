from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.models import OnboardPage
from apps.common.serializers import OnboardPageSrz


class OnboardGetAPIView(APIView):

    @swagger_auto_schema(
        operation_summary='Get onboard page',
        responses={status.HTTP_200_OK: OnboardPageSrz(), status.HTTP_204_NO_CONTENT: None})
    def get(self, request):
        onboard = OnboardPage.objects.first()
        if not onboard:
            return Response(status=status.HTTP_204_NO_CONTENT)
        srz = OnboardPageSrz(instance=onboard, context={'request': request})
        return Response(srz.data, status.HTTP_200_OK)
