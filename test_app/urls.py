from django.urls import path
from test_app.views import Logout, Login
from test_app import views

app_name = 'test_app'

urlpatterns = [
    path('', views.users_profile, name='users'),
    path('profile/', views.user_profile, name='user'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-form/', views.change_password, name='change_password'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]