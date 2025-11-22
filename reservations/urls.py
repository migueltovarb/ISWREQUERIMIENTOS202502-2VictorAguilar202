from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.HomeView.as_view(), name='home'),
    path('mis-reservas/', views.MyReservationsView.as_view(), name='my_reservations'),
    path('room/add/', views.RoomCreateView.as_view(), name='room_add'),
    path('room/<int:pk>/edit/', views.RoomUpdateView.as_view(), name='room_edit'),
    path('room/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),
    path('reserve/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('reservation/<int:pk>/cancel/', views.ReservationCancelView.as_view(), name='reservation_cancel'),
]
