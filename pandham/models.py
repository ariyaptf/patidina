from django.db import models
from django.utils.translation import gettext_lazy as _
from coderedcms.fields import CoderedStreamField
from coderedcms.blocks import LAYOUT_STREAMBLOCKS
from custom_media.models import CustomImage as Image
from wagtail.admin.panels import FieldPanel

class PanDhamTargetGroup(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Group Name")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True
    )
    priority = models.IntegerField(
        default=0,
        verbose_name=_("Priority")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Target Group")
        verbose_name_plural = _("Target Groups")
        ordering = ['priority', 'name']


class PanDhamTarget(models.Model):
    group = models.ForeignKey(
        PanDhamTargetGroup,
        on_delete=models.CASCADE,
        verbose_name=_("Target Group"),
        related_name="targets"
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    address = models.TextField(
        verbose_name=_("Address")
    )
    requested_books = models.PositiveIntegerField(
        verbose_name=_("Requested Books")
    )
    request_date = models.DateTimeField(
        verbose_name=_("Request Date")
    )
    additional_info = models.TextField(
        verbose_name=_("Additional Information"),
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.group.name}"

    class Meta:
        verbose_name = _("Target")
        verbose_name_plural = _("Targets")


class PanDhamBook(models.Model):
    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stock")

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    short_description = models.CharField(
        max_length=500,
        verbose_name=_("Short Description"),
        blank=True,
    )
    cover_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="book_cover",
        null=True
    )
    description = CoderedStreamField(
        LAYOUT_STREAMBLOCKS,
        verbose_name=_("content"),
        blank=True,
        use_json_field=True,
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    initial_stock = models.IntegerField(
        default=0
    )
    stock = models.IntegerField(
        default=0
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('short_description'),
        FieldPanel('cover_image'),
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('initial_stock'),
        FieldPanel('stock'),
    ]

    def __str__(self):
        return self.name


class SupportPublication(models.Model):
    book = models.ForeignKey(
        PanDhamBook,
        on_delete=models.CASCADE,
        verbose_name=_("PanDham Book"),
        related_name="support_publication"
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    date_contribute = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date")
    )
    amount_contributed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Amount")
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity")
    )
    distribution_preference = models.CharField(
        max_length=100,
        choices=[
            ('request_book', _("Request Book")),
            ('no_book_request', _("No Book Requested"))
        ],
        verbose_name=_("Distribution Preference")
    )
    requested_books = models.PositiveIntegerField(
        verbose_name=_("Requested Books"),
        default=0
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name=_("Phone Number")
    )
    shipping_address = models.TextField(
        blank=True,
        verbose_name=_("Shipping Address")
    )
    otp = models.CharField(
        max_length=6,
        verbose_name=_("OTP Number")
    )
    pandhann_books = models.PositiveIntegerField(
        verbose_name=_("PanDham Books"),
        default=0
    )
    target_groups = models.ManyToManyField(
        'PanDhamTargetGroup',
        blank=True,
        verbose_name=_("Target Groups")
    )
    target_address = models.TextField(
        blank=True,
        verbose_name=_("Target Address")
    )
    note = models.TextField(
        verbose_name=_("Note"),
        blank=True
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_("Is Completed")
    )

    def __str__(self):
        return f"{self.name} - {self.amount_contributed}"

    class Meta:
        verbose_name = _("Support Publication")
        verbose_name_plural = _("Support Publications")
