from rest_framework import status
from rest_framework.exceptions import APIException


class ProfessionNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Profession not found.'
    default_code = 'not_found'


class ProfessionAdmissionNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Profession admission not found.'
    default_code = 'not_found'
