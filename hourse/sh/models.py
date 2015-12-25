from __future__ import unicode_literals

from django.db import models

class Person(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255, blank=False, null=False)

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    link = models.CharField(max_length=255, blank=False, null=False)
    pub_date = models.DateTimeField('date posted', null=True)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=False, null=False)
    content = models.TextField(null=True)
