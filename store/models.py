from django.db import models
from django.utils import timezone
import uuid
from accounts.models import StoreUser


# Create your models here.


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name="user_authors", blank=True, null=True)
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} id {self.id}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name="user_categories", blank=True, null=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} id {self.id}"


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name="user_books", blank=True, null=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="book_category", blank=True,
                                 null=True)
    price = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} id {self.id}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE, related_name="user_carts", blank=True, null=True)
    books = models.ManyToManyField(Book, through='CartItem', related_name='books_carts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}'s Cart, id {self.id}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,  related_name="cart_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_in_cart_items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.book.title} in {self.cart.user}'s Cart"


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name="user_purchases", blank=True, null=True)
    books = models.ManyToManyField(Book, through='PurchaseItem', related_name='books_purchases')
    total_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Purchase {self.id} by {self.user}"


class PurchaseItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.book.title} in Purchase {self.purchase.id}"
