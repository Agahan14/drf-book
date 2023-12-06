from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import (
    generics,
    permissions,
    status,
)
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from book.models import (
    Book,
    Review,
    FavoriteBook,
)
from book.serializers import (
    BookSerializer,
    BookDetailSerializer,
    ReviewSerializer,
)
from book.filters import BookFilter
from book.pagination import CustomPagination


class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related('genre', 'author').all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_class = BookFilter

    @swagger_auto_schema(
        tags=['Books'],
        manual_parameters=[
            openapi.Parameter('page', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Номер страницы для постраничных результатов.'),
            openapi.Parameter('limit', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Количество результатов, возвращаемых на страницу.'),
            openapi.Parameter('publication_date_after', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              format=openapi.FORMAT_DATE,
                              description='Дата публикации после (в формате YYYY-MM-DD).'),
            openapi.Parameter('publication_date_before', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              format=openapi.FORMAT_DATE,
                              description='Дата публикации до (в формате YYYY-MM-DD).')
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related('genre', 'author').all()
    serializer_class = BookDetailSerializer

    @swagger_auto_schema(
        tags=['Books'],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор новости",
                required=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=['Review'],
        manual_parameters=[
            openapi.Parameter('page', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Номер страницы для постраничных результатов.'),
            openapi.Parameter('limit', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Количество результатов, возвращаемых на страницу.')
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Review'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Review'],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор книги",
                required=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Review'],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор книги",
                required=True,
            ),
        ],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Review'],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор книги",
                required=True,
            ),
        ]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Review'],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор книги",
                required=True,
            ),
        ]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class AddToFavoritesView(generics.CreateAPIView):
    queryset = FavoriteBook.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Favorites'],
        manual_parameters=[
            openapi.Parameter(
                name="book_id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор книги",
                required=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            book_id = self.kwargs.get('book_id')
            if not book_id:
                return Response({
                    'error': 'book_id parameter is missing.'},
                    status=status.HTTP_400_BAD_REQUEST)

            book = get_object_or_404(Book, id=book_id)

            favorite_books, created = FavoriteBook.objects.get_or_create(user=user, book=book)
            if created:
                return Response({
                    'message': 'Book added to favorites successfully.'},
                    status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': 'Book is already in favorites.'},
                    status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FavoritesBookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        favourite_books = user.favorite_books.select_related('genre', 'author').all()
        return favourite_books

    @swagger_auto_schema(
        tags=['Favorites'],
        manual_parameters=[
            openapi.Parameter('page', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Номер страницы для постраничных результатов.'),
            openapi.Parameter('limit', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Количество результатов, возвращаемых на страницу.'),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RemoveFromFavoritesView(generics.DestroyAPIView):
    queryset = FavoriteBook.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Favorites'],
        manual_parameters=[
            openapi.Parameter('book_id', openapi.IN_PATH,
                              description="ID книги, которую вы хотите удалить из избранного",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            204: "Book removed from favorites successfully.",
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            book_id = self.kwargs.get('book_id')

            if not book_id:
                return Response({
                    'error': 'book_id parameter is missing.'},
                    status=status.HTTP_400_BAD_REQUEST)

            book = get_object_or_404(Book, id=book_id)

            try:
                favorite_books = FavoriteBook.objects.get(user=user, book=book)
                favorite_books.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except FavoriteBook.DoesNotExist:
                return Response({
                    'message': 'Book is not in favorites.'},
                    status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
