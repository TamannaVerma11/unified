from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_user, name='login_user'),
    path('signup', views.signup_user, name='signup_user'),
    path('', views.dashboard, name="dashboard"),
    path('classes', views.classIndex, name="classIndex"),
    path('add-class', views.addClass, name="add_class"),
    path('add-section', views.addSection, name="add_section")
]
