from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_user, name='login_user'),
    path('signup', views.signup_user, name='signup_user'),
    path('', views.dashboard, name="dashboard"),
    path('classes', views.classIndex, name="classIndex"),
    path('classes/delete', views.classDelete, name="classDelete"),
    path('students', views.studentIndex, name="studentIndex"),
    path('teachers', views.teacherIndex, name="teacherIndex"),
]
