from profile.models import TagPref
from tags.models import EthicsType

from django.core.exceptions import ObjectDoesNotExist

# Fills in all missing tag preferences for a given user to be neutral
def populate_neutral(user):
    # Check to see if there are any missing Tag Types
    etypes = list(EthicsType.objects.all())
    prefs = user.preferences.select_related('tag_type').all()

    if len(prefs) < len(etypes):
        existing_types = [x.tag_type for x in prefs] 

        # Remove EthicsTypes that already have preferences from the list
        for t in existing_types:
           etypes.remove(t)

        # Create new TagPref for missing EthicsTypes
        for t in etypes:
            TagPref(user=user,preference=0,tag_type=t).save()

