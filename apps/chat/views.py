from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from apps.chat.api_exceptions import AbiturientChatBannedException
from apps.chat.models import Message, Conversation, FAQ
from apps.chat.serializers import MessageSrz, FAQSrz


class ChatHistoryAPIView(generics.ListAPIView):
    """Get user chat history"""

    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSrz
    pagination_class = None

    def get_queryset(self):
        try:
            conversation = Conversation.objects.get(sender=self.request.user)
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(sender=self.request.user,
                                                       status=Conversation.ACTIVE)
        if conversation.status == Conversation.BANNED:
            raise AbiturientChatBannedException()
        return conversation.messages.filter(is_deleted=False).order_by('-sent_at')

    @swagger_auto_schema(responses={status.HTTP_400_BAD_REQUEST: '{"detail": "%s"' % AbiturientChatBannedException.default_detail,
                                    status.HTTP_401_UNAUTHORIZED: '{"detail": "Учетные данные не были предоставлены."}'})
    def get(self, request, *args, **kwargs):
        return super(ChatHistoryAPIView, self).get(request, *args, **kwargs)


class ChatSendMessageAPIView(generics.CreateAPIView):
    """Sending message from user to staff user"""

    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSrz

    def perform_create(self, serializer):
        sender = self.request.user
        try:
            conversation = Conversation.objects.get(sender=sender)
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(sender=sender, status=Conversation.ACTIVE)
        if conversation.status == Conversation.BANNED:
            raise AbiturientChatBannedException()
        serializer.save(type=Message.FROM_USER, conversation=conversation,
                        status=Message.SENT)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, required=['text'],
                                                     properties={'text': openapi.Schema(type=openapi.TYPE_STRING, description='not nullable. max length = 1000 symbols')}),
                         responses={status.HTTP_400_BAD_REQUEST: '{"detail": "%s"' % AbiturientChatBannedException.default_detail,
                                    status.HTTP_401_UNAUTHORIZED: '{"detail": "Учетные данные не были предоставлены."}'})
    def post(self, request, *args, **kwargs):
        return super(ChatSendMessageAPIView, self).post(request, *args, **kwargs)


class FAQListAPIView(generics.ListAPIView):
    """Get list of frequently asked questions"""

    serializer_class = FAQSrz
    queryset = FAQ.objects.all()
