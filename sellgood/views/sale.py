from django.shortcuts import HttpResponse
from sellgood.models import Sale
from sellgood.forms import SaleForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt
def create_read_sale(request):  # Create Sale
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

     elif request.method == 'GET':  # If request method == GET Return Sale List
        sales_list = list()

        for sale in Sale.objects.all():
            sale_json = {
                'date': sale.date.strftime('%m-%Y'),
                'amount': float(sale.amount),
                'seller': sale.seller.name,
                'seller_id': sale.seller_id
            }
            sales_list.append(sale_json)
        sales_json = json.dumps(sales_list)

        return HttpResponse(sales_json, 
                            content_type = 'application/json', status=200)


    else:  # If method is not POST OR GET, return body_content
        body_content = {
            'error': 'Method not allowed'
        }
        return JsonResponse(body_content, status=405)


@csrf_exempt
def update_delete_sale(request, id_sale):
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

        # If request method == DELETE; Delete Sale
        elif request.method == 'DELETE': 
                sale_to_delete = Sale.objects.get(pk=id_sale)
                sale_to_delete.delete()

                response_body = {
                    'id_sale_deleted': id_sale
                    }

                return JsonResponse(response_body, status=200)

    # If method is not PUT or DELETE, return body_content        
    else:
        body_content = {
            'error': 'Method not allowed'
        }
        return JsonResponse(body_content, status=405)