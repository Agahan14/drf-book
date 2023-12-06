import django_filters
from book.models import Book


class BookFilter(django_filters.FilterSet):
    genre_name = django_filters.CharFilter(
        field_name='genre__name',
        lookup_expr='iexact',
    )
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='iexact',
    )
    publication_date = django_filters.DateFromToRangeFilter(
        field_name='publication_date',
        label='Publication Date (Between)'
    )

    class Meta:
        model = Book
        fields = [
            'genre_name',
            'author_name',
            'publication_date',
        ]
