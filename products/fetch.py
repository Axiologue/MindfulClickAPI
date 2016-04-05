from .models import Product

from django.core.exceptions import ObjectDoesNotExist

from fuzzywuzzy import fuzz, process

def fuzzy_fetch(queryset, object_string):
    names_list = queryset.values_list('name', flat=True)
    extracted = process.extractOne(object_string,names_list,scorer=fuzz.token_set_ratio)

    # Make sure there's a good enough match
    if extracted[1] > 80:
        obj = queryset.filter(name=extracted[0])[0]
       
        return obj

    else:
        raise ObjectDoesNotExist('No {0} Matches {1}'.format(queryset.model.__name__, object_string))
