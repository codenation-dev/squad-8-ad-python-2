from django.urls import path, re_path

from .views import commission


app_name='sellgood'
urlpatterns = [
    path('commission/rank/', commission.rank, name='rank'),
    re_path(r'commission/rank/(?P<year>\d{4})$', 
            commission.rank_year, 
            name='rank_year'),
    re_path(r'commission/rank/(?P<month>\d{1,2})$', 
            commission.rank_month, 
            name='rank_month'), 
    path('commission/rank/<int:year>/<int:month>', 
         commission.rank_year_month, 
         name='rank_year_month')
]