from django.urls import path

from user.views import login, register, logout_1

urlpatterns = [
    path('login/', login, name='login' ),
    path('register/', register, name='register' ),
    path('logout/', logout_1, name='logout'),
]