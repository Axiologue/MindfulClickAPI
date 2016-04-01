from django.db import models

from django.conf import settings

# Article is the base link to outside information
# an 'article' can actually be a report, journalism, or anything else relevant to our research
class Reference(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)

    notes = models.TextField(blank=True,null=True)

    pub_date = models.DateTimeField(blank=True,null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-add_date',)
