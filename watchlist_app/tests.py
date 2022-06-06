from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testcase", password="test@1234")
        self.token = Token.objects.get(user__username='testcase')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # create a stream platform
        self.stream = models.StreamPlatform.objects.create(name="Amazon Prime Video",
                                                           about="a streaming platform by Amazon",
                                                           website="https://primevideo.com/")
        self.stream.save()

    def test_streamplatform_create(self):
        data = {
                "name": "Netflix",
                "about": "A streaming platform",
                "website": "https://netflix.com"
                }
        response = self.client.post(reverse('platform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('platform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_item(self):
        response = self.client.get(reverse('platform-details', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_update(self):
        data = {
                "name": "Prime Video",
                "about": "A streaming platform by Amazon. Has thousands of series, podcasts, movies and many more!",
                "website": "https://primevideo.com"
                }
        response = self.client.put(reverse('platform-details', args=(self.stream.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_delete(self):
        response = self.client.delete(reverse('platform-details', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
