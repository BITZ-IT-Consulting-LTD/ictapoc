from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notification_task(user_email, subject, message):
    """
    Background task to send notifications.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, message, from_email, [user_email], fail_silently=False)
        logger.info(f"NOTIFICATION_SENT [To: {user_email}]")
        return True
    except Exception as e:
        logger.error(f"NOTIFICATION_FAILED [To: {user_email}]: {str(e)}")
        return False

@shared_task
def execute_system_step_task(request_id, step_id):
    """
    Offloads synchronous API calls to background Celery workers.
    Ensures the web thread remains responsive.
    """
    from .models import ServiceRequest, WorkflowStep
    from .workflow import WorkflowEngine
    from django.db import transaction

    logger.info(f"CELERY_START [Request: {request_id}, Step: {step_id}]")
    
    try:
        with transaction.atomic():
            service_request = ServiceRequest.objects.get(request_id=request_id)
            step = WorkflowStep.objects.get(id=step_id)
            
            engine = WorkflowEngine(request_id=request_id)
            engine.process_async_api_call(step_id)
            
            logger.info(f"CELERY_SUCCESS [Request: {request_id}, Step: {step_id}]")
            return f"Processed step {step.step_name} for request {request_id}"
            
    except ServiceRequest.DoesNotExist:
        logger.error(f"CELERY_ERROR: Request {request_id} not found.")
    except WorkflowStep.DoesNotExist:
        logger.error(f"CELERY_ERROR: Step {step_id} not found.")
    except Exception as e:
        logger.error(f"CELERY_FAILURE [Request: {request_id}]: {str(e)}")
        raise e
