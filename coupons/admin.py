from django.contrib import admin
from coupons.models import *

@admin.register(CouponType)
class CouponTypeAdmin(admin.ModelAdmin):
    list_display = ['coupon_type']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'coupon_type', 'count', 'validupto')
    search_fields = ['code']
    list_filter = ['coupon_type']

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user_id')
    search_fields = ('coupon', 'user_id')
