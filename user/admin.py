from django.contrib import admin
from .models import Message


# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ["sender", "recipient", "date", "context"]


admin.site.register(Message, MessageAdmin)
