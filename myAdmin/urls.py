from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('signup', views.signup_user, name='signup_user'),
    path('add-address', views.add_address, name="add_address"),
    path('add-school', views.add_school, name="add_school"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('classes', views.classIndex, name="classIndex"),
    path('classes/delete/<int:id>', views.classDelete, name="classDelete"),
    path('classes/edit/<int:id>', views.classEdit, name="classEdit"),
    path('class/update', views.classUpdate, name="classUpdate"),
    path('medium', views.mediumIndex, name="mediumIndex"),
    path('medium/delete/<int:id>', views.mediumDelete, name="mediumDelete"),
    path('medium/edit/<int:id>', views.mediumEdit, name="mediumEdit"),
    path('medium/update', views.mediumUpdate, name="mediumUpdate"),
    path('section', views.sectionIndex, name="sectionIndex"),
    path('section/delete/<int:id>', views.sectionDelete, name="sectionDelete"),
    path('section/edit/<int:id>', views.sectionEdit, name="sectionEdit"),
    path('section/update', views.sectionUpdate, name="sectionUpdate"),
    path('category', views.categoryIndex, name="categoryIndex"),
    path('category/delete/<int:id>', views.categoryDelete, name="categoryDelete"),
    path('category/edit/<int:id>', views.categoryEdit, name="categoryEdit"),
    path('category/update', views.categoryUpdate, name="categoryUpdate"),
    path('students', views.studentIndex, name="studentIndex"),
    path('student/delete/<int:id>', views.studentDelete, name="studentDelete"),
    path('student/edit/<int:id>', views.studentEdit, name="studentEdit"),
    path('teachers', views.teacherIndex, name="teacherIndex"),
    path('department', views.departmentIndex, name="departmentIndex"),
    path('designation', views.designationIndex, name="designationIndex"),
]
