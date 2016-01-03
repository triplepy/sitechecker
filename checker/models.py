from django.db import models
import uuid

class User(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    


class Site(models.Model):
    user = models.ForeignKey("User")
    url = models.CharField(max_length=300)
    uuid_to_ceitify = models.CharField(max_length=70, default=str(uuid.uuid4()))
    is_verified = models.BooleanField(default=False)

    def send_register_mail(self):
        #TODO 구현해야 함
        pass

    def verify(self, uuid):
        self.is_verified = uuid == self.uuid_to_ceitify
