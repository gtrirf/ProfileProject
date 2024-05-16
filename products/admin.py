from django.contrib import admin
from .models import Books, BookAuthor, CategoryBooks, Author, Review, Language


admin.site.register(Books)
admin.site.register(BookAuthor)
admin.site.register(CategoryBooks)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Language)
