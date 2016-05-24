from django.db import models

class CouponType(models.Model):
    coupon_type = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
		return self.coupon_type


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    coupon_type = models.ForeignKey(CouponType)
    count = models.IntegerField(max_length=10, default=0)
    validupto = models.DateTimeField()

    def __unicode__(self):
		return self.code

class History(models.Model):
    coupon = models.ForeignKey(Coupon)
    user_id = models.CharField(max_length=50)

    class Meta:
         verbose_name_plural = "History"
