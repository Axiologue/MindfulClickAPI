from profile.models import TagPref
from tags.models import EthicsTag, EthicsCategory

from profile.populate import populate_neutral

from django.db.models import Count

def get_company_score(company, user):
    categories = EthicsCategory.objects.prefetch_related('subcategories').all() 

    prefs = user.preferences.select_related('tag_type').values('tag_type__name','preference')
    tags = EthicsTag.objects.filter(company=company).select_related('tag_type').annotate(count=Count('tag_type')).values('tag_type__name','count','tag_type__subcategory_id')

    # We want to make sure there's a preference there for all possible ethics types
    populate_neutral(user)

    scores = [{'tag_type': x['tag_type__name'], 
              'score': x['preference']*y['count'],
              'subcat_id':y['tag_type__subcategory_id']
             } for x in prefs for y in tags if x['tag_type__name'] == y['tag_type__name']]

    # Organize data by categories and subcategories
    totals = []
    for category in categories:
        cat = {"category": category.name, 'subcategories':[], 'score': 0, 'id':category.id}

        for subcat in category.subcategories.all():
            subcategory = {'subcategory': subcat.name,'id':subcat.id}
            subcategory['tags'] =  [{
                                    'tag_type':x['tag_type'],
                                    'score':x['score']
                                    } for x in scores if x['subcat_id']==subcat.id]
            subcategory['score'] = sum(x['score'] for x in subcategory['tags'])

            cat['subcategories'].append(subcategory)
            cat['score'] += subcategory['score']

        totals.append(cat)

    return totals

        

            
