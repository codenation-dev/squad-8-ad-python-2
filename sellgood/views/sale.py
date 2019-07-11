from django.shortcuts import HttpResponse
from .models import Sale
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def create_sale(request):
    sale_info = json.loads(request.body)
    new_sale = Sale.objects.create(**sale_info)
    response_body = {
        'Seller': new_sale.seller_id,
        'comission': float(new_sale.comissions)
    }
        
    return HttpResponse(
                json.dumps(response_body),
                content_type='application/json',
                status=200)


