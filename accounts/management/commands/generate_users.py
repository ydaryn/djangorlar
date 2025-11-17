from typing import Any
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from faker import Faker
import random
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.db import transaction

class Command(BaseCommand):
    help = 'Generate random users'

    DEPARTMENTS = ['HR', 'IT', 'Sales', 'Marketing', 'Finance']
    ROLES = ['admin', 'employee', 'manager']

    def __generate_users(self, user_count: int=10000) -> None:
        fake=Faker()

        password_hash = make_password('12345')
        users_before = CustomUser.objects.count()
        created_users:list[CustomUser] = []

        batch_size: int = 1000
        created_total: int = 0

        for i in range(user_count):
            profile = {
                "email": fake.unique.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "phone": fake.phone_number(),
                "city": fake.city(),
                "country": fake.country(),
                "department": random.choice(self.DEPARTMENTS),
                "role": random.choice(self.ROLES),
                "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=65),
                "salary": round(random.uniform(30000, 120000), 2),
                "is_active": True,
                "is_staff": False,
                "date_joined": fake.date_time_between(start_date='-5y', end_date='now'),
                "password": password_hash,
            }
            created_users.append(CustomUser(**profile))

            if len(created_users) >= batch_size:
                CustomUser.objects.bulk_create(created_users, ignore_conflicts=True)
                created_total += len(created_users)
                created_users.clear()
                self.stdout.write(self.style.WARNING(f'Created {created_total} users so far...'))
        if created_users:
            CustomUser.objects.bulk_create(created_users, ignore_conflicts=True)
            created_total += len(created_users)

        users_after: int = CustomUser.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {users_after - users_before} users.'
            )
        )
    def handle(self, *args : tuple[Any, ...], **kwargs:dict[str,Any]) -> None:
            start_time:datetime = datetime.now()
            self.__generate_users(user_count=10000)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Total time taken: {datetime.now() - start_time}'
                )
            )
    