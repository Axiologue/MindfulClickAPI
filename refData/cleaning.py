from refData.models import Product

from django.db.utils import IntegrityError

# Function to replace incorrect categories with proper ones
def cat_replace(source,replacement):
    for p in Product.objects.filter(category=source):
        try:
            p.category = replacement
            p.save()
        except IntegrityError:
            p.delete()

def cat_strip(phrase):
    for p in Product.objects.filter(category__icontains=phrase):
        try:
            p.category = p.category.replace(phrase,"")
            p.save()
        except IntegrityError:
            p.delete()

