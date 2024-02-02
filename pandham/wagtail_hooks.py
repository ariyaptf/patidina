from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from .models import (
    PanDhamTargetGroup, PanDhamTarget, PanDhamBook, SupportPublication
)

class PanDhamTargetGroupAdmin(ModelAdmin):
    model = PanDhamTargetGroup
    menu_label = _("Target Group")
    menu_icon = 'folder'
    list_display = ('name',)
    search_fields = ('name', 'description')

class PanDhamTargetAdmin(ModelAdmin):
    model = PanDhamTarget
    menu_label = _("Target")
    menu_icon = 'list-ul'
    list_display = ('name', 'group')
    list_filter = ('group',)
    search_fields = ('name',)

class PanDhamBookAdmin(ModelAdmin):
    model = PanDhamBook
    menu_label = _("Stock")
    menu_icon = 'decimal'
    list_display = ('name',)
    search_fields = ('name', 'short_description')

class SupportPublicationAdmin(ModelAdmin):
    model = SupportPublication
    menu_label = _("Support Publication")
    menu_icon = 'doc-full'
    list_filter = ('distribution_preference', 'target_groups', 'is_completed')
    list_display = ('name', 'date_contribute', 'phone_number',
                    'amount_contributed', 'quantity', 'is_completed')
    search_fields = ('name', 'phone_number', 'shipping_address',)


class PanDhamGroup(ModelAdminGroup):
    menu_label = _("PanDham")
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 700  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (PanDhamTargetGroupAdmin, PanDhamTargetAdmin,
             PanDhamBookAdmin, SupportPublicationAdmin)

modeladmin_register(PanDhamGroup)
