from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'main_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('editstudent/', views.EditStudentView.as_view(), name='editstudent'),
    path('uvaclass/', views.UVAClassView.as_view(), name='uvaclass'),
    path('uvaclass/addClass', views.addClass, name='addClass'),
    path('uvaclass/list', views.UVAClassListView.as_view(), name='list'),
    path('uvaclass/submitEditedStudent', views.submitEditedStudent, name='submitEditedStudent')
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name="logout"),
]
