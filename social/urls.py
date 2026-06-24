from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from social.settings.base import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('home/', include('apps.myapp.urls'))
] + static(STATIC_URL, document_root=STATIC_ROOT)

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
