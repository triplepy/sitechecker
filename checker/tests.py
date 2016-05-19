
import os
import uuid


from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client
from django.test.client import RequestFactory
from .models import User, Site
from .views import home, delete


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
        self.assertIn("sitechecker", response.content.decode())


class VerifyTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(nickname="jellymsblog")
        self.verified_site = Site.objects.create(
            user=self.user, url="jellyms.kr")
        self.not_verified_site = Site.objects.create(
            user=self.user, url="injellyms.kr")

    def test_verify_success(self):
        site_uuid = self.verified_site.uuid_to_verify
        self.verified_site.verify(site_uuid)
        self.assertTrue(self.verified_site.is_verified)

    def test_verify_fail(self):
        site_uuid = str(uuid.uuid4())
        result = self.not_verified_site.verify(site_uuid)
        self.assertFalse(self.verified_site.is_verified)
        self.assertFalse(result)


class PostDataTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post_data(self):
        nickname = 'test_post_data'
        url = 'jellyms.kr'
        request = self.factory.post('/',
                                    {'nickname': nickname, 'siteurl': url})

        request.user = AnonymousUser()

        response = home(request)
        self.assertEqual(200, response.status_code)

        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            pass
        self.assertTrue(user, "User Does not exist")

        try:
            define_url = Site.url_type(url)
            site = Site.objects.get(user=user, url=define_url)
        except Site.DoesNotExist:
            pass
        self.assertTrue(site, "Site does not exist")

    def test_post_data_twice(self):
        nickname = 'twicenick'
        request_url = 'twicesite.jelly'

        request = self.factory.post('/',
                                    {'nickname': nickname, 'siteurl': request_url})

        request.user = AnonymousUser()

        response = home(request)
        self.assertEquals(200, response.status_code)

        response = home(request)
        self.assertEquals(200, response.status_code)

        user = User.objects.filter(nickname=nickname)
        self.assertEquals(1, len(user))

        define_url = Site.url_type(request_url)
        site = Site.objects.filter(url=define_url)
        self.assertEquals(1, len(site))


class DeleteSiteTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.nickname = "to_delete"
        self.user = User.objects.create(nickname=self.nickname)
        self.url = "to_delete_url"
        self.site = Site.objects.create(user=self.user, url=self.url)

    def test_delete_site(self):
        request = self.factory.post('/delete',
                                    {'nickname': self.nickname,
                                     'siteurl': self.url})
        request.user = AnonymousUser()

        response = delete(request)
        self.assertEquals(200, response.status_code)

        deleted_site = Site.objects.filter(url=self.site.url)
        self.assertFalse(deleted_site)

if not os.getenv('BUILD_ON_TRAVIS', None):
    class IsSet(TestCase):
        def setUp(self):
            try:
                self.username = os.environ['SITECHECKER_SMTP_USERNAME']
            except KeyError:
                self.username = ""
            try:
                self.password = os.environ['SITECHECKER_SMTP_PASSWORD']
            except KeyError:
                self.password = ""

        def test_is_set(self):
            if not self.username:
                self.assertFail("please set environment variable username")
            if not self.password:
                self.assertFail("please set environment variable password")



