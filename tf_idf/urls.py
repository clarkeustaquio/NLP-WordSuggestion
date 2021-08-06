from django.urls import path
from . import views

app_name = 'tf_idf'

urlpatterns = [
    path('scrape/', views.scrape, name='scrape')
]
