from django.urls import path
from book.views import (
    BookListView,
    BookDetailView,
    ReviewListCreateView,
    ReviewDetailView,
    FavoritesBookListView,
    AddToFavoritesView,
    RemoveFromFavoritesView,
)

urlpatterns = [
    path('list/', BookListView.as_view(), name='book-list'),
    path('detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('favorites-book-list/', FavoritesBookListView.as_view(), name='favorites-book-list'),
    path('add-to-favorites/<int:book_id>/', AddToFavoritesView.as_view(), name='add-to-favorites'),
    path('remove-from-favorites/<int:book_id>/', RemoveFromFavoritesView.as_view(), name='remove-from-favorites'),
]
