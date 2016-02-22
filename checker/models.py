from checker.loadconf import load_smtp_conf
from django.db import models
import uuid

from pingdumb.smtp_module import send_email
from email.mime.text import MIMEText


class User(models.Model):
    nickname = models.CharField(max_length=50, unique=True)


class Site(models.Model):
    user = models.ForeignKey("User")
    url = models.CharField(max_length=300)
    uuid_to_verify = models.CharField(max_length=70, default=str(uuid.uuid4()))
    is_verified = models.BooleanField(default=False)

    def send_register_mail(self, host):
        s = load_smtp_conf()
        verify_link = "http://" + host + "/" + self.user.nickname \
                      + "/verify/" + self.url + "/" + self.uuid_to_verify
        msg = self.form_msg_verify("sitechecker 등록을 원하신다면 <a href=\""
                                   + verify_link + "\">" + verify_link +
                                   "</a>로 이동해주세요", self.user.nickname + "@gmail.com")
        send_email(s, msg)

    def form_msg_verify(self, text, to):
        our_application = "sitechecker"
        msg = MIMEText(text, _subtype='html', _charset="utf-8")
        msg['Subject'] = 'Verify your account'
        msg['From'] = our_application
        msg['To'] = to
        return msg

    def form_msg_status(self, text, to):
        our_application = "sitechecker"
        msg = MIMEText(text, _subtype='html', _charset="utf-8")
        msg['Subject'] = 'Check your site\'s status'
        msg['From'] = our_application
        msg['To'] = to
        return msg

    def verify(self, uuid):
        self.is_verified = uuid == self.uuid_to_verify
        return self.is_verified

    def url_type(url):
        if "://" not in url:
            return "http://" + url
        else:
            return url
