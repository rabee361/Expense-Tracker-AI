from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('project/admin/', admin.site.urls),
    path('project/' , include('accounts.urls')),
    path('project/charts/' , include('charts.urls'))

]+ static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

