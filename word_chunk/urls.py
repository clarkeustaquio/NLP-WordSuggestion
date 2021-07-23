from django.urls import path
from . import views
app_name = 'word_chunk'

urlpatterns = [
    path('', views.chunk, name='chunk')
]
