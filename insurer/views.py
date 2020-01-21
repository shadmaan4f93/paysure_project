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

def process_payment(request):
    
    return_value={
        "authorized":None,
        "reason":None
    }

    if not request.POST:
        xml_content = request.body.decode()
        tree = ET.iterparse(StringIO(xml_content))
        root = {}
        for _, el in tree:
            prefix, has_namespace, postfix = el.tag.partition('}')
            root[prefix] = el.text
        xml_data = root

        # mapping xml elements parsed 
        user_id = xml_data['Token']
        benifit = xml_data['MCC_Desc']
        max_amount = xml_data['Bill_Amt']
        currency   = xml_data['Txn_Ctry']


    else:
        user_id = request.POST.get('external_user_id')
        benifit =  request.POST.get('benefit')
        max_amount =  request.POST.get('amount')
        currency =  request.POST.get('currency')
    


    try:
        if user_id and benifit and max_amount and currency:
            this_user_policy = Policy.objects.filter(external_user_id=user_id).first()
            if this_user_policy:
                policy_amount = this_user_policy.total_max_amount
                policy_benifit = this_user_policy.benefit
                policy_currency = this_user_policy.currency

                if policy_amount >= float(max_amount):
                    if policy_benifit == benifit:
                        if policy_currency == currency:
                            this_user_policy.total_max_amount = policy_amount-float(max_amount)
                            this_user_policy.save()

                            return_value["authorized"] = True
                        else:
                            return_value["authorized"] = False
                            return_value["reason"] = "POLICY_NOT_FOUND"

                    else:
                        return_value["authorized"] = False
                        return_value["reason"] = "POLICY_NOT_FOUND"

                else:
                    return_value["authorized"] = False
                    return_value["reason"] = "POLICY_AMOUNT_EXCEEDED"

            else:
                return_value["authorized"] = False
                return_value["reason"] = "POLICY_NOT_FOUND"
            
            

        else:
            return_value["authorized"] = False
            return_value["reason"] = "Bad Request"

        timestamp = iso8601.parse_date(now().isoformat())
        authorization_obj = PolicyAuthorization(external_user_id=user_id,benefit=benifit,currency=currency,
                                                amount = float(max_amount),
                                                timestamp = timestamp,
                                                payment_status = return_value["authorized"],
                                                failure_reason = return_value["reason"]                         
                                            )

        authorization_obj.save()        

    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(return_value), content_type="application/json")



