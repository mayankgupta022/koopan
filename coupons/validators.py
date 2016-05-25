from django.http import HttpResponseBadRequest
from coupons.models import *
import json
from dateutil.parser import parse
from datetime import datetime

def createValidator(request):
    response = dict()

    if request.META.get('CONTENT_TYPE') != 'application/json':
        raise ValueError(40000, "ContentType must be application/json", 400)

    data = json.loads(request.body)
    if 'type' not in data or not data['type']:
        raise ValueError(40001, "Type cannot be null", 400)

    if CouponType.objects.filter(coupon_type = data['type']).count() == 0:
        raise ValueError(40002, "Invalid coupon type", 400)

    if data['type'] != "perpetual-use" and ('validupto' not in data or not data['validupto']):
        raise ValueError(40003, "validupto cannot be null for coupon type " + data['type'], 400)

    if 'count' in data and not data['count'].isdigit():
        raise ValueError(40004, "count must be a positive integer", 400)

    if data['type'] == "multi-use" and ('count' not in data or not data['count']):
        raise ValueError(40005, "count cannot be null for coupon type " + data['type'], 400)


def updateValidator(request):
    response = dict()

    if request.META.get('CONTENT_TYPE') != 'application/json':
        raise ValueError(40000, "ContentType must be application/json", 400)

    data = json.loads(request.body)
    if 'id' not in data or not data['id']:
        raise ValueError(40011, "id cannot be null", 400)

    if 'count' in data and not data['count'].isdigit():
        raise ValueError(40012, "count must be a positive integer", 400)

    if 'type' in data and CouponType.objects.filter(coupon_type = data['type']).count == 0:
        raise ValueError(40013, "Invalid CouponType", 400)

    if 'validupto' in data and parse(data['validupto']) < datetime.now():
        raise ValueError(40014, "validupto must be later than current date", 400)


def applyValidator(request):
    response = dict()

    if request.META.get('CONTENT_TYPE') != 'application/json':
        raise ValueError(40000, "ContentType must be application/json", 400)

    data = json.loads(request.body)
    if 'coupon' not in data or not data['coupon']:
        raise ValueError(40021, "coupon cannot be null", 400)

    if 'user_id' not in data or not data['user_id']:
        raise ValueError(40022, "user_id cannot be null", 400)
