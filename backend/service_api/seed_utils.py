import os
import json
from django.conf import settings
from service_api.models import MDA

def get_canonical_mdas():
    """
    Loads the canonical MDA registry from the fixtures directory.
    """
    fixture_path = os.path.join(settings.BASE_DIR, 'service_api', 'fixtures', 'canonical_mdas.json')
    if not os.path.exists(fixture_path):
        return []
    with open(fixture_path, 'r') as f:
        return json.load(f)

def get_or_create_mda(name=None, code=None, defaults=None):
    """
    Idempotent helper to get or create an MDA using canonical mapping.
    Priority is given to the 'code'.
    """
    if not defaults:
        defaults = {}
    
    # Try looking up in canonical list if only name is provided
    if name and not code:
        canonical_list = get_canonical_mdas()
        for item in canonical_list:
            if item['name'].lower() == name.lower():
                code = item['code']
                # Merge canonical defaults if not provided
                if 'description' not in defaults: defaults['description'] = item.get('description')
                if 'head_of_mda' not in defaults: defaults['head_of_mda'] = item.get('head')
                break

    if not code:
        # Fallback to a Slug-like code if still none
        code = name.replace(' ', '_').upper()[:50] if name else 'UNKNOWN'

    mda, created = MDA.objects.get_or_create(
        code=code,
        defaults={
            'name': name or code,
            **defaults
        }
    )
    
    if not created and name and mda.name != name:
        # Update name if it has changed in the seed but code matches
        mda.name = name
        mda.save()
        
    return mda, created
