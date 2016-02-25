from unittest import TestCase


from batch.batch import check
from checker.models import User, Site


class BatchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(nickname="jellymsblog")
        self.verified_site = Site.objects.create(
            user=self.user, url="jellyms.kr")

    def test_check(self):
        try:
            check()
        except IOError:
            self.assertFail()
            return
        self.assertTrue(True)
