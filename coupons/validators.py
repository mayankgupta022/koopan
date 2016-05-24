from django.http import HttpResponseBadRequest
from coupons.models import *
import json

def createValidator(request):
    response = dict()

    if request.META.get('CONTENT_TYPE') != 'application/json':
        raise ValueError(4001, "ContentType must be application/json", 400)

    data = json.loads(request.body)
    if 'type' not in data or not data['type']:
        raise ValueError(4002, "Type cannot be null", 400)

    if CouponType.objects.filter(coupon_type = data['type']).count() == 0:
        raise ValueError(4003, "Invalid coupon type", 400)

    if data['type'] != "perpetual-use" and ('validupto' not in data or not data['validupto']):
        raise ValueError(4004, "validupto cannot be null for coupon type " + data['type'], 400)

    if data['type'] == "multi-use" and ('count' not in data or not data['count']):
        raise ValueError(4005, "count cannot be null for coupon type " + data['type'], 400)
