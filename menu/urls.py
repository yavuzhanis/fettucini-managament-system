from django.contrib import admin
from django.urls import path
from menu.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", menu_view, name="menu"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
