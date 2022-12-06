from django.urls import path
from . import views

urlpatterns = [
        path('signup', views.RegistView.as_view(), name='signup'),
        path('login', views.LoginView.as_view(), name='login'),
        path('profile', views.PofileView.as_view(), name='profile'),
        path("update_password", views.UpdatePasswordView.as_view(), name="update_password"),

]
