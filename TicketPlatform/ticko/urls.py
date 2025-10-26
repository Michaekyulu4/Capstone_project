from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
   
    path('events/', views.event_list_view, name='event_list'),
    path('events/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('events/create/', views.create_event_view, name='create_event'),

    path('events/<int:event_id>/book/', views.book_ticket_view, name='book_ticket'),
    path('my-tickets/', views.my_tickets_view, name='my_tickets'),
    path('', views.home_view, name='home'),
]
