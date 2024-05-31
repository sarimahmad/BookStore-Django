from django.contrib import admin
from .models import *


# Register your models here.

class StoreUserAdmin(admin.ModelAdmin):
    """Custom admin class for User Links model."""
    readonly_fields = ('id',)
    list_display = (
        "id",
        "username",
        "email"
    )


admin.site.register(StoreUser, StoreUserAdmin)

