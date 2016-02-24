from refData.models import Product

from django.core.exceptions import ObjectDoesNotExist

from fuzzywuzzy import fuzz, process

def product_fetch(product_string):
    products = Product.objects.all()
    names_list = [x.name for x in products]
    product_string = process.extractOne(product_string,names_list,scorer=fuzz.token_set_ratio)

    # Make sure there's a good enough match
    if product_string[1] > 80:
        product = Product.objects.filter(name=product_string[0])[0]
       
        return product

    else:
        raise ObjectDoesNotExist('No Product Matches that Name')
