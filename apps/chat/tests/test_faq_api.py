from django.test import TestCase
from django.urls import reverse

from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIRequestFactory

from apps.chat.models import FAQ
from apps.chat.views import FAQListAPIView


class TestFAQAPIView(TestCase):

    view = FAQListAPIView
    factory = APIRequestFactory()
    url = reverse('faq-list-url')

    def setUp(self) -> None:
        for position in range(1, 16):
            mixer.blend(FAQ, position=position)

    def test_get_faq_list(self):
        request = self.factory.get(self.url)
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 15)
        self.assertEqual(response.data['next'], request.build_absolute_uri(self.url) + '?limit=10&offset=10')
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 10)
        first_faq = FAQ.objects.first()
        self.assertEqual(response.data['results'][0]['id'], first_faq.id)
        self.assertEqual(response.data['results'][0]['question'], first_faq.question)
        self.assertEqual(response.data['results'][0]['answer'], first_faq.answer)

        next_request = self.factory.get(response.data['next'])
        response = self.view.as_view()(next_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 15)
        self.assertIsNone(response.data['next'])
        self.assertEqual(response.data['previous'], request.build_absolute_uri(self.url) + '?limit=10')
        self.assertEqual(len(response.data['results']), 5)
        last_faq = FAQ.objects.order_by('position').last()
        self.assertEqual(response.data['results'][-1]['id'], last_faq.id)
        self.assertEqual(response.data['results'][-1]['question'], last_faq.question)
        self.assertEqual(response.data['results'][-1]['answer'], last_faq.answer)

