from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='You Tube',
        description='Project for You Tube',
        default_version='v1',
        terms_of_service='https://javlonbekinomjonovich@gmail.com/',
        contact=openapi.Contact(email='javlonbekinomjonovich@gmail.com', name='Javlonbek', url='javlonbekinomjonovich@gmail.com'),
        license=openapi.License(name='Hech qanaqa litsenziya'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # docExpansion = 'none',
)
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api1/v1/auth/', include('accounts.urls')),
    path('api/v1/content/', include('content.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0, ), name='schema-swagger-ui'),
    path('', schema_view.with_ui('swagger', cache_timeout=0, ), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)