from django.db import models
import uuid
import smtplib

from pingdumb.smtp_module import form_msg, send_email


class User(models.Model):
    nickname = models.CharField(max_length=50, unique=True)


class Site(models.Model):
    user = models.ForeignKey("User")
    url = models.CharField(max_length=300)
    uuid_to_verify = models.CharField(max_length=70, default=str(uuid.uuid4()))
    is_verified = models.BooleanField(default=False)

    def load_smtp_conf(self):
        s = smtplib.SMTP("smtp.gmail.com:587")
        s.starttls()
        username = ""
        password = ""
        s.login(username, password)
        return s

    def send_register_mail(self):
        s = self.load_smtp_conf()
        verify_link = "http://sitechec.kr/site/" + self.user.nickname \
                      + "/verify/" + self.uuid_to_verify
        msg = form_msg("sitechecker 등록을 원하신다면 <a href=\""
                       + verify_link + "\">" + verify_link + "\"</a>로 이동해주세요")
        send_email(s, msg)

    def verify(self, uuid):
        self.is_verified = uuid == self.uuid_to_ceitify
