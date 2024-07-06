from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path('start/', views.start_simulator, name='start_simulator'),
    path('stop/', views.stop_simulator, name='stop_simulator'),

    path('run_tests/', views.run_tests_view, name='run_tests'),
]
