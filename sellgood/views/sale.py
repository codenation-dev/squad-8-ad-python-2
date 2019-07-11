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
        sales =  Sale.objects.all().values('id', 'date', 'amount', 'comissions',                                'seller__name', 'seller_id')
        
        return JsonResponse({'sales': list(sales)}, status=200)


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
        try:   # Check if the sale exists
            sale_to_delete = Sale.objects.get(pk=id_sale)
        except:    # Returns an error in JSON format if sale doesn't exist
            return JsonResponse({'error':'sale_id not found'}, status=422)
        else:       # If sale exists, delete.
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


@csrf_exempt
def sale_list_seller(request, id_seller):
    if request.method == 'GET':
        seller_sale = Sale.objects.filter(seller_id=id_seller).values('comissions', 'date', 'amount', 'seller__name', 'seller_id')

        if not seller_sale:        # Return error if seller_id doesn't exist
            return JsonResponse({'error': 'seller_id not found'}, status=422)

        return JsonResponse({'seller_sales': list(seller_sale)})

    else:  # If method is not GET, return body_content
        body_content = {
            'error': 'Method not allowed'
            }
        return JsonResponse(body_content, status=405)


@csrf_exempt
def list_sales_month(request, month):
    if request.method == 'GET':
        sales_month = Sale.objects.filter(date__month=month).values('id', 
                                        'date', 'amount', 'comissions', 'seller__name', 'seller_id')
        if not sales_month:
            return JsonResponse({'error': 'Empty month'})

        return JsonResponse({'sales_month': list(sales_month)})

    else:
        body_content = {
            'error': 'Method not allowed'}
        return JsonResponse(body_content, status=405)


@csrf_exempt
def list_sales_year(request, year):
    if request.method == 'GET':
        sales = list()
        sales_year = Sale.objects.filter(date__year=year)
        if not sales_year:
            return JsonResponse({'error': 'Empty year'})
    
        for obj in sales_year:
            sale = {
                'value': float(obj.amount),
                'date': obj.date.strftime('%m-%Y'),
                'comission': float(obj.comissions),
                'seller_name': obj.seller.name,
                'seller_id': obj.seller_id
            }
            sales.append(sale)

        sales_json = json.dumps(sales)

        return HttpResponse(sales_json, content_type='application/json',
                            status=202)
    else:
        body_content = {
            'error': 'Method not allowed'}
        return JsonResponse(body_content, status=405)

@csrf_exempt
def list_sales_year_month(request, year, month):
    if request.method == 'GET':
        sales = list()
        sales_ym = Sale.objects.filter(date__year=year, date__month=month)
        if not sales_ym:
            return JsonResponse({'error': 'Empty year or empty month'})
    
        for obj in sales_ym:
            sale = {
                'value': float(obj.amount),
                'date': obj.date.strftime('%m-%Y'),
                'comission': float(obj.comissions),
                'seller_name': obj.seller.name,
                'seller_id': obj.seller_id
            }
            sales.append(sale)

        sales_json = json.dumps(sales)

        return HttpResponse(sales_json, content_type='application/json',
                            status=202)
    else:
        body_content = {
            'error': 'Method not allowed'}
        return JsonResponse(body_content, status=405)