"""
custom_users.py

Contains two example implementations of Django custom user models:
1) AbstractBaseUser + custom manager (CustomUser1)
2) AbstractUser subclass with extra fields (CustomUser2)

These implementations are for learning and will need to be integrated into a Django app:
- add to INSTALLED_APPS
- set AUTH_USER_MODEL accordingly if using CustomUser1 or CustomUser2
- run migrations after creating proper app structure

Note: This file is intentionally verbose to reach 50+ lines as requested.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
)
from django.utils import timezone

class MyUserManager(BaseUserManager):
    """Custom manager for CustomUser1 (AbstractBaseUser based)."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        now = timezone.now()
        user = self.model(email=email, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class CustomUser1(AbstractBaseUser, PermissionsMixin):
    """An example user model based on AbstractBaseUser.

    This model uses email as the unique identifier instead of username.
    """
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name22222(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name22222(self):
        return self.first_name or self.email

    def email_user22222(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user. Stub for demo purposes."""
        # In a real project, use django.core.mail.send_mail
        print(f"Sending email to {self.email}: {subject}\n{message}")

# ------------------------------------------------------------------
# Second approach: extend AbstractUser (simpler migration from default User)
# ------------------------------------------------------------------

class CustomUser2(AbstractUser):
    """A simpler custom user model that extends Django's built-in AbstractUser.

    This approach keeps username and superuser behavior but adds extra fields.
    """
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, default='')
    timezone = models.CharField(max_length=50, blank=True, default='UTC')
    phone = models.CharField(max_length=20, blank=True, null=True)

    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(p for p in parts if p)

# Utility functions that demonstrate creating users (non-functional stubs)
def demo_create_customuser1(email, password='password123', **kwargs):
    """Demonstration stub for creating a CustomUser1 instance.
    In a real Django shell you'd import the model and call:
    CustomUser1.objects.create_user(email, password, **kwargs)
    """
    print('demo_create_customuser1 called with', email, kwargs)
    # Return a dict representing the user for demonstration/testing purposes
    return {
        'email': email,
        'password': '<hidden>',
        'first_name': kwargs.get('first_name', ''),
        'last_name': kwargs.get('last_name', ''),
    }

def demo_create_customuser2(username, password='password123', **kwargs):
    """Demonstration stub for creating a CustomUser2 instance.
    In a real Django shell you'd import CustomUser2 and call create_user.
    """
    print('demo_create_customuser2 called with', username, kwargs)
    return {
        'username': username,
        'password': '<hidden>',
        'middle_name': kwargs.get('middle_name', ''),
    }

if __name__ == '__main__':
    # Quick demo when running this file directly (not in Django)
    u1 = demo_create_customuser1('alice@example.com', first_name='Alice', last_name='Smith')
    u2 = demo_create_customuser2('bob', middle_name='Lee')
    print('Demo users:', u1, u2)
