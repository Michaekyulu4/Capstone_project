from django.contrib import admin
from .models import Event, Ticket, Payment

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Payment)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'price', 'available_seats', 'organizer')
    search_fields = ('name', 'location', 'organizer__username')
    list_filter = ('date', 'location')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'purchase_date')
    search_fields = ('user__username', 'event__name')
    list_filter = ('status', 'purchase_date')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'amount', 'transaction_id', 'status', 'created_at')
    search_fields = ('transaction_id', 'ticket__event__name')
    list_filter = ('status', 'created_at')