from django.test import TestCase, Client
from .models import User


class DBTest(TestCase):

    def test_user_model_save_and_get_data(self):
        User.objects.create(nickname="nickname")
        all_users = User.objects.all()
        self.assertTrue(all_users)


class HomePageTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_get_homepage_response(self):
        response = self.c.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertIn(response.content('Hello'))
