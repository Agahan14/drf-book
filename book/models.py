from django.db import models
from django.db.models import Avg
from django.core.cache import cache
from authentication.models import User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    genre = models.ForeignKey(
        Genre,
        related_name='books',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE,
    )
    description = models.TextField()
    publication_date = models.DateField()

    favourites = models.ManyToManyField(
        User,
        through="FavoriteBook",
        related_name="favorite_books",
    )

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        average = reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average, 2) if average is not None else 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_cached_average_rating()

    def update_cached_average_rating(self):
        cache_key = f'book_average_rating_{self.id}'
        reviews = self.reviews.all()
        average = reviews.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(average, 2) if average is not None else 0
        cache.set(cache_key, average_rating, timeout=60)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user} for {self.book}"


class FavoriteBook(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        Book,
        related_name='favorited_by',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return self.user
