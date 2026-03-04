import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings'); django.setup()
from service_api.models import ServiceConfig, ServiceFamily

registry_family, _ = ServiceFamily.objects.get_or_create(name='Government Registry Services')

mapping_dict = {
    'Water Connection Request': 'Governance & Intergovernmental Coordination',
    'Refugee Registration': 'Immigration & Border Management',
    'Business Grant Application': 'Trade, Industry & Investment',
    'Cultural Grant': 'Tourism, Heritage & Sports',
    'Environmental Impact Assessment': 'Environmental & Natural Resources',
    'Recruitment & HR Records': 'Governance & Intergovernmental Coordination',
    'Child Protection Case Management': 'Social Protection & Welfare',
    'Executive Briefing Management': 'Governance & Intergovernmental Coordination',
    'Sports Club Registration': 'Tourism, Heritage & Sports',
    'Cabinet Memo Tracking': 'Governance & Intergovernmental Coordination',
    'Youth Fund Application': 'Social Protection & Welfare',
    'Research Permit': 'Education & Skills Development',
    'Student Registration': 'Education & Skills Development',
    'Export Permit': 'Business & Commercial Regulation',
}

for svc in ServiceConfig.objects.filter(service_family__isnull=True):
    if svc.service_name in mapping_dict:
        fam, _ = ServiceFamily.objects.get_or_create(name=mapping_dict[svc.service_name])
        svc.service_family = fam
        svc.save()
    elif svc.service_name.startswith(('Incoming', 'Outgoing', 'File /', 'Archive', 'Registry')):
        svc.service_family = registry_family
        svc.is_public_facing = False
        svc.service_type = 'Internal'
        svc.save()
