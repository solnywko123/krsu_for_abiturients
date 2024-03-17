from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.chat.api_exceptions import AbiturientChatBannedException
from apps.chat.models import Conversation, Message
from apps.chat.views import ChatHistoryAPIView, ChatSendMessageAPIView

User = get_user_model()


class TestChatSendMessageAPIView(TestCase):
    view = ChatSendMessageAPIView
    factory = APIRequestFactory()
    url = reverse('chat-send-msg-url')

    def test_send_message(self):
        self.user = mixer.blend(User)
        conversation = mixer.blend(Conversation, sender=self.user, status=Conversation.ACTIVE)
        request = self.factory.post(self.url, data={'text': 'Hello!'})
        force_authenticate(request, user=self.user)
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data['id'], int)
        msg = Message.objects.select_related('conversation').get(id=response.data['id'])
        self.assertEqual(response.data['text'], msg.text)
        self.assertEqual(response.data['status'], Message.SENT)
        self.assertEqual(msg.status, Message.SENT)
        self.assertEqual(response.data['type'], Message.FROM_USER)
        self.assertEqual(msg.type, Message.FROM_USER)
        self.assertEqual(msg.conversation, conversation)

    def test_send_message__unauthorized(self):
        request = self.factory.post(self.url, data={'text': 'Hello!'})
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_send_message__banned(self):
        self.user = mixer.blend(User)
        mixer.blend(Conversation, sender=self.user,
                                   status=Conversation.BANNED)
        request = self.factory.post(self.url, data={'text': 'Hello!'})
        force_authenticate(request, user=self.user)
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], AbiturientChatBannedException.default_detail)
