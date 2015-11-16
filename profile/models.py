from django.db import models
from django.contrib.auth.models import User

from tags.models import EthicsType

# Class for holding individual prefreences on ethical issues
# There should be a one-to-one ratio Preferences and and EthicalTypes for any given user
class Preference(models.Model):
    user = models.ForeignKey(User,related_name="preferences")
    tag_type = models.ForeignKey(EthicsType)

    preference = models.FloatField()

    class Meta:
        unique_together = ('user','tag_type')

    def __str__(self):
        return "{0} - {1}: {2}".format(self.user,self.tag_type,self.preference)

    def save(self, *args, **kwargs):
        # Ensure that the preference stays in the proper range:
        if self.preference > 5:
            self.preference = 5
        if self.preference < -5:
            self.preference = -5

        return super(Preference, self).save(*args, **kwargs)

# Question to Help Set Tag Preferences 
class Question(models.Model):
    question = models.TextField()
    supplement = models.TextField(blank=True,null=True)

# Possible Answers to any given question
class Answer(models.Model):
    question = models.ForeignKey(Question,related_name="answers")

    answer = models.TextField()

    # All users who have chosen this particular answer
    users = models.ManyToManyField(User,related_name="answered",blank=True)

# Modifiers based on any given answer
# Again, ideally there is a 1-to-1 ratio of Modifiers to EthicsTypes
class Modifier(models.Model):
    answer = models.ForeignKey(Answer, related_name="modifiers")
    tag_type = models.ForeignKey(EthicsType)

    # Value to shift the preferences when applied
    modifier = models.IntegerField()

    # Tracking users who have applied this migration
    users = models.ManyToManyField(User,related_name="applied",blank=True)

    def __str__(self):
        return "{0} : {1}".format(self.answer,self.tag_type)
