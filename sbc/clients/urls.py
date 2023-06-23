from django.urls import path

from .views import (
    create_client_profile,
    got_success,
    view_forms_list,
    CitizenView,
    CitizenDeleteView,
    CitizenSendEmail,
    search_client_view,
    root,
)
    # about_citizen,

app_name = 'clients'

urlpatterns = [
    path('', root, name="root"),
    path('clients/create/', create_client_profile, name='create_client_profile'),
    path('clients/success/', got_success, name='got_success'),
    path('clients/', view_forms_list, name='view_forms_list'),
    path('clients/<int:id>/', CitizenView.as_view(), name='client_detail'),
    path('clients/<int:id>/edit/', CitizenView.as_view(template_name = "clients/edit_citizen.html"), name='edit_citizen'),
    path('clients/<int:id>/delete/', CitizenDeleteView.as_view(), name='citizen-delete'),
    path('clients/search/', search_client_view, name='search-citizen'),
    path('clients/<int:id>/email/',  CitizenSendEmail.as_view(), name='send_email')


    # path('<int:id>/edit', edit_form, name='edit_form')
    # path('<str:firstname>/', about_citizen, name='about_citizen')

]