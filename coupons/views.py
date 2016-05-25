from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
import json
import random
import string
from dateutil.parser import parse
from datetime import datetime
from coupons.validators import *
from coupons.models import *
from django.db import IntegrityError
from django.db.models import Count

def errorHandler(e):
    response = dict()

    if len(e.args) == 3:
        response['errorCode'] = e.args[0]
        response['errorMessage'] = e.args[1]

        if e.args[2] == 400:
            return HttpResponseBadRequest(json.dumps(response),content_type="application/json")

        if e.args[2] == 403:
            return HttpResponseForbidden(json.dumps(response),content_type="application/json")

        if e.args[2] == 404:
            return HttpResponseNotFound(json.dumps(response),content_type="application/json")

    response['errorMessage'] = str(e)
    return HttpResponseBadRequest(json.dumps(response),content_type="application/json")


@require_http_methods(["GET"])
def coupons(request):
    response = dict()

    coupons = Coupon.objects.filter()

    response['coupons'] = [{
        'id': coupon.id,
        'code': coupon.code,
        'count': coupon.count,
        'validupto': str(coupon.validupto) } for coupon in coupons]

    return HttpResponse(json.dumps(response), content_type="application/json")


@require_http_methods(["POST"])
def create(request):
    response = dict()

    try:
        createValidator(request);
        data = json.loads(request.body)

        if 'count' in data and data['type'] == "multi-use" :
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

        coupons = Coupon.objects.filter(pk = data['id'])

        if coupons.count() == 0:
            raise ValueError(40411, "coupon with given id not found", 404)

        coupon = coupons[0]

        history = History.objects.filter(coupon = coupon)

        if 'type' in data:

            if data['type'] == "single-use" and history.count() > 1:
                raise ValueError(40311, "cannot set type to single-use as coupon has already been used more than once", 403)

            if data['type'] == "single-use-per-user" and History.objects.filter(coupon = coupon).values('user_id').annotate(ucount=Count('user_id')).filter(ucount__gt = 0).count() > 0:
                raise ValueError(40312, "cannot set type to single-use-per user as coupon has already been used more than once by same user", 403)

            if data['type'] == "multi-use" and coupon.count == 0 and ('count' not in data or not data['count'].isdigit()):
                raise ValueError(40313, "cannot set type to multi-use as count is not present", 403)

            coupon.type = data['type']

        if 'count' in data:
            if coupon.type == "multi-use" and history.count() > data['count']:
                raise ValueError(40314, "cannot set count to " + data['count'] + " as coupon has already been used more number of times", 403)

            if coupon.type != "multi-use":
                data['count'] = 0

            coupon.count = data['count']

        if 'validupto' in data:
            coupon.validupto = parse(data['validupto'])

        coupon.save()

        response['id'] = coupon.id;
        response['code'] = coupon.code;
        response['coupon_type'] = coupon.coupon_type.coupon_type;
        response['count'] = coupon.count;
        response['validupto'] = str(coupon.validupto);

        return HttpResponse(json.dumps(response), content_type="application/json")

    except ValueError as e:
        return errorHandler(e)


@require_http_methods(["POST"])
def apply(request):
    response = dict()

    try:
        applyValidator(request);
        data = json.loads(request.body)

        coupons = Coupon.objects.filter(code = data['coupon'])

        if coupons.count() == 0:
            raise ValueError(40421, "coupon with given code not found", 404)

        coupon = coupons[0]

        history = History.objects.filter(coupon = coupon)

        if coupon.type == "single-use" and history.count() > 0:
            raise ValueError(40321, "coupon has already been used", 403)

        if coupon.type == "multi-use" and history.count() > coupon.count():
            raise ValueError(40322, "coupon has already been used maximum number of times", 403)

        if coupon.type == "single-use-per-user":
            history_user = History.objects.filter(coupon = coupon, user_id = data['user_id'])

            if history_user.count() > 0:
                raise ValueError(40322, "coupon has already been used by this user", 403)

        History.objects.create(
            coupon = coupon,
            user = data['user_id']
        )

        response['coupon'] = coupon.code
        response['user_id'] = data['user_id']

        return HttpResponse(json.dumps(response), content_type="application/json")

    except ValueError as e:
        return errorHandler(e)
