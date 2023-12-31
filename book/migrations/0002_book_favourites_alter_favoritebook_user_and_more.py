# Generated by Django 4.2.8 on 2023-12-05 08:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='favourites',
            field=models.ManyToManyField(related_name='favorite_books', through='book.FavoriteBook', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='favoritebook',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterUniqueTogether(
            name='favoritebook',
            unique_together={('user', 'book')},
        ),
    ]
