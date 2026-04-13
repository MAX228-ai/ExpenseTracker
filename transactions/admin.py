from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date', 'description')
    list_filter = ('category', 'date', 'user')
    search_fields = ('description', 'user__username')
    date_hierarchy = 'date'