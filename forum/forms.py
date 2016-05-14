from django import forms
from .models import Post
from .models import Thread
from .models import Category


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class ThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ('subject',)

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)