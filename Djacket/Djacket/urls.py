from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include('product.urls')),   # for /api/v1/latest-products/
    path('product/', include('product.urls')),  # for /product/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
