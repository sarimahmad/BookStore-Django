from rest_framework import serializers
from .models import Author, Category, Book, Cart, CartItem, PurchaseItem, Purchase
from django.db import transaction
from .tasks import send_purchase_email


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['user']
        author = Author.objects.create(user=user, **validated_data)
        return author

    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['user']
        category = Category.objects.create(user=user, **validated_data)
        return category

    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        # validated_data['user'] = self.context['user']
        # print("Validated dat", validated_data)
        # return super().create(validated_data)
        user = self.context['user']
        book = Book.objects.create(user=user, **validated_data)
        return book

    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('id',)


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    book_id = serializers.UUIDField(write_only=True, required=False)
    quantity = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Cart
        fields = ['cart_items', 'book_id', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ('id',)

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['user']
        book_id = validated_data.pop('book_id', None)
        quantity = validated_data.pop('quantity', 1)
        cart, created = Cart.objects.get_or_create(user=user)
        if book_id:
            book = Book.objects.get(id=book_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
            cart_item.quantity = quantity
            cart_item.save()

        return cart

    def update(self, instance, validated_data):
        book_id = validated_data.pop('book_id', None)
        quantity = validated_data.pop('quantity', 1)

        if book_id:
            book = Book.objects.get(id=book_id)
            cart_item, created = CartItem.objects.get_or_create(cart=instance, book=book)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

        return super().update(instance, validated_data)


class PurchaseItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = PurchaseItem
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(source='purchase_items', many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = ['id', 'user', 'total_amount', 'created_at', 'items']

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['user']
        cart = user.user_carts
        if cart.cart_items.count() == 0:
            raise serializers.ValidationError({"message": "Cart is empty"})

        purchase = Purchase.objects.create(user=user, total_amount=validated_data['total_amount'])
        for cart_item in cart.cart_items.all():
            PurchaseItem.objects.create(
                purchase=purchase,
                book=cart_item.book,
                quantity=cart_item.quantity,
                price=cart_item.book.price
            )
        cart.cart_items.all().delete()
        transaction.on_commit(lambda: send_purchase_email.delay(purchase.id))
        return purchase
