from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include

def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]