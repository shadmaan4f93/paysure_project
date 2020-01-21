import datetime
from django.db import models
from django.utils.timezone import now as now

# Create your models here.
class Policy(models.Model):
    external_user_id = models.CharField(max_length=255,default=None, blank=False, null=False)
    benefit = models.CharField(max_length=255,default=None, blank=False, null=False)
    currency = models.CharField(max_length=255,default=None, blank=False, null=False)
    total_max_amount = models.FloatField()

    class Meta:
        unique_together = ["external_user_id", "benefit", "currency"]


class PolicyAuthorization(models.Model):
    external_user_id = models.CharField(max_length=255,default=None, blank=False, null=False)
    benefit = models.CharField(max_length=255,default=None, blank=False, null=False)
    currency = models.CharField(max_length=255,default=None, blank=False, null=False)
    amount = models.FloatField()
    timestamp = models.DateTimeField(editable=False,blank=False,null=False)
    payment_status = models.BooleanField(default=False)
    failure_reason = models.CharField(max_length=255,default=None, blank=True, null=True)

    

