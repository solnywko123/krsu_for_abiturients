from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.chat.api_exceptions import AbiturientChatBannedException
from apps.chat.models import Conversation, Message
from apps.chat.views import ChatHistoryAPIView

User = get_user_model()


class TestChatHistoryAPIView(TestCase):
    view = ChatHistoryAPIView
    factory = APIRequestFactory()
    url = reverse('chat-history-url')

    def setUp(self) -> None:
        self.user = mixer.blend(User)
        conversation = mixer.blend(Conversation, sender=self.user, status=Conversation.ACTIVE)
        mixer.cycle(10).blend(Message, conversation=conversation)

    def test_get_chat(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_chat__unauthorized(self):
        request = self.factory.get(self.url)
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_chat__banned(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        conversation = self.user.conversation
        conversation.status = Conversation.BANNED
        conversation.save(update_fields=['status'])
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], AbiturientChatBannedException.default_detail)
