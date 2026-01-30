from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static   # ✅ THIS WAS MISSING

urlpatterns = [
   path('secure-camx-admin-9f3k/', admin.site.urls),  # ✅ secure admin
    path('', include('shop.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)