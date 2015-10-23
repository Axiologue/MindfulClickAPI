from profile.models import TagPref
from tags.models import EthicsType

from django.core.exceptions import ObjectDoesNotExist

# Fills in all missing tag preferences for a given user to be neutral
def populate_neutral(user):
    for etype in EthicsType.objects.all():
        try:
            pref = TagPref.objects.get(user=user,tag_type=etype)
        except ObjectDoesNotExist:
            pref = TagPref(user=user,tag_type=etype,preference=0)
            pref.save()
