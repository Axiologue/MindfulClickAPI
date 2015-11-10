from profile.models import Preference, Modifier
from tags.models import EthicsType

from django.core.exceptions import ObjectDoesNotExist

# Fills in all missing tag preferences for a given user to 0
def populate_preferences(user):
    _populate_neutral(user, Preference)

# Fills in all missing modifiers for a given answer to 0
def populate_modifiers(answer):
    _populate_neutral(answer, Modifier)

# Generalized function to set new tag_type related objects to 0
def _populate_neutral(obj,model):
    # Check to see if there are any missing Tag Types
    etypes = list(EthicsType.objects.all())
    objs = getattr(obj,model.__name__.lower()+'s').select_related('tag_type').all()

    if len(objs) < len(etypes):
        existing_types = [x.tag_type for x in objs]

        # Remove any Tag Types that already have a value set
        for t in existing_types:
            etypes.remove(t)

        # For the remaining Tag Types, create a model object with the value set to 0
        for t in etypes:
            m = model(tag_type=t)
            setattr(m,obj.__class__.__name__.lower(),obj)
            setattr(m,model.__name__.lower(),0)
            m.save()

# Find New tags and populate with modified tags
def populate_with_answers(user):
    # ensure blank answers are there for every Tag Type
    populate_preferences(user)

    # Get the users preferences
    prefs = user.preferences.all()

    # Get all unapplied modifiers
    modifiers = Modifier.objects.filter(answer__users=user).exclude(users=user)

    # Apply each modifier and mark as applied
    for modifier in modifiers:
        # Get the pref from the list of preferences
        pref = next((x for x in prefs if x.tag_type_id == modifier.tag_type_id), None)
        
        # Apply the modifier
        pref.preference += modifier.modifier
        pref.save()

        # Record the modifier as applied
        modifier.users.add(user)
