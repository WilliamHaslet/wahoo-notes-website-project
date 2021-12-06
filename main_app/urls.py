from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

#Added for file uploads
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('editprofile/', views.EditProfileView.as_view(), name='editprofile'),
    path('submitEditedProfile/', views.submitEditedProfile, name='submitEditedProfile'),
    path('addClasses/', views.AddClassesView.as_view(), name='addclasses'),
    path('course/<int:pk>/', views.ClassDetailView.as_view(), name='classdetail'),
    path('filterclasses/', views.filterClasses, name='filterclasses'),
    path('addCourse/<int:pk>/', views.addCourse, name="addCourse"),
    path('removeCourse/<int:pk>/', views.removeCourse, name="removeCourse"),
    path('listClasses/', views.ListClassesView.as_view(), name='listclasses'),
    path('assignments/', views.AssignmentsView.as_view(), name='assignments'),
    path('removeAssignment/<int:pk>/', views.removeAssignment, name="removeAssignment"),
    path('addAssignment/', views.addAssignment, name="addAssignment"),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('studentSearch', views.studentSearchView, name="studentSearch"),
    path('documents/', views.document_list, name='documents'),
    path('documents/upload', views.document_upload, name='document_upload'),
    path('documents/<int:pk>', views.document_delete, name='document_delete')
]
