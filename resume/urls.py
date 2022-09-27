from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new/', views.makenew),
    path('newSubmit/', views.savenew),
    path('view/<str:username>/<int:resume>', views.show),
]
