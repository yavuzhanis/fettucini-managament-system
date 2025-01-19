from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path("admin/", admin.site.urls,name='admin:index'),
    path('', include('menu.urls')),
    path('checkout/', include('checkout.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
