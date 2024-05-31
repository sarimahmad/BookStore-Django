import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
# from accounts.models import
from faker import Faker

faker = Faker()

AkiraUser = get_user_model()
USER = {
    "email": os.environ.get("SUPER_USER_EMAIL", None),
    "password": os.environ.get("SUPER_USER_PASSWORD", None),
    "username": os.environ.get("SUPER_USER_NAME", None),
    "is_staff": True
}


class Command(BaseCommand):
    help = "Seeds the database with fake data for users, posts, libraries, and interactions"

    def handle(self, *args, **options):
        # Superuser creation
        super_user_email = os.environ.get("SUPER_USER_EMAIL", None)
        super_user_password = os.environ.get("SUPER_USER_PASSWORD", None)
        super_user_username = os.environ.get("SUPER_USER_NAME", None)

        if super_user_email and super_user_password and super_user_username:
            if not AkiraUser.objects.filter(email=super_user_email).exists():
                AkiraUser.objects.create_superuser(
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

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))
