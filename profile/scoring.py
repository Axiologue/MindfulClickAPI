from profile.models import Preference
from tags.models import EthicsTag, EthicsCategory

from profile.populate import populate_preferences

from django.db.models import Count

# Returns scores, with associated tag information, on any given company
def get_company_score(company, user):

    tags = EthicsTag.objects.filter(company=company,product=None).select_related('tag_type').annotate(count=Count('tag_type')).values('tag_type__name','count','tag_type__subcategory_id')
    
    return compute_score(tags, user)


# Retuns personalized score, along with article/tag counts
def get_product_score(product,user):
    tags = EthicsTag.objects.filter(product=product).select_related('tag_type').annotate(count=Count('tag_type')).values('tag_type__name','count','tag_type__subcategory_id')

    return compute_score(tags, user)

# gets score for both a product AND its parent company (without double counting)
def get_combined_score(product, user):

    tags = list(EthicsTag.objects.filter(product=product).select_related('tag_type').annotate(count=Count('tag_type')).values('tag_type__name','count','tag_type__subcategory_id')) + list(EthicsTag.objects.filter(company=product.company, product=None).select_related('tag_type').annotate(count=Count('tag_type')).values('tag_type__name','count','tag_type__subcategory_id'))

    return compute_score(tags, user)

def compute_score(tags,user):
    categories = EthicsCategory.objects.prefetch_related('subcategories').all() 
    prefs = user.preferences.select_related('tag_type').values('tag_type__name','preference')

    # We want to make sure there's a preference there for all possible ethics types
    populate_preferences(user)
   
    # compute individual tag scores, based on preferences
    scores = [{'tag_type': x['tag_type__name'], 
              'score': x['preference'],
              'subcat_id':y['tag_type__subcategory_id'],
              'count': y['count'],
             } for x in prefs for y in tags if x['tag_type__name'] == y['tag_type__name']]

    # Organize data by categories and subcategories
    parsed_categories = []
    for category in categories:
        cat = {"category": category.name, 
               'subcategories':[],
               'score': 0,
               'id':category.id,
               'count':0}

        has_data = 0
        for subcat in category.subcategories.all():
            subcategory = {'subcategory': subcat.name,'id':subcat.id}
            subcategory['tags'] =  [{
                                    'tag_type':x['tag_type'],
                                    'score':x['score'],
                                    'count':x['count']
                                    } for x in scores if x['subcat_id']==subcat.id]
            subcategory['count'] = sum(x['count'] for x in subcategory['tags'])
            subcategory['score'] = weighted_average([x['score'] for x in subcategory['tags']])

            cat['subcategories'].append(subcategory)
            cat['count'] += subcategory['count']

        cat['score'] = weighted_average([sub['score'] for sub in cat['subcategories']]) 
        parsed_categories.append(cat)

    # Compute the overall scores
    overall = {
            'overall': weighted_average([cat['score'] for cat in parsed_categories]),
            'categories': parsed_categories 
    }
 
    return overall 

# Calculate weighted average used in scoring
def weighted_average(nums):
    total = sum(abs(x) for x in nums)
    
    weighted = sum((x * abs(x))/total for x in nums) if total > 0 else 0

    return round(weighted,1)
    
