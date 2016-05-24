from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
import json
import random
import string
from dateutil.parser import parse
from datetime import datetime
from coupons.validators import *
from coupons.models import *
from django.db import IntegrityError

def errorHandler(e):
    response = dict()

    if len(e.args) == 3 and e.args[2] == 400:
        response['errorCode'] = e.args[0]
        response['errorMessage'] = e.args[1]
        return HttpResponseBadRequest(json.dumps(response),content_type="application/json")

    response['errorMessage'] = str(e)
    return HttpResponseBadRequest(json.dumps(response),content_type="application/json")


@require_http_methods(["POST"])
def create(request):
    response = dict()

    try:
        createValidator(request);
        data = json.loads(request.body)

        if 'count' in data:
            count = data['count']
        else:
            count = 0

        unique_code_generated = False

        while unique_code_generated is False:
            try:
                unique_code_generated = True
                coupon_code = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))

                coupon = Coupon.objects.create(
                    code = coupon_code,
                    coupon_type = CouponType.objects.filter(coupon_type = data['type'])[0],
                    count = count,
                    validupto = parse(data['validupto'])
                )
            except IntegrityError as e:
                unique_code_generated = False

        response['id'] = coupon.id;
        response['code'] = coupon.code;
        response['coupon_type'] = coupon.coupon_type.coupon_type;
        response['count'] = coupon.count;
        response['validupto'] = str(coupon.validupto);

        return HttpResponse(json.dumps(response), content_type="application/json")

    except ValueError as e:
        return errorHandler(e)


@require_http_methods(["POST"])
def update(request):
    response = dict()

    try:
        updateValidator(request);
        data = json.loads(request.body)


        return HttpResponse(json.dumps(response), content_type="application/json")

    except ValueError as e:
        return errorHandler(e)


@require_http_methods(["POST"])
def apply(request):
    response = dict()

    try:
        applyValidator(request);
        data = json.loads(request.body)


        return HttpResponse(json.dumps(response), content_type="application/json")

    except ValueError as e:
        return errorHandler(e)
