from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Creating user groups"

    User.objects.create_superuser(username='admin123', email='', password='admin456')

    def handle(self, *attrs, **options):
        _, created = Group.objects.get_or_create(name='Player')
        _, created = Group.objects.get_or_create(name='Society')
