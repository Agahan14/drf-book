from rest_framework import serializers
from book.models import (
    Book,
    Genre,
    Author,
    Review,
)
from authentication.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]


class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "genre",
            "author",
            "average_rating",
        ]

    def get_average_rating(self, obj):
        return obj.average_rating


class ReviewByUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = ReviewByUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "user",
            "rating",
            "comment",
        ]


class BookDetailSerializer(BookSerializer):
    reviews = ReviewDetailSerializer(many=True, read_only=True)

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + [
            'description', 'publication_date', 'reviews'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "book",
            "user",
            "rating",
            "comment",
        ]
