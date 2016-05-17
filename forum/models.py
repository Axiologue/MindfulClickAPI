from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    list_order = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('list_order', )

    # Save function to handle assignable ordering
    def save(self, *args, **kwargs):
        model = self.__class__
        
        #Automatic ordering of list_order property
        if self.list_order is None:
            try:
                last = model.objects.order_by('-list_order')[0]
                self.list_order = last.list_order + 1
            except IndexError:
                self.list_order = 0
        
        return super(Category, self).save(*args, **kwargs)


class Thread(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    subject = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, related_name="threads")

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ('-created_date', )


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    last_edited_date = models.DateTimeField(auto_now=True)
    thread = models.ForeignKey(Thread, related_name="posts")

    sticky = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:100]

    class Meta:
        ordering = ('-sticky', 'created_date', )





