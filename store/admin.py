from django.contrib import admin
from .models import *


# Register your models here.
class UserBooksAdmin(admin.ModelAdmin):
    """Custom admin class for User Links model."""
    readonly_fields = ('id',)
    list_display = (
        "id",
        "user",
        "title",
        "author",
        "published_date",
        "isbn",
        "category",
        "price"
    )


class UserPurchaseAdmin(admin.ModelAdmin):
    """Custom admin class for User Links model."""
    readonly_fields = ('id',)
    list_display = (
        "id",
        "user",
        "total_amount"
    )


admin.site.register(Book, UserBooksAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Purchase, UserPurchaseAdmin)
admin.site.register(PurchaseItem)
