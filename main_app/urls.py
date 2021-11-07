from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'main_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('editprofile/', views.EditProfileView.as_view(), name='editprofile'),
    path('addClasses/', views.AddClassesView.as_view(), name='addclasses'),
    path('addClasses/<int:pk>/', views.ClassDetailView.as_view(), name='classdetail'),
    path('listClasses/', views.ListClassesView.as_view(), name='listclasses'),
    path('submitEditedProfile/', views.submitEditedProfile, name='submitEditedProfile'),
    path('addCourse/<int:pk>/', views.addCourse, name="addCourse"),
    path('removeCourse/<int:pk>/', views.removeCourse, name="removeCourse"),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('classTest', views.classTestView, name="classTest"),
]
