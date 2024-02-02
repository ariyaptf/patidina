from django.http import HttpResponseRedirect
from wagtail import hooks
from django.utils.translation import gettext_lazy as _

from .models import (
    MoonPhaseCreatorForm,
)


@hooks.register('before_create_snippet')
def redirect_to_edit_if_exists(request, model):
    if model == MoonPhaseCreatorForm and MoonPhaseCreatorForm.objects.exists():
        instance = MoonPhaseCreatorForm.objects.first()
        # ใช้ URL โดยตรง
        url = f'/admin/snippets/utils/moonphasecreatorform/edit/{instance.pk}/'
        return HttpResponseRedirect(url)


