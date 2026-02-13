from django.db import transaction
from service_api.models import (
    ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain, MDA, 
    ServiceRequest, AuditLog, GovernmentFile, InterDepartmentalMemo,
    OfficialLetter, CorrespondenceAction
)

def deep_wipe():
    print("--- STARTING DEEP WIPE (DOCKER) ---")
    with transaction.atomic():
        print("Deleting Correspondence Actions...")
        CorrespondenceAction.objects.all().delete()
        
        print("Deleting Official Letters...")
        OfficialLetter.objects.all().delete()
        
        print("Deleting InterDepartmental Memos...")
        InterDepartmentalMemo.objects.all().delete()
        
        print("Deleting Government Files...")
        GovernmentFile.objects.all().delete()
        
        print("Deleting Audit Logs...")
        AuditLog.objects.all().delete()
        
        print("Deleting Service Requests...")
        ServiceRequest.objects.all().delete()
        
        print("Deleting Workflow Steps...")
        WorkflowStep.objects.all().delete()
        
        print("Deleting Service Configs...")
        ServiceConfig.objects.all().delete()
        
        print("Deleting Service Categories...")
        ServiceCategory.objects.all().delete()
        
        print("Deleting Service Domains...")
        ServiceDomain.objects.all().delete()
        
        print("Deleting MDAs...")
        MDA.objects.all().delete()
        
    print("--- DEEP WIPE COMPLETE ---")

if __name__ == "__main__":
    deep_wipe()
