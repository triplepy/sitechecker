from django.db import models

class User(models.Model):
    nickname = models.CharField(max_length=50)
