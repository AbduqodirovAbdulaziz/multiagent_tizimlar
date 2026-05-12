"""
URL Configuration - asosiy routing.

Bu fayl barcha URL pattern'larni birlashtiradi va
API versiyalash, admin panel, va static files'ni sozlaydi.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/', include('apps.api.urls')),
    
    # Dashboard
    path('', include('apps.dashboard.urls')),
    
    # Web Apps
    path('patients/', include('apps.patients.urls')),
    path('diagnostics/', include('apps.diagnostics.urls')),
    path('agents/', include('apps.agents.urls')),
    
    # Authentication
    path('accounts/', include('allauth.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Health check
    path('health/', include('apps.core.urls')),
]

# Debug toolbar (faqat development)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Static va media files (faqat development)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin panel customization
admin.site.site_header = "Medical MAS Admin"
admin.site.site_title = "Medical MAS"
admin.site.index_title = "Multiagent Tibbiy Diagnostika Platformasi"
