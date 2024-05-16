from django.urls import path
from .views import (
    BookListView, BookDetailView, BookUpdateView,
    BookCreateView, AddReviewView, BookDeleteView,
    DeleteReviewView, UpdateReviewView)


app_name = 'products'

urlpatterns = [
    path('book-list/',  BookListView.as_view(), name='book-list'),
    path('book-detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book-update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    path('book-create/', BookCreateView.as_view(), name='book-create'),
    path('book-delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
    path('add-review/<int:pk>/', AddReviewView.as_view(), name='add-review'),
    path('update-review/<int:pk>/', UpdateReviewView.as_view(), name='update-review'),
    path('delete-review/<int:pk>/', DeleteReviewView.as_view(), name='delete-review')
]