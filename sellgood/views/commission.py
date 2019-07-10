import json

from django.http import JsonResponse

from sellgood.models import Sale


def rank(request):
    rank = (Sale.objects
                .all()                
                .order_by('-commission')
                .values('date', 'commission', 'seller__name'))
    return JsonResponse({'rank': list(rank)})


def rank_year(request, year):
    rank = (Sale.objects
                .filter(date__year=year)
                .order_by('-commission')
                .values('date', 'commission', 'seller__name'))
    return JsonResponse({'rank_year': list(rank)})


def rank_month(request, month):
    rank = (Sale.objects
                .filter(date__month=month)
                .order_by('-commission')
                .values('date', 'commission', 'seller__name'))
    return JsonResponse({'rank_month': list(rank)})


def rank_year_month(request, year, month):
    rank = (Sale.objects
                .filter(date__year=year, date__month=month)
                .order_by('-commission')
                .values('date', 'commission', 'seller__name'))
    return JsonResponse({'rank_year_month': list(rank)})
    