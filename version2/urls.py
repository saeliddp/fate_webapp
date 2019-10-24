from django.urls import path
from . import views

# home is where the survey actually takes place
# update refreshes the home page and sends data to server
urlpatterns = [
    path('', views.home, name='version2-home'),
    path('update/', views.update, name='version2-update'),
]