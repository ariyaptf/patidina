"""
Create or customize your page models here.
"""
import random
from datetime import date, datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from coderedcms.blocks import (
    CONTENT_STREAMBLOCKS,
)
from coderedcms.fields import CoderedStreamField
from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from coderedcms.models import CoderedStreamFormPage
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.fields import StreamField
from custom_media.models import CustomImage as Image

from utils.moon import (
    convert_float_to_dms
)
from utils.calendar import (
    th_lunar_date,
    th_zodiac,
    era
)

from .blocks import (
    LAYOUT_STREAMBLOCKS,
    HTML_STREAMBLOCKS
)

# ------------------------------
# ArticlePage
# ------------------------------
class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"

class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


# ------------------------------
# EventPage
# ------------------------------
class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"

class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"

class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


# ------------------------------
# FormPage
# ------------------------------
class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"

class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")

class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


# ------------------------------
# LocationPage
# ------------------------------
class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]

class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


# ------------------------------
# WebPage
# ------------------------------
class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    body = StreamField(
        LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"


# ------------------------------
# TodayMessagePage
# ------------------------------
class TodayMessagePage(CoderedWebPage):
    """
    Short and impressive article for daily learning with today's calendar and events.
    """

    body = StreamField(
        LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    display_title = models.CharField(_('Display title'), max_length=255)
    linked_event = models.ForeignKey(
        'website.EventIndexPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("display_title"),
        FieldPanel('linked_event'),
    ]

    class Meta:
        verbose_name = "Today's Message"

    subpage_types = ['website.DailyQuotesPage']

    template = "website/pages/today_message_page.html"

    def get_random_background_image_url(self):
        background = Image.objects.filter(collection__name='Background')
        if background:
            selected_image = random.choice(background)
            return selected_image.file.url
        return None

    def get_background_image_for_title(self):
        background = Image.objects.filter(collection__name='Title Background')
        if background:
            selected_image = random.choice(background)
            return selected_image.file.url
        return None

    def get_daily_quote(self):
        today = date.today()
        all_quotes = self.get_children().type(DailyQuotesPage).live().specific()
        path_prefix = self.path
        daily_quotes_today = DailyQuotesPage.objects.filter(path__startswith=path_prefix, date_display=today)
        if daily_quotes_today.exists():
            return daily_quotes_today.first()
        else:
            if all_quotes.exists():
                return random.choice(all_quotes)
            return None

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        today = date.today()

        # รับวันที่ปัจจุบันและแปลงเป็นรูปแบบที่ต้องการ
        date_str = today.strftime('%Y-%m-%d')
        # เพิ่มวันที่ในรูปแบบที่เพื่อเปิดรูป
        context['date_str'] = date_str
        # ภาพ random พื้นหลัง
        context['background_image_url'] = self.get_random_background_image_url()
        context['background_image_for_title'] = self.get_background_image_for_title()
        # บทความสั้นประจำวัน
        context['daily_quote'] = self.get_daily_quote()
        # ปฏิทินสุริยคติ
        context['solar_date'] = today
        # ปฏิทินจันทรคติ
        context['lunar_date'] = th_lunar_date(today)
        # ตำแหน่งสังเกตุดวงจันทร์
        lat = self.seo_struct_org_dict.get('geo')['latitude']
        lon = self.seo_struct_org_dict.get('geo')['longitude']
        context['latitude'] = convert_float_to_dms(lat)
        context['longitude'] = convert_float_to_dms(lon)
        # ศักราช และปีนักษัตร
        context['BE'] = era(today, output_type=6)
        context['th_zodiac'] = th_zodiac(today)
        context['th_zodiac_no'] = th_zodiac(today, output_type=3)
        context['CE'] = era(today, output_type=7)
        # qr-code สำหรับหน้านี้
        context['page_link'] =  self.full_url

        return context


# ------------------------------
# DailyQuotesPage
# ------------------------------
class DailyQuotesPage(CoderedArticlePage):
    """
    The poetry or short article.
    """

    body = StreamField(
        LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    class Meta:
        verbose_name = "Daily Quotes"

    parent_page_types = ["website.TodayMessagePage"]
    subpage_types = []

    template = "website/pages/daily_quotes_page.html"

    def get_random_background_image_url(self):
        background = Image.objects.filter(collection__name='Background')
        if background:
            selected_image = random.choice(background)
            return selected_image.file.url
        return None

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['background_image_url'] = self.get_random_background_image_url()
        return context


# ------------------------------
# StreamFormPage
# ------------------------------
class StreamFormPage(CoderedStreamFormPage):
    class Meta:
        verbose_name = "Stream Form"

    template = "coderedcms/pages/stream_form_page.html"

class StreamFormConfirmEmail(CoderedEmail):
    page = ParentalKey("StreamFormPage", related_name="confirmation_emails")


# ------------------------------
# PTFPandhammaPage
# ------------------------------
