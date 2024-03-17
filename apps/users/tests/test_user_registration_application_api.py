from unittest import mock

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory

from apps.users.models import UserRegistrationApplication
from apps.users.views import AbiturientRegistrationApplicationCreateAPIView


class TestUserRegistrationApplicationCreateAPIView(TestCase):

    view = AbiturientRegistrationApplicationCreateAPIView
    factory = APIRequestFactory()
    url = reverse('abiturient-registration-url')

    @mock.patch('apps.users.views.AbiturientRegistrationApplicationCreateAPIView.post.send_mail')
    def test_registration_application(self, send_mail_mock):
        send_mail_mock.return_value = 1

        request = self.factory.post(self.url, data={'email': 'testName@email.com', 'password': 'someTestPassword'})
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['has_sent'], True)
        self.assertEqual(response.data['email'], 'testName@email.com')
        application = UserRegistrationApplication.objects.get(email='testName@email.com')
        self.assertEqual(application.password, 'someTestPassword')
        self.assertGreaterEqual(application.verification_code, 1001)
        self.assertLessEqual(application.verification_code, 9999)
