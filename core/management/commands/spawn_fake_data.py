import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from accounts.models import StoreUser
from store.models import Author, Category, Book
from faker import Faker

faker = Faker()

StoreUser = get_user_model()
USER = {
    "email": os.environ.get("SUPER_USER_EMAIL", None),
    "password": os.environ.get("SUPER_USER_PASSWORD", None),
    "username": os.environ.get("SUPER_USER_NAME", None),
    "is_staff": True
}


class Command(BaseCommand):
    help = "Seeds the database with fake data for users, authors, books, and categories"

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, help='Number of fake users to create', default=50)
        parser.add_argument('--entities_per_user', type=int, help='Number of fake authors, books, and categories per user', default=20)

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        # Superuser creation
        super_user_email = os.environ.get("SUPER_USER_EMAIL", None)
        super_user_password = os.environ.get("SUPER_USER_PASSWORD", None)
        super_user_username = os.environ.get("SUPER_USER_NAME", None)

        if super_user_email and super_user_password and super_user_username:
            if not StoreUser.objects.filter(email=super_user_email).exists():
                StoreUser.objects.create_superuser(
                    email=super_user_email,
                    username=super_user_username,
                    password=super_user_password
                )
                self.stdout.write(self.style.SUCCESS(f'Superuser {super_user_email} created'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Superuser {super_user_email} already exists'))
        else:
            self.stdout.write(self.style.WARNING('Superuser environment variables not fully set'))

        self.stdout.write(self.style.SUCCESS('Starting to seed data...'))

        # Create Users and their Authors, Categories, and Books
        for _ in range(options['users']):
            user = StoreUser.objects.create_user(
                email=faker.email(),
                username=faker.user_name(),
                password='password',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'User {user.username} created'))

            # Create Authors for the user
            for _ in range(options['entities_per_user']):
                author = Author.objects.create(
                    user=user,
                    name=faker.name(),
                    biography=faker.text(max_nb_chars=255),
                    date_of_birth=faker.date_of_birth(),
                    date_of_death=faker.date_of_birth() if faker.boolean() else None
                )

            # Create Categories for the user
            for _ in range(options['entities_per_user']):
                category = Category.objects.create(
                    user=user,
                    name=faker.word()
                )

            # Create Books for the user
            for _ in range(options['entities_per_user']):
                book = Book.objects.create(
                    user=user,
                    title=faker.sentence(),
                    author=author,  # you might want to select a random author linked to this user
                    published_date=faker.date(),
                    isbn=faker.isbn13(),
                    category=category,  # you might want to select a random category linked to this user
                    price=faker.random_int(min=10, max=1000)
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))