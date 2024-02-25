import datetime
from django import forms
from .models import SupportPublication, PanDhamBook, PanDhamTargetGroup
from django.utils.translation import gettext_lazy as _
from django.forms.models import modelformset_factory


class SupportPublicationStepOneForm(forms.ModelForm):

    class Meta:
        model = SupportPublication
        fields = [
            'book', 'name',
            'phone_number'
        ]


class SupportPublicationStepTwoForm(forms.ModelForm):

    class Meta:
        model = SupportPublication
        fields = [
            'amount_contributed',
            'quantity',
            'distribution_preference'
        ]
        js= ('pandham/js/support.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['readonly'] = True


class SupportPublicationStepThreeForm(forms.ModelForm):

    target_groups = forms.ModelMultipleChoiceField(
        queryset=PanDhamTargetGroup.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_("Target Groups"),
        help_text=_("Select the target groups for this support publication."),
        required=False
    )

    class Meta:
        model = SupportPublication
        fields = [
            'requested_books',
            'shipping_address',
            'for_PanDham',
            'target_groups',
            'target_address',
            'note',
        ]

        js= ('pandham/js/support.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requested_books'].widget.attrs['oninput'] = 'requested_books_change(event)'
        self.fields['for_PanDham'].widget.attrs['readonly'] = True
        self.fields['target_groups'].widget.attrs['onchange'] = 'target_groups_change(event, value)'


class SupportPublicationStepFourForm(forms.ModelForm):
    class Meta:
        model = SupportPublication
        fields = ['otp']


