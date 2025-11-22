from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Room, Reservation

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

from django.utils.html import format_html

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'location', 'image_preview')
    search_fields = ('name', 'location')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "Sin Imagen"
    image_preview.short_description = 'Vista Previa'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'date', 'start_time', 'end_time')
    list_filter = ('date', 'room')
    search_fields = ('user__email', 'room__name')
