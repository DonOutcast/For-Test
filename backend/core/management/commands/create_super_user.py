from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.utils import os_getenv


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = os_getenv("SUPER_USER_EMAIL", "adm@adm.ru")
        if not User.objects.filter(email=email).exists():
            super_user = User(
                is_superuser=True,
                is_staff=True,
                email=email,
                username=os_getenv("SUPER_USER_NAME", "adm")
            )
            super_user.set_password(os_getenv("SUPER_USER_PASSWORD", "adm"))
            super_user.save()
            self.stdout.write("Super user seed successful OK")
        else:
            self.stdout.write("Super user already exists")