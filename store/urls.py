from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, CategoryViewSet, BookViewSet, CartViewSet, PurchaseViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'books', BookViewSet, basename='books')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'purchases', PurchaseViewSet, basename='purchases')

urlpatterns = [
    path('', include(router.urls)),
]