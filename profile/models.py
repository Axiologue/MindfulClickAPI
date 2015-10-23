from django.db import models
from django.contrib.auth.models import User

from tags.models import EthicsType

class TagPref(models.Model):
    user = models.ForeignKey(User,related_name="preferences")
    tag_type = models.ForeignKey(EthicsType)

    preference = models.FloatField()

    class Meta:
        unique_together = ('user','tag_type')

    def __str__(self):
        return "{0} - {1}: {2}".format(self.user,self.tag_type,self.preference)
