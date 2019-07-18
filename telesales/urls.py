from django.contrib import admin
from django.urls import include, path
from django.conf.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sellgood/', include('sellgood.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
