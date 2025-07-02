from celery import shared_task  # type: ignore
from decimal import Decimal
from datetime import datetime
from pytz import timezone  # type: ignore

from .models import Brand, Campaign


@shared_task
def enforce_budget_limits() -> None:
    import logging
    from datetime import datetime
    
    # Set up logging to both console and file
    logger = logging.getLogger('enforce_budget_limits')
    
    brands = Brand.objects.all()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Write to both console and file
    log_message = f"\n=== ENFORCE_BUDGET_LIMITS RUNNING at {timestamp} ==="
    print(log_message)
    
    # Also write to a file so you can see it's working
    with open('budget_logs.txt', 'a') as f:
        f.write(f"{log_message}\n")
    
    for brand in brands:
        message = f"[{brand.name}] daily_spend={brand.daily_spend}, daily_budget={brand.daily_budget}"
        print(message)
        with open('budget_logs.txt', 'a') as f:
            f.write(f"{message}\n")
            
        if brand.daily_spend >= brand.daily_budget or brand.monthly_spend >= brand.monthly_budget:
            deactivate_msg = f"Deactivating campaigns for {brand.name}"
            print(deactivate_msg)
            with open('budget_logs.txt', 'a') as f:
                f.write(f"{deactivate_msg}\n")
            Campaign.objects.filter(brand=brand).update(is_active=False)
        else:
            Campaign.objects.filter(brand=brand).update(is_active=True)
    
    with open('budget_logs.txt', 'a') as f:
        f.write("=== END ===\n\n")


@shared_task
def enforce_dayparting() -> None:
    now_hour = datetime.now(timezone('America/New_York')).hour
    campaigns = Campaign.objects.select_related('brand').all()

    for campaign in campaigns:
        brand = campaign.brand
        budget_exceeded = (
            brand.daily_spend >= brand.daily_budget or
            brand.monthly_spend >= brand.monthly_budget
        )

        # ALWAYS respect budget limits first - if budget exceeded, stay deactivated
        if budget_exceeded:
            campaign.is_active = False
        else:
            # Only check dayparting if budget is NOT exceeded
            allowed = campaign.start_hour <= now_hour < campaign.end_hour
            campaign.is_active = allowed

        campaign.save()


@shared_task
def daily_reset() -> None:
    brands = Brand.objects.all()
    for brand in brands:
        brand.daily_spend = Decimal('0.00')
        brand.save()

    enforce_budget_limits.delay()


@shared_task
def monthly_reset() -> None:
    brands = Brand.objects.all()
    for brand in brands:
        brand.monthly_spend = Decimal('0.00')
        brand.save()

    enforce_budget_limits.delay()
