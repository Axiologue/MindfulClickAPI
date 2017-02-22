from django.db.models import Count, Max

from products.models import Product


DIVISIONS = { 
    "Boys": "Boys' ", "Girls": "Girls' ", "Infant": "Infant's ", 
    "Kids": "Kids' ", "Men": "Men's ", "Women": "Women's ", "Unisex": "Unisex "
}

def run():
    for product in Product.objects.all():
        division = DIVISIONS.get(product.division, '')

        product.name = division + product.name
        product.save()

    duplicates = Product.objects.values('name').annotate(c=Count('id'), max_id=Max('id')).filter(c__gt=1)

    for duplicate in duplicates:
        Product.objects.filter(name=duplicate['name']).exclude(id=duplicate['max_id']).delete()

