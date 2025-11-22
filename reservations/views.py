from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomAuthenticationForm, RoomForm, ReservationForm
from .models import Room, Reservation
from django.utils import timezone
from django.core.mail import send_mail

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'reservations/login.html'

class HomeView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'reservations/home.html'
    context_object_name = 'rooms'

class MyReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/my_reservations.html'
    context_object_name = 'my_reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user, date__gte=timezone.now().date())


class RoomCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'reservations/room_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_staff

class RoomUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'reservations/room_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_staff

class RoomDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Room
    template_name = 'reservations/room_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_staff
    


class ReservationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        # Deny access to staff (admins)
        return not self.request.user.is_staff

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Validation: Check availability
        room = form.cleaned_data['room']
        date = form.cleaned_data['date']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']

        if date < timezone.now().date():
             form.add_error('date', "La fecha no puede ser en el pasado.")
             return self.form_invalid(form)

        # Simple overlap check
        overlapping = Reservation.objects.filter(
            room=room,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlapping:
            form.add_error(None, "La sala ya está reservada en este horario.")
            return self.form_invalid(form)

        response = super().form_valid(form)
        
        # Send Email
        send_mail(
            'Reserva Confirmada',
            f'Tu reserva para la sala {room} el día {date} ha sido confirmada.',
            'sistema@campusucc.edu.co',
            [self.request.user.email],
            fail_silently=True,
        )
        return response

class ReservationCancelView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservations/reservation_confirm_cancel.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        # Allow user to cancel own, or admin to cancel any
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        reservation = self.get_object()
        reason = request.POST.get('cancel_reason', 'No especificado')
        # Send Email (Fail silently if error occurs)
        try:
            send_mail(
                'Reserva Cancelada',
                f'Tu reserva para la sala {reservation.room} el día {reservation.date} ha sido cancelada.\n\nMotivo: {reason}',
                'sistema@campusucc.edu.co',
                [reservation.user.email],
                fail_silently=False, # We handle the exception manually
            )
        except Exception as e:
            # Log the error or just pass, ensuring deletion continues
            print(f"Error sending cancellation email: {e}")

        return super().delete(request, *args, **kwargs)
