import logging
from typing import List

from celery import shared_task
from django.utils import timezone
from plans.models import PaymentRegistry, Plan

logger = logging.getLogger()


@shared_task()
def create_payment_registries_task():
    now = timezone.now()
    old_plans = Plan.objects.filter(
        is_permanent=False, assigned_date__lte=now
    ).prefetch_related("managers")
    count = len(old_plans)

    payment_registries: List[PaymentRegistry] = []
    for plan in old_plans:
        for manager in plan.managers.all():
            payment_registries.append(
                PaymentRegistry(
                    date=plan.assigned_date,
                    manager=manager,
                    payment=manager.payment,
                    bonus=0,
                )
            )

    payment_registries = PaymentRegistry.objects.bulk_create(
        payment_registries, ignore_conflicts=True
    )
    updated_count = old_plans.update(is_permanent=True)

    return {
        "payments_created": len(payment_registries),
        "permenant_plans": f"{updated_count} из {count}",
    }
