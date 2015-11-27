from django.test import TestCase
from .models import Users

class DBTest(TestCase):

    def test_user_model_save_and_get_data(self):
        User.create(nickname="nickname")
        all_users = User.objects.all()
        self.asesrtTrue(all_users)
