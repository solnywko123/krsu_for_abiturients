from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIRequestFactory

from apps.professions.api_exceptions import ProfessionNotFoundException
from apps.professions.models import Profession, ProfessionGalleryImage
from apps.professions.views import ProfessionRetrieveAPIView


User = get_user_model()


class TestProfessionRetrieveAPIView(TestCase):
    view = ProfessionRetrieveAPIView
    factory = APIRequestFactory()

    def setUp(self) -> None:
        self.prof1 = mixer.blend(Profession)
        self.img1 = mixer.blend(ProfessionGalleryImage, profession=self.prof1)
        self.img2 = mixer.blend(ProfessionGalleryImage, profession=self.prof1)

    def test_get_profession(self):
        url = reverse('profession-retrieve-url', kwargs={'pk': self.prof1.id})
        request = self.factory.get(url)
        response = self.view.as_view()(request, pk=self.prof1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.prof1.id)
        self.assertEqual(response.data['name'], self.prof1.name)
        self.assertEqual(response.data['description'], self.prof1.description)
        self.assertEqual(len(response.data['images']), 2)
        self.assertEqual(response.data['images'][0]['id'], self.img1.id)
        self.assertEqual(response.data['images'][0]['image'], request.build_absolute_uri(self.img1.image.url))
        self.assertEqual(response.data['images'][1]['id'], self.img2.id)
        self.assertEqual(response.data['images'][1]['image'], request.build_absolute_uri(self.img2.image.url))

    def test_get_profession__not_found(self):
        deleted_prof_id = self.prof1.id
        self.prof1.delete()
        url = reverse('profession-retrieve-url', kwargs={'pk': deleted_prof_id})
        request = self.factory.get(url)
        response = self.view.as_view()(request, pk=deleted_prof_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], str(ProfessionNotFoundException()))
