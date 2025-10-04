from django.db import models

#Django modules
from django.db.models import(
    Model,
    CharField,
    DateTimeField,
    TextField,
    IntegerField,
    ForeignKey,
    ManyToManyField,
    UniqueConstraint,
    BooleanField,
    DecimalField,
    constraints,
    PROTECT,
    CASCADE,
)
from django.contrib.auth.models import User


class Restaurant(Model):
    """"
    Catalogs: Restaurants
    """
    NAME_MAX_LEN=100
    DESCRIPTION_MAX_LEN=255

    name = CharField(
        max_length=NAME_MAX_LEN,
    )
    description= CharField(
        max_length=DESCRIPTION_MAX_LEN,
        blank=True,
        default="",
    )
    is_active=BooleanField(
        default=True,
    )
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


class MenuItem(Model):
    """
    Catalogs:MenuItem
    """
    NAME_MAX_LEN=100
    DESCRIPTION_MAX_LEN=255

    restaurant = ForeignKey(
        Restaurant,
        on_delete=CASCADE,
        related_name="menu_items",
    )
    name = CharField(
        max_length=NAME_MAX_LEN,
    )
    description = CharField(
        max_length=DESCRIPTION_MAX_LEN,
        blank=True,
        default="",
    )
    base_price = DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    is_available= BooleanField(
        default=True,
    )
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
    categories= ManyToManyField(
        "Category",
        through="ItemCategory",
        through_fields=("menu_item", "category"),
        blank=True,
        related_name="menu_items"
    )
    options = ManyToManyField(
        "Option",
        through="ItemOption",
        through_fields=("menu_item", "option"),
        blank=True,
        related_name="menu_items",
    )

    class Meta:
        ordering = ("restaurant_id", "id")

class Category(Model):
    """
    Categories
    """
    NAME_MAX_LEN=100
    name = CharField(
        max_length = NAME_MAX_LEN
    )

class Option(Model):
    """
    Options
    """
    NAME_MAX_LEN=100
    name = CharField(
        max_length = NAME_MAX_LEN
    )

class ItemCategory(Model):
    """
    Through table between MenuItem and Category with extra field position
    """
    menu_item = ForeignKey(
        MenuItem,
        on_delete= CASCADE,
    )
    category = ForeignKey(
        Category,
        on_delete=CASCADE,
    )
    position = IntegerField(
        default=0,
    )
    class Meta:
        constraints = [
            UniqueConstraint(
                fields= ["menu_item", "category"],
                name= "unique_menuitem_category"
            )
        ]
        ordering = ("category_id", "position")

class ItemOption(Model):
    """
    Through table between MenuItem and Option with price_delta and is_default
    """
    menu_item = ForeignKey(
        MenuItem,
        on_delete=CASCADE,
    )
    option = ForeignKey(
        Option,
        on_delete=CASCADE,
    )
    price_delta = DecimalField(
        max_digits=10,
        decimal_places=2
    )
    is_default= BooleanField(
        default=False,
    )
    
    class Meta:
        constraints=[
            UniqueConstraint(
                fields=["menu_item", "option"],
                name="unique_menuitem_option"
            )
        ]