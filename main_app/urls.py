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
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('uvaclass/', views.UVAClassView.as_view(), name='uvaclass'),
    path('uvaclass/express', views.express, name='express'),
    path('uvaclass/list', views.UVAClassListView.as_view(), name='list'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name="logout"),
    path('documents/', views.document_upload, name='documents'),
    path('documents/<int:pk>', views.document_delete, name='document_delete')
    #path('documents/submit', views.upload_file, name='upload_file')
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)