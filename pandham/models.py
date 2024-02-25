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
        related_name="support_publication",
        help_text=_("Select the PanDham book for support in printing and distribution.")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        default=_("Anonymous"),
        help_text=_("Please specify name, pseudonym, or dedication.")
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name=_("Phone Number"),
        help_text=_("Contactable mobile phone number ie.0988888888 (not publicly disclosed).")
    )
    amount_contributed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Contribute funds"),
        help_text=_("Intention to support the printing and distribution.")
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        help_text=_("Calculated result in the number of book volumes."),
        default=0
    )
    distribution_preference = models.CharField(
        max_length=100,
        choices=[
            ('request_book', _("Request Book")),
            ('no_book_request', _("No Book Requested"))
        ],
        verbose_name=_("Distribution Preference"),
        default='no_book_request',
    )
    requested_books = models.PositiveIntegerField(
        verbose_name=_("Requested Books"),
        default=0,
        help_text=_("Enter the number of books requested.")
    )
    shipping_address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Shipping Address")
    )
    for_PanDham = models.PositiveIntegerField(
        verbose_name=_("Number of books for PanDham"),
        default=0
    )
    target_groups = models.ManyToManyField(
        'PanDhamTargetGroup',
        blank=True,
        verbose_name=_("Target Groups"),
        help_text=_("Select the target groups for this support publication.")
    )
    target_address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Target Address"),
        help_text=_("Please provide the address of the PanDham recipient.")
    )
    note = models.TextField(
        verbose_name=_("Memo or Note"),
        blank=True,
        null=True,
        help_text=_("Enter any additional notes or comments.")
    )
    otp = models.CharField(
        max_length=6,
        verbose_name=_("OTP"),
        help_text=_("Enter the OTP number.")
    )
    date_contribute = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date")
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
