from django.test import TestCase
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


        
