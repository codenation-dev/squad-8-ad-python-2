from django.shortcuts import HttpResponse
from .models import Sale
from sellgood.forms import SaleForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def create_sale(request): # Create Sale
    if request.method == 'POST':  # Check request method
        sale_info = json.loads(request.body)
        form = SaleForm(sale_info)
        if form.is_valid():   # Body request validation 
            date = form.cleaned_data['date']    
            amount = form.cleaned_data['amount']
            seller = form.cleaned_data['seller']  

            # Create a new sale
            new_sale = Sale.objects.create(     
                    date=date, amount=amount, seller=seller)

            # Body content when form is valid.
            response_body = dict(Seller=new_sale.seller_id, 
                                 comission=float(new_sale.comissions))

            # Since body content is valid, return response_body
            return JsonResponse(response_body)

        # Since body not valid, return errors       
        else:
            return JsonResponse(form.errors)   
                                       
    else:  # If method is different from POST, return body_content
        body_content = {
            'error': 'Method not allowed'
        }
        return JsonResponse(body_content)


@csrf_exempt
def update_sale(request, id_sale):
    sale_upd_info = json.loads(request.body)
    sale_to_update = Sale.objects.filter(pk=id_sale)
    for obj in sale_to_update:
        obj.date = sale_upd_info['date']
        obj.amount = sale_upd_info['amount']
        obj.save()
    response = {
        'sale_id': id_sale
    }

    return HttpResponse(json.dumps(response),content_type='application/json',
                        status=205)