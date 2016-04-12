import markdown

from django.db import models
from django.utils.text import slugify
from django.utils.html import strip_tags

from django.conf import settings

class Post(models.Model):
    # Meta info
    pub_time = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Post Content
    title = models.CharField(max_length = 300, unique=True)
    sub_title = models.CharField(max_length = 300)
    body = models.TextField()

    # Post Title URL
    title_url = models.SlugField(editable=False, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_time']

    # Overwrite save function to add auto-slugify for post title/URL
    def save(self, *args, **kwargs):
        self.title_url = slugify(self.title)[:50]

        super(Post, self).save(*args,**kwargs)

    @property
    def excerpt(self):
        # convert markdown to html and then strip
        html = markdown.markdown(self.body[:500])
        excerpt = strip_tags(html)

        return excerpt
