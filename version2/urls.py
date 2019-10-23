from django.urls import path
from . import views

# about is the intro page
# home is where the survey actually takes place
urlpatterns = [
    path('', views.home, name='version2-home'),
    path('update/', views.update, name='version2-update'),
]