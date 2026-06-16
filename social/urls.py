from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from social.settings.base import STATIC_URL, STATIC_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('myapp', include('apps.myapp.urls'))
] + static(STATIC_URL, document_root=STATIC_ROOT)
