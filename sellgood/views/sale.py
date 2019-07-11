from django.shortcuts import HttpResponse
from sellgood.models import Sale
from sellgood.forms import SaleForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt
def create_sale(request):  # Create Sale
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
            return JsonResponse(response_body, status=200)

        # Since body not valid, return errors       
        else:
            return JsonResponse(form.errors, status=422)   

    else:  # If method is different from POST, return body_content
        body_content = {
            'error': 'Method not allowed'
        }
        return JsonResponse(body_content, status=405)


@csrf_exempt
def update_sale(request, id_sale):
    if request.method == 'PUT':   # Check request method
        sale_info = json.loads(request.body)
        form = SaleForm(sale_info)
        if form.is_valid():      # Validate data
            sale_to_update = Sale.objects.get(pk=id_sale)
            sale_to_update.date = form.cleaned_data['date']
            sale_to_update.amount = form.cleaned_data['amount']
            sale_to_update.seller = form.cleaned_data['seller']
            sale_to_update.save()
            body_content = {
                'sale_id': id_sale
            }

             # Return updated_sale id 
            return JsonResponse(response, status=200)
            
        # Since body not valid, return errors    
        else:
            return JsonResponse(form.errors, status=422)

    # If method is different from PUT, return body_content        
    else:
        body_content = {
            'error': 'Method not allowed'
        }
        return JsonResponse(body_content, status=405)