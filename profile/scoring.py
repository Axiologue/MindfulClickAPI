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
    categories = EthicsCategory.objects.prefetch_related('subcategories').all() 
    totals = []
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
            total = sum(x['score'] for x in subcategory['tags'])
            subcategory['count'] = sum(x['count'] for x in subcategory['tags'])
            subcategory['score'] = round(total/subcategory['count'],1) if subcategory['count'] else 0

            cat['subcategories'].append(subcategory)
            cat['score'] += subcategory['score'] 
            cat['count'] += subcategory['count']
            has_data += 1 if subcategory['count'] else 0

        cat['score'] = round(cat['score']/has_data,1) if has_data else 0
        totals.append(cat)

    return totals
