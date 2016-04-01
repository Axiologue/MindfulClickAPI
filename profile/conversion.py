import json
import os

from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Preference
from tags.models import EthicsType

User = get_user_model()


def convert_preferences():
    raw = open(os.path.join(settings.BASE_DIR, 'preferences.json')).read()
    pref_data = json.loads(raw)

    for pref in pref_data:
        user = User.objects.get(id=pref['fields']['user'])
        tag_type = EthicsType.objects.get(id=pref['fields']['tag_type'])
        
        preference, _ = Preference.objects.get_or_create(tag_type=tag_type, preference=pref['fields']['preference'])

        user.preferences.add(preference)
