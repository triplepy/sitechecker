from django.test import TestCase, Client
from .models import User, Site


class DBTest(TestCase):

    def test_user_model_save_and_get_data(self):
        User.objects.create(nickname="nickname")
        all_users = User.objects.all()
        self.assertTrue(all_users)

    def test_site_model_save_and_get_data(self):
        some_user = User.objects.create(nickname="site_model_test")
        Site.objects.create(user=some_user)
        all_sites = Site.objects.all()
        self.assertTrue(all_sites)


class HomePageTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_get_homepage_response(self):
        response = self.c.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertIn("Hello", response.content.decode())
