from django.contrib import admin
from .models import Brand, Campaign


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'daily_budget', 'monthly_budget', 'daily_spend', 'monthly_spend')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'is_active', 'start_hour', 'end_hour')
