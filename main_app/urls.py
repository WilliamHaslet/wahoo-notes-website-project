from django.urls import path

from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('deepthoughts/', views.DeepthoughtView.as_view(), name='deepthoughts'),
    path('deepthoughts/express', views.express, name='express'),
    path('deepthoughts/list', views.DeepthoughtListView.as_view(), name='list'),
]
