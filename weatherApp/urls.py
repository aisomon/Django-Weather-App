from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name="home" ),
    path('remove/<city_name>',views.city_delete, name="remove_city"),
]