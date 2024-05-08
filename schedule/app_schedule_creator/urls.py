from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('homepage', views.home, name='home'),
    path('about', views.about, name='about'),
    path('upload', views.upload, name='upload'),
    path('import_csv_to_database', views.import_csv_to_database, name='import_csv_to_database'),
]