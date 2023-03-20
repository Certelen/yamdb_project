from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


class Command(BaseCommand):
    """Загрузка данных из CSV файлов из папки static/data в базу данных"""
    help = "Loads data from csv files in static/data"

    def handle(self, *args, **options):
        for categories in DictReader(
            open('static/data/category.csv', encoding="utf8")
        ):
            category = Category(
                id=categories['id'],
                name=categories['name'],
                slug=categories['slug'],
            )
            category.save()

        for genres in DictReader(
            open('static/data/genre.csv', encoding="utf8")
        ):
            genre = Genre(
                id=genres['id'],
                name=genres['name'],
                slug=genres['slug'],
            )
            genre.save()

        for titles in DictReader(
            open('static/data/titles.csv', encoding="utf8")
        ):
            title = Title(
                id=titles['id'],
                name=titles['name'],
                year=titles['year'],
                category_id=titles['category'],
            )
            title.save()

        for row in DictReader(
            open('static/data/genre_title.csv', encoding="utf8")
        ):
            titlegenre = TitleGenre(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )
            titlegenre.save()

        for users in DictReader(
            open('static/data/users.csv', encoding="utf8")
        ):
            user = User(
                id=users['id'],
                username=users['username'],
                email=users['email'],
                role=users['role'],
                bio=users['bio'],
                first_name=users['first_name'],
                last_name=users['last_name'],
            )
            user.save()

        for reviews in DictReader(
            open('static/data/review.csv', encoding="utf8")
        ):
            review = Review(
                id=reviews['id'],
                title_id=reviews['title_id'],
                text=reviews['text'],
                author_id=reviews['author'],
                score=reviews['score'],
                pub_date=reviews['pub_date'],
            )
            review.save()

        for comments in DictReader(
            open('static/data/comments.csv', encoding="utf8")
        ):
            comment = Comment(
                id=comments['id'],
                review_id=comments['review_id'],
                text=comments['text'],
                author_id=comments['author'],
                pub_date=comments['pub_date'],
            )
            comment.save()
