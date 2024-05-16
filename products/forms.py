from django.forms import ModelForm
from django import forms
from .models import Review, Books


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'description', 'price', 'category', 'page', 'image', 'book_lang']


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'star_given']


# class BookForm(forms.ModelForm):
#     class Meta:
#         model = Books
#         fields = ['title', 'description', 'price', 'category', 'page', 'image', 'book_lang']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'star_given']