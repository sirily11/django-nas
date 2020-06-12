from django.test import TestCase
from django.urls import reverse

from nas.models import File


class TestHome(TestCase):
    def test_home(self):
        """
        Without any files
        :return:
        """
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
