import xml.etree.ElementTree as ET
import iso8601
import json
from django.utils.timezone import now as now
from io import StringIO
from django.http import HttpResponse
from .models import Policy,PolicyAuthorization

# Create your views here.

def upload_policy(request):
    success = False
    try:
        user = request.POST.get('external_user_id')
        benifit =  request.POST.get('benefit')
        max_amount =  request.POST.get('total_max_amount')
        currency =  request.POST.get('currency')

        
        if user and benifit and max_amount and currency:
            policy_object = Policy(external_user_id=user,benefit=benifit,
                                    currency=currency,total_max_amount=float(max_amount))
            policy_object.save()
            success = True
    except Exception as e:
        print(e)
        success = False
    if success:
        httpresponse = HttpResponse()
        httpresponse.status_code = 201
        return httpresponse  



