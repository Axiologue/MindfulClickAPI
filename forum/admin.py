from django.contrib import admin
from .models import Post
from .models import Thread
from .models import Category

admin.site.register(Post)
admin.site.register(Thread)
admin.site.register(Category)