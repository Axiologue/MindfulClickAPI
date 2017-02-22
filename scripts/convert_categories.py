from products.models import Product, ProductCategory


VALID_CATEGORIES = [
    'Soccer', 'Baseball', 'Basketball', 'Casual', 'Crosstraining', 'Dance', 'Football', 
    'Hiking', 'Running', 'Tennis', 'Track & Field', 'Trail Running', 'Trainers', 'Volleyball', 
    'Walking', 'Wrestling', 'Other'
]


def run():
    main_category, _ = ProductCategory.objects.get_or_create(name="Clothing")
    subcategory, _ = ProductCategory.objects.get_or_create(name="Shoes", parent=main_category)

    athletic, _ = ProductCategory.objects.get_or_create(name="Athletic", parent=subcategory)

    for category in VALID_CATEGORIES:
        ProductCategory.objects.get_or_create(name=category, parent=athletic)

    for product in Product.objects.all():
        try:
            category = ProductCategory.objects.get(name=product.category)
        except:
            category = ProductCategory.objects.get(name="Other")

        product.product_category = category
        product.save()
