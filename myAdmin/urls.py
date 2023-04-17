from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_user, name='login_user'),
    path('signup', views.signup_user, name='signup_user'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('classes', views.classIndex, name="classIndex"),
    path('classes/delete/<int:id>', views.classDelete, name="classDelete"),
    path('classes/edit/<int:id>', views.classEdit, name="classEdit"),
    path('medium', views.mediumIndex, name="mediumIndex"),
    path('medium/delete/<int:id>', views.mediumDelete, name="mediumDelete"),
    path('medium/edit/<int:id>', views.mediumEdit, name="mediumEdit"),
    path('medium/update', views.mediumUpdate, name="mediumUpdate"),
    path('section', views.sectionIndex, name="sectionIndex"),
    path('section/delete/<int:id>', views.sectionDelete, name="sectionDelete"),
    path('section/edit/<int:id>', views.sectionEdit, name="sectionEdit"),
    path('section/update', views.sectionUpdate, name="sectionUpdate"),
    path('students', views.studentIndex, name="studentIndex"),
    path('teachers', views.teacherIndex, name="teacherIndex"),
]
