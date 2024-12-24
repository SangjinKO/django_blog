
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('about_me/', views.about_me),
    path('my_flix/', views.my_flix),
    path('', views.landing),
    path('sitemap/', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),

]
