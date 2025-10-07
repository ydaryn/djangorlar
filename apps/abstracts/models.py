# Python modules
from typing import Any

# from datetime import datetime, timezone

# Django modules
from django.db.models import Model, DateTimeField
from django.utils import timezone as django_timezone


class AbstractBaseModel(Model):
    """
    Abstract base model with common fields.
    """

    created_at = DateTimeField(
        auto_now_add=True
    )
    updated_at = DateTimeField(
        auto_now=True
    )
    deleted_at = DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        """Meta class for AbstractBaseModel."""

        abstract = True

    


class AbstractSoftDeletableModel(Model):
    """
    To support soft delete
    """
    created_at = DateTimeField(
        auto_now_add=True
    )
    updated_at = DateTimeField(
        auto_now=True
    )
    deleted_at = DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        """Meta class for AbstractBaseModel."""
        abstract = True

    def delete (self, *args : tuple[Any, ...], **kwargs : dict[str, Any]) -> None:
        if not self.deleted_at:
            self.deleted_at= django_timezone.now()  
            self.save(update_fields=["deleted_at"])
    
    def is_deleted(self) -> bool:
        """
        cjeck if deleted
        """
        return self.deleted_at is not None
    
    def __str__(self) -> str:
        base_str= super().__str__()
        return f"{base_str} [Deleted]" if self.is_deleted else base_str 