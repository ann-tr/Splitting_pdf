from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.say, name = 'hello'),
    path('uploads/',views.uploads , name = 'uploads'),
    path('api_upload/', views.api_upload, name = 'api_upload'),
    
    path('upload_from_url', views.MyModelView.as_view(), name='upload_from_url')
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)