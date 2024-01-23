
from datetime import timedelta, date
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from .moon import calculate_moon_phase


# ----------------------------
# MoonPhaseCreatorForm
# ----------------------------
@register_snippet
class MoonPhaseCreatorForm(models.Model):
    selected_date = models.DateField(
        default=timezone.now
    )
    before_selected_date = models.IntegerField(default=10)
    after_selected_date = models.IntegerField(default=90)

    class Meta:
        verbose_name = _("Moon Phase Creator Form")
        verbose_name_plural = _("Moon Phase Creator Form")

    def __str__(self):
        start_date = self.selected_date - timedelta(days=self.before_selected_date)
        end_date = self.selected_date + timedelta(days=self.after_selected_date)
        return f'Moon Phase from {start_date} to {end_date}'

    def save(self, *args, **kwargs):
        date_str = self.selected_date.strftime('%Y-%m-%d')
        before_date = self.before_selected_date
        after_date = self.after_selected_date
        calculate_moon_phase(date_str, before_date, after_date)

        super().save(*args, **kwargs)


# ----------------------------
# ImportantDaysInLunarCalendar
# ----------------------------
@register_snippet
class ImportantDaysInLunarCalendar(ClusterableModel):
    """
    Important Days in Lunar Calendar
    """

    # Choices for moon phase
    MOON_PHASE_CHOICES = [
        ('01', 'ขึ้น'),
        ('02', 'แรม'),
    ]

    # Choices for day (1-15)
    DAY_CHOICES = [(f"{i:02d}", f"{i:2d}") for i in range(1, 16)]

    # Adjusted MONTH_CHOICES
    MONTH_CHOICES = [
        ('01', '1'),
        ('02', '2'),
        ('03', '3'),
        ('04', '4'),
        ('05', '5'),
        ('06', '6'),
        ('07', '7'),
        ('08', '8'),
        ('09', '88'),
        ('10', '9'),
        ('11', '10'),
        ('12', '11'),
        ('13', '12'),
    ]

    # Fields for lunar in normal year
    moon_phase = models.CharField(_("moon phase"), max_length=10, choices=MOON_PHASE_CHOICES, default='01')
    lc_day = models.CharField(_("day"), max_length=2, choices=DAY_CHOICES)
    lc_month = models.CharField(_("month"), max_length=2, choices=MONTH_CHOICES)

    # Fields for lunar date in adhikamasa year
    moon_phase_adhikamasa = models.CharField(_("moon phase"), max_length=10, choices=MOON_PHASE_CHOICES, default='01')
    lc_day_adhikamasa = models.CharField(_("day"), max_length=2, choices=DAY_CHOICES)
    lc_month_adhikamasa = models.CharField(_("month"), max_length=2, choices=MONTH_CHOICES)

    # Fields Lunar date
    lunar_date = models.CharField(_("lunar date"), max_length=25, blank=True)
    lunar_date_in_adhikamasa = models.CharField(_("lunar date in adhikamasa"), max_length=25, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('moon_phase'),
            FieldPanel('lc_day'),
            FieldPanel('lc_month'),
        ], heading="Lunar Date"),
        MultiFieldPanel([
            FieldPanel('moon_phase_adhikamasa'),
            FieldPanel('lc_day_adhikamasa'),
            FieldPanel('lc_month_adhikamasa'),
        ], heading="Lunar Date in Adhikamasa"),
        InlinePanel('lunar_calendar_details', label=_("Details")),
    ]

    class Meta:
        verbose_name = _("Important Days in Lunar Calendar")
        verbose_name_plural = _("Important Days in Lunar Calendar")
        ordering = ['lc_month', 'moon_phase', 'lc_day']

    def __str__(self):
        details_names = [detail.name for detail in self.lunar_calendar_details.all()]
        details_str = ", ".join(details_names)
        return f"{self.lunar_date} - {details_str}"

    def save(self, *args, **kwargs):
        # Update lunar_date from the fields for lunar_date
        moon_phase_display = self.get_moon_phase_display()
        lc_month_display = self.get_lc_month_display()
        lc_day_display = self.get_lc_day_display()
        self.lunar_date = f"{moon_phase_display} {lc_day_display.strip()} ค่ำ เดือน {lc_month_display.strip()}"

        # Update lunar_date_in_adhikamasa from the fields for lunar_date_in_adhikamasa
        moon_phase_adhikamasa_display = self.get_moon_phase_adhikamasa_display()
        lc_month_adhikamasa_display = self.get_lc_month_adhikamasa_display()
        lc_day_adhikamasa_display = self.get_lc_day_adhikamasa_display()
        self.lunar_date_in_adhikamasa = f"{moon_phase_adhikamasa_display} {lc_day_adhikamasa_display.strip()} ค่ำ เดือน {lc_month_adhikamasa_display.strip()}"

        super().save(*args, **kwargs)

class LunarCalendarDetail(Orderable, models.Model):
    lunar_calendar_day = ParentalKey(
        ImportantDaysInLunarCalendar,
        related_name='lunar_calendar_details',
        verbose_name=_('Detail')
    )
    name = models.CharField(_('name'), max_length=255)
    buddhist_commemorative_day = models.BooleanField(
        default=True, verbose_name=_('Buddhist Commemorative Day')
    )
    article_page = models.OneToOneField(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Article Page')
    )

    def __str__(self):
        return self.name


# ----------------------------
# ImportantDaysInSolarCalendar
# ----------------------------
@register_snippet
class ImportantDaysInSolarCalendar(ClusterableModel):
    """
    Important Days in Solar Calendar
    """

    class Meta:
        verbose_name = _("Important Days in Solar Calendar")
        verbose_name_plural = _("Important Days in Solar Calendar")
        ordering = ['month', 'day']

    DAY_CHOICES = [(i, i) for i in range(1, 32)]  # วันที่ 1 ถึง 31

    MONTH_CHOICES = [
        (1, _("January")),
        (2, _("February")),
        (3, _("March")),
        (4, _("April")),
        (5, _("May")),
        (6, _("June")),
        (7, _("July")),
        (8, _("August")),
        (9, _("September")),
        (10, _("October")),
        (11, _("November")),
        (12, _("December")),
    ]

    day = models.IntegerField(_('day'), choices=DAY_CHOICES, blank=False, null=True)
    month = models.IntegerField(_('month'), choices=MONTH_CHOICES, blank=False, null=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('day'),
            FieldPanel('month'),
        ], heading="Solar Calendar Date"),
        InlinePanel('solar_calendar_details', label=_("Details")),
    ]

    def __str__(self):
        details_names = [detail.name for detail in self.solar_calendar_details.all()]
        details_str = ", ".join(details_names)
        return f"{self.day}/{self.month} - {details_str}"

class SolarCalendarDetail(Orderable, models.Model):
    solar_calendar_day = ParentalKey(
        ImportantDaysInSolarCalendar,
        related_name='solar_calendar_details',
        verbose_name=_('Detail')
    )
    name = models.CharField(_("name"), max_length=255)
    article_page = models.OneToOneField(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Article Page')
    )

    def __str__(self):
        return self.name


# ----------------------------
# PatidinaPakkhaganana
# ----------------------------
def validate_buddhist_year(value):
    if not value.isdigit() or len(value) != 4 or int(value) < 2500:
        raise ValidationError(
            _('The year must be a 4-digit number and no less than 2500 (Buddhist Era).'),
            params={'value': value},
        )

@register_snippet
class PatidinaPakkhaganana(ClusterableModel):
    """
    Uposadha day of Dhammayuttikanikaya
    """
    title = models.CharField(
        _('title'),
        max_length=255,
        validators=[validate_buddhist_year],
        help_text=_('Enter the year in Buddhist Era format, which should be a 4-digit number and no less than 2500.')
    )

    class Meta:
        verbose_name = _("Paṭidina Pakkhagaṇanā")
        verbose_name_plural = _("Paṭidina Pakkhagaṇanā")

    panels = [
        FieldPanel('title'),
        InlinePanel('uposatha_of_pakkhaganana', label=_("Uposatha Day")),
    ]

    def __str__(self):
        return self.title

class UposathaOfPakkhaganana(Orderable, models.Model):
    # Choices for moon phase
    MOON_PHASE_CHOICES = [
        ('last_quarter', 'จันทร์ลับ'),
        ('new_moon', 'จันทร์ดับ'),
        ('first_quarter', 'จันทร์กึ่ง'),
        ('full_moon', 'จันทร์เพ็ญ'),
    ]

    patidina_pakkhaganana = ParentalKey(
        PatidinaPakkhaganana,
        related_name='uposatha_of_pakkhaganana',
        verbose_name=_('Uposatha Day')
    )
    selected_date = models.DateField()
    moon_phase = models.CharField(_("moon phase"), max_length=15, choices=MOON_PHASE_CHOICES)

    def __str__(self):
        phase = self.get_moon_phase_display()
        return f"{self.selected_date.strftime('%Y-%m-%d')}-{phase}"
