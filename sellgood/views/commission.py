import json

from django.http import JsonResponse

from sellgood.models import Sale


def rank(request):
    rank = (Sale.objects
                .all()                
                .order_by('-commission')
                .values('date', 'commission', 'seller__name'))
    if not rank:
        return JsonResponse({'error': 'rank not found'}, status=404)
    return JsonResponse({'rank': list(rank)})


def rank_year(request, year):
    rank = (Sale.objects
                .filter(date__year=year)
                .order_by('-commission')
                .values('date', 'commission', 'seller__name'))
    if not rank:
        return JsonResponse({'error': f'rank of year {year} not found'},
                            status=404)
    return JsonResponse({'rank_year': list(rank)})


def rank_month(request, month):
    rank = (Sale.objects
                .filter(date__month=month)
                .order_by('-commission')
                .values('date', 'commission', 'seller__name'))
    if not rank:
        return JsonResponse({'error': f'rank of month {month} not found'},
                            status=404)
    return JsonResponse({'rank_month': list(rank)})


def rank_year_month(request, year, month):
    rank = (Sale.objects
                .filter(date__year=year, date__month=month)
                .order_by('-commission')
                .values('date', 'commission', 'seller__name'))
    if not rank:
        return JsonResponse(
            {'error': f'rank of year {year} and month {month} not found'}, 
            status=404)
    return JsonResponse({'rank_year_month': list(rank)})
    