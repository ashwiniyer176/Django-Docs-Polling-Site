from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:questionID>/', views.detail, name='detail'),
    path('<int:questionID>/results/', views.results, name='results'),
    path('<int:questionID>/vote/', views.vote, name='vote')
]
