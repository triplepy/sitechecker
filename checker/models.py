from django.db import models


class User(models.Model):
    nickname = models.CharField(max_length=50)


class Site(models.Model):
    user = models.ForeignKey("User")
    url = models.CharField(max_length=300)
