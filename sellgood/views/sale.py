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
            new_sale_info = Sale.objects.filter(pk=new_sale.id).values('id',                                                'seller', 'amount')

            # Since body content is valid, return response_body
            return JsonResponse({'New Sale Info': list(new_sale_info)},                             status=200)

        # Since body not valid, return errors       
        else:
            return JsonResponse(form.errors, status=422)   

    elif request.method == 'GET':  # If request method == GET Return Sale List
        sales =  Sale.objects.all().values('id', 'date', 'amount',                                                  'seller__name', 'seller_id')
        if not sales:
            return JsonResponse({'error': "no sales recorded" }, status=404)

        return JsonResponse({'sales': list(sales)}, status=200)

    else:  # If method is not POST OR GET, return body_content
        return JsonResponse({'error': 'Method not allowed'}, status=405)


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

            sale_info = Sale.objects.filter(pk=sale_to_update.id).values('id')
             # Return updated_sale id 
            return JsonResponse({'id_sale_updated': list(sale_info)},                               status=200)
            
        # Since body not valid, return errors    
        else:
            return JsonResponse(form.errors, status=422)

    # If request method == DELETE; Delete Sale
    elif request.method == 'DELETE': 
        try:   # Check if the sale exists
            sale_to_delete = Sale.objects.get(pk=id_sale)
        except Sale.DoesNotExist:    # Returns an error if sale doesn't exist
            return JsonResponse({'error':'sale_id not found'}, status=404)
        else:       # If sale exists, delete.
            sale_to_delete.delete()
            return JsonResponse({'id_sale_deleted': id_sale}, status=200)

    # If method is not PUT or DELETE, return body_content        
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def sale_list_seller(request, id_seller):
    if request.method == 'GET':
        seller_sale = Sale.objects.filter(seller_id=id_seller).values('id',                                                         'date', 'amount',                                            'seller__name', 'seller_id')

        if not seller_sale:        # Return error if seller_id doesn't exist
            return JsonResponse({'error': 'seller_id not found'}, status=404)

        return JsonResponse({'seller_sales': list(seller_sale)}, status=200)

    else:  # If method is not GET, return body_content
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def list_sales_month(request, month):
    if request.method == 'GET':
        sales_month = Sale.objects.filter(date__month=month).values('id', 
                                        'date', 'amount', 'seller__name',                           'seller_id')
        if not sales_month:
            return JsonResponse({'error': 'Empty month'}, status=404)

        return JsonResponse({'sales_month': list(sales_month)}, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def list_sales_year(request, year):
    if request.method == 'GET':
        sales_year = Sale.objects.filter(date__year=year).values('id', 
                                        'date', 'amount', 'seller__name',                       'seller_id')
        if not sales_year:
            return JsonResponse({'error': 'Empty year'}, status=404)
    
        return JsonResponse({'sales_year': list(sales_year)}, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def list_sales_year_month(request, year, month):
    if request.method == 'GET':
        sales_ym = Sale.objects.filter(date__year=year, 
                        date__month=month).values('id', 'date', 'amount',                               'seller__name', 'seller_id')
        if not sales_ym:
            return JsonResponse({'error': 'Empty year or empty month'},                             status=404)
            
        return JsonResponse({'sale_year_month': list(sales_ym)}, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)