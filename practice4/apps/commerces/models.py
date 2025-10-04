from decimal import Decimal
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
from django.conf import settings
class Adress(Model):
    """
    Commerces & address
    """
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name= "addresses",
    )
    LABEL_MAX_LEN=100
    CITY_MAX_LEN=100
    STREET_MAX_LEN=100
    
    label = CharField(
        blank=True,
        max_length=LABEL_MAX_LEN,
        default="",
    )
    street = CharField(
        blank=True,
        max_length=STREET_MAX_LEN,
        default="",
    )
    city = CharField(
        blank=True,
        max_length=CITY_MAX_LEN,
        default="",
    )
    postal_code=CharField(
        blank=True,
        default="",
    )
    is_default= BooleanField(
        default=False,
    )

    class Meta:
        ordering = ("user_id", "is_default", "id")

class PromoCode(Model):
    """
    Unique codes
    """
    CODE_MAX_LEN=100
    DESCRIPTION_MAX_LEN=255
    DISCOUNT_TYPE_MAX_LEN=100

    code = CharField(
        max_length=CODE_MAX_LEN,
    )
    description = CharField(
        max_length=DESCRIPTION_MAX_LEN,
        default="",
    )
    discount_type= CharField(
        max_length=DISCOUNT_TYPE_MAX_LEN,
        default="",
    )
    value= DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    is_active = BooleanField(
        default=True,
    )
    created_at = DateTimeField(
        auto_now_add=True,
    )


class Order(Model):
    """
    Orders with enum
    """
    STATUS_NEW="new"
    STATUS_CONFIRMED="confirmed"
    STATUS_DELIVERING= "delivering"
    STATUS_DONE= "done"
    STATUS_MAX_LEN = 100
    STATUS_CHOICES = (
        (STATUS_NEW, "new"),
        (STATUS_CONFIRMED, "confirmed"),
        (STATUS_DELIVERING, "delivering"),
        (STATUS_DONE, "done"),
    )

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= PROTECT,
        related_name = "orders",
    )
    restaurant = ForeignKey(
        "catalogs.Restaurant",
        on_delete=PROTECT,
        related_name="orders",
    )
    address= ForeignKey(
        Adress,
        on_delete=PROTECT,
        related_name="orders",
    )
    status = CharField(
        max_length=STATUS_MAX_LEN,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    subtotal = DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    discount_total = DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    total = DecimalField(
        max_digits = 10,
        decimal_places= 2,
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

    class Meta:
        ordering = ("created_at",)


class OrderItem(models.Model):
    """
    Snapshot of MenuItem inside an order.
    menu_item can be nullable.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(
        "catalogs.MenuItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    item_name = models.CharField()   # snapshot
    item_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}×{self.item_name} (order {self.order_id})"


class OrderItemOption(Model):
    """
    Selected option snapshot for an OrderItem
    """
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="options")
    option_name = models.TextField()
    price_delta = DecimalField(
        max_digits=9,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.option_name} (+{self.price_delta})"


class OrderPromo(models.Model):
    """
    Through-table between Order and PromoCode with applied_amount.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promocode = models.ForeignKey(PromoCode, on_delete=models.PROTECT)
    applied_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "promocode"],
                name="unique_order_promocode"
            )
        ]

    def __str__(self):
        return f"{self.promocode.code} on {self.order_id} = {self.applied_amount}"