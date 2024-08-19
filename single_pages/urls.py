
from django.urls import path
from . import views

urlpatterns = [
    path('about_me/', views.about_me),
    path('my_flix/', views.my_flix),
    path('', views.landing)
]
