from rest_framework import status
from rest_framework.exceptions import APIException


class AbiturientChatBannedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Вас заблокировали скорее всего за непристойные сообщения, ' \
                     'теперь вам запрещено писать в чате.'
    default_code = 'user_blocked'
