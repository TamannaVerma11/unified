from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_user, name='login_user'),
    path('signup', views.signup_user, name='signup_user'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('classes', views.classIndex, name="classIndex"),
    path('medium', views.mediumIndex, name="mediumIndex"),
    path('section', views.sectionIndex, name="sectionIndex"),
    path('classes/delete', views.classDelete, name="classDelete"),
    path('medium/delete/<int:id>', views.mediumDelete, name="mediumDelete"),
    path('section/delete/<int:id>', views.sectionDelete, name="sectionDelete"),
    path('students', views.studentIndex, name="studentIndex"),
    path('teachers', views.teacherIndex, name="teacherIndex"),
]
