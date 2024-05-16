from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from .forms import AddReviewForm, ReviewForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Books, Review
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView,CreateView, DeleteView
from .forms import BookForm
from django.contrib import messages


class BookListView(View):
    def get(self, request):
        book = Books.objects.all().order_by('-id')
        context = {
            'book': book
        }
        return render(request, 'book_list.html', context=context)


# class BookDetailView(View):
#     def get(self, request, pk):
#         book = Books.objects.get(pk=pk)
#         reviews = Review.objects.filter(book=pk)
#         context = {
#             'book': book,
#             'reviews': reviews
#         }
#         return render(request, 'book_detail.html', context=context)


class BookDetailView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        reviews = Review.objects.filter(book=pk)
        user_has_reviewed = reviews.filter(user=request.user).exists()
        context = {
            'book': book,
            'reviews': reviews,
            'current_user': request.user,
            'user_has_reviewed': user_has_reviewed,
        }
        return render(request, 'book_detail.html', context=context)


class BookUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        form = BookForm(instance=book)
        context = {
            'form': form
        }
        return render(request, 'update.html', context=context)

    def post(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('products:book-detail', pk=pk)
        else:
            context = {
                'form': form
            }
            return render(request, 'update.html', context=context)


class BookCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = BookForm()
        context = {
            'form': form
        }
        return render(request, 'book_create.html', context=context)

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.save()
            return redirect('products:book-list')
        else:
            return render(request, 'book_create.html', {'form': form})


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Books
    template_name = 'book_delete.html'
    success_url = reverse_lazy('products:book-list')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Books, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete book'
        return context


class AddReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        add_review_form = AddReviewForm()
        context = {
            'book': book,
            'add_review_form': add_review_form
        }
        return render(request, 'add_review.html', context=context)

    def post(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        add_review_form = AddReviewForm(request.POST)
        if add_review_form.is_valid():
            review = add_review_form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('products:book-detail', pk=pk)
        else:
            messages.error(request, 'Something went wrong. Please check your input.')
            context = {
                'book': book,
                'add_review_form': add_review_form
            }
            return render(request, 'add_review.html', context=context)


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        is_author = review.user == request.user
        return render(request, 'delete_review.html', {'review': review, 'is_author': is_author})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.user != request.user:
            messages.error(request, "You are not authorized to delete this review.")
            return redirect('products:book-detail', pk=review.book_id)

        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('products:book-detail', pk=review.book_id)


# class DeleteReviewView(DeleteView):
#     model = Review
#     success_url = reverse_lazy('products:book-list')
#
#     def get_success_url(self):
#         # Assuming you have a ForeignKey relationship from Review to Book
#         book_pk = self.object.book.pk
#         return reverse_lazy('products:book-detail', kwargs={'pk': book_pk})


class UpdateReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        form = AddReviewForm(instance=review)
        context = {
            'form': form,
            'review': review
        }
        return render(request, 'update_review.html', context=context)

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        form = AddReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return redirect('products:book-detail', pk=review.book_id)
        else:
            messages.error(request, 'Error updating review. Please check the form.')
        return render(request, 'update_review.html', {'form': form, 'review': review})
