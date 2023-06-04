from django.urls import path

from .views import create_client_profile, got_success

app_name = 'clients'

urlpatterns = [

    path('create/', create_client_profile, name='create_client_profile'),
    path('success/', got_success, name='got_success'),

]