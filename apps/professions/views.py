from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.professions.api_exceptions import ProfessionNotFoundException, \
    ProfessionAdmissionNotFoundException
from apps.professions.models import Profession, AdmissionCondition
from apps.professions.serializers import ProfessionListSrz, \
    ProfessionRetrieveSrz, ProfessionAdmissionSrz


class ProfessionListAPIView(ListAPIView):
    serializer_class = ProfessionListSrz
    pagination_class = None

    def get_queryset(self):
        name_qp = self.request.query_params.get('name')
        if name_qp:
            qs = Profession.objects.filter(name__icontains=name_qp)
        else:
            qs = Profession.objects.all()
        return qs.only('id', 'name')

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)])
    def get(self, request, *args, **kwargs):
        return super(ProfessionListAPIView, self).get(request, *args, **kwargs)


class ProfessionRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProfessionRetrieveSrz
    queryset = Profession.objects.all()

    def get_object(self):
        try:
            return (
                self.queryset
                .prefetch_related('images')
                .get(id=self.kwargs['pk'])
            )
        except Profession.DoesNotExist:
            raise ProfessionNotFoundException()

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: ProfessionRetrieveSrz,
        status.HTTP_404_NOT_FOUND: ProfessionNotFoundException.default_detail,
    })
    def get(self, request, *args, **kwargs):
        return super(ProfessionRetrieveAPIView, self).get(request, *args, **kwargs)


class ProfessionAdmissionRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProfessionAdmissionSrz
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return AdmissionCondition.objects.prefetch_related('for_citizens').get(professions=self.kwargs['pk'])
        except AdmissionCondition.DoesNotExist:
            raise ProfessionAdmissionNotFoundException()

    @swagger_auto_schema(responses={
        status.HTTP_404_NOT_FOUND: '{"detail": "%s"' % ProfessionAdmissionNotFoundException.default_detail,
        status.HTTP_401_UNAUTHORIZED: '{"detail": "Учетные данные не были предоставлены."}'
    })
    def get(self, request, *args, **kwargs):
        return super(ProfessionAdmissionRetrieveAPIView, self).get(request, *args, **kwargs)
