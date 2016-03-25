from django import template
import markdown

register = template.Library()

# Code from http://www.jw.pe/blog/post/using-markdown-django-17/
@register.filter
def markdownify(text):
    return markdown.markdown(text)