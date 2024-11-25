from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # primary homepage
    path('', views.home_view, name='home'),
    
    # default login and logout views
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # booking creation and deletion views
    path('create-booking/', views.create_booking_view, name='create_booking'),
    path('delete-booking/<int:booking_id>/', views.delete_booking_view, name='delete_booking'),
]
