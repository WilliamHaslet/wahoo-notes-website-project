from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from django.contrib.auth.views import LoginView

app_name = 'main_app'

urlpatterns = [
    path('', views.login, name='login'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('uvaclass/', views.UVAClassView.as_view(), name='uvaclass'),
    path('uvaclass/express', views.express, name='express'),
    path('uvaclass/list', views.UVAClassListView.as_view(), name='list'),
    path('accounts/', include('allauth.urls')),
    path('calendar/', TemplateView.as_view(template_name='main_app/calendar.html'), name='index'),
    path('logout', LogoutView.as_view(), name="logout"),
]
