from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIRequestFactory

from apps.professions.models import Profession
from apps.professions.views import ProfessionListAPIView

User = get_user_model()


class TestProfessionListAPIView(TestCase):
    view = ProfessionListAPIView
    factory = APIRequestFactory()
    url = reverse('profession-list-url')

    def setUp(self) -> None:
        self.prof1 = mixer.blend(Profession, position=1)
        self.prof2 = mixer.blend(Profession, position=2)

    def test_get_professions(self):
        request = self.factory.get(self.url)
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.prof1.id)
        self.assertEqual(response.data[0]['name'], self.prof1.name)
        self.assertEqual(response.data[1]['id'], self.prof2.id)
        self.assertEqual(response.data[1]['name'], self.prof2.name)

    def test_get_professions_with_name_qp(self):
        new_prof = mixer.blend(Profession, name='Test prof name')
        request = self.factory.get(self.url, data={'name': 'test Prof'})
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], new_prof.id)
        self.assertEqual(response.data[0]['name'], new_prof.name)
