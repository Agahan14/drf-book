from django.contrib import admin
from book.models import (
    Book,
    Genre,
    Author,
    Review,
    FavoriteBook,
)

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(FavoriteBook)
