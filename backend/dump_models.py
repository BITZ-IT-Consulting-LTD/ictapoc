import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from service_api.models import MDA, ServiceConfig, WorkflowStep
for model in [MDA, ServiceConfig, WorkflowStep]:
    print(f"\n{model.__name__} Fields:")
    for f in model._meta.get_fields():
        print(f" - {f.name}: {f.__class__.__name__}")
