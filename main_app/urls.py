from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'main_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('editprofile/', views.EditProfileView.as_view(), name='editprofile'),
    path('uvaclass/', views.UVAClassView.as_view(), name='uvaclass'),
    path('uvaclass/addClass', views.addClass, name='addClass'),
    path('uvaclass/list', views.UVAClassListView.as_view(), name='list'),
    path('uvaclass/submitEditedProfile', views.submitEditedProfile, name='submitEditedProfile'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name="logout"),
]
