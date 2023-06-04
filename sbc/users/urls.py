from django.urls import path

from .views import main, login_user, create_user_profile, logout_user

app_name = 'users'


urlpatterns = [
    path('', main, name='main'),
    path('login/', login_user, name='login_user'),
    path('signup/', create_user_profile, name='create_user_profile'),
    path('logout/', logout_user, name='logout_user'),
]
