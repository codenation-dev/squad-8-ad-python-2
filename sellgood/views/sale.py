from sellgood.models import Sale
from rest_framework import generics, viewsets
from sellgood.serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer  

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