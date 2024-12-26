from typing import List

from django.utils import timezone

from celery.utils.log import get_task_logger
from celery import shared_task
from managers.models import Manager
from plans.models import PaymentRegistry, Plan


logger = get_task_logger(__name__)


@shared_task()
def create_payment_registries_task():
    
    now = timezone.now()
    old_plans = Plan.objects.filter(is_permanent=False, assigned_date__lte=now)

    logger.info(f"not permanent plans count: {old_plans.count()}")
    
    managers = Manager.objects.filter(plans__in=old_plans).distinct()
    assigned_dates = old_plans.values_list('assigned_date', flat=True).distinct()

    logger.info(f"managers: {managers}")

    logger.info(f"assigned_dates: {assigned_dates}")

    payment_registries: List[PaymentRegistry] = []
    for assigned_date in assigned_dates: 
        for manager in managers:
            payment_registries.append(
                PaymentRegistry(
                    date=assigned_date,
                    manager=manager,
                    payment=manager.payment,
                    bonus=0,
                )
            )

    logger.info(len(payment_registries))

    PaymentRegistry.objects.bulk_create(payment_registries, ignore_conflicts=True)
    old_plans.update(is_permanent=True)
